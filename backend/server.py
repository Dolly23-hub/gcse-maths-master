from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# LLM Setup
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

app = FastAPI()
api_router = APIRouter(prefix="/api")

# --- Pydantic Models ---
class TopicBase(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: str
    title: str
    slug: str
    tier: str  # Foundation, Higher, Both
    description: str
    explanation: str
    worked_examples: List[dict] = []
    key_points: List[str] = []
    difficulty: int = 1
    order: int = 0
    # Guided learning journey fields
    video_id: Optional[str] = None
    big_idea: Optional[str] = None
    visual_example: Optional[str] = None
    step_by_step: List[str] = []

class QuizQuestion(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic_id: str
    topic_title: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    difficulty: int = 1

class PastPaper(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    board: str
    year: str
    paper_number: int
    tier: str
    calculator_allowed: bool
    description: str
    link: str
    practice_questions: List[dict] = []

class Formula(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: str
    name: str
    formula: str
    description: str
    usage_example: str

class AITutorRequest(BaseModel):
    question: str
    topic: Optional[str] = None
    context: Optional[str] = None

class QuizCheckRequest(BaseModel):
    question_id: str
    selected_answer: int

class RevisionPlanRequest(BaseModel):
    exam_board: str
    exam_date: str  # ISO format date
    confidence: dict  # category -> 1-5 rating
    study_hours_per_day: float = 1.0
    use_ai: bool = True

# --- API Routes ---
@api_router.get("/")
async def root():
    return {"message": "GCSE Maths Master API"}

@api_router.get("/topics")
async def get_topics():
    topics = await db.topics.find({}, {"_id": 0}).sort("order", 1).to_list(200)
    return {"topics": topics}

@api_router.get("/topics/category/{category}")
async def get_topics_by_category(category: str):
    topics = await db.topics.find({"category": category}, {"_id": 0}).sort("order", 1).to_list(100)
    return {"topics": topics}

@api_router.get("/topics/{topic_id}")
async def get_topic(topic_id: str):
    topic = await db.topics.find_one({"id": topic_id}, {"_id": 0})
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@api_router.get("/past-papers/{board}")
async def get_past_papers(board: str):
    papers = await db.past_papers.find({"board": board}, {"_id": 0}).sort([("year", -1), ("paper_number", 1)]).to_list(100)
    return {"papers": papers, "board": board}

@api_router.get("/quizzes/{topic_id}")
async def get_quiz(topic_id: str):
    questions = await db.quizzes.find({"topic_id": topic_id}, {"_id": 0}).to_list(50)
    return {"questions": questions, "topic_id": topic_id}

@api_router.get("/quizzes")
async def get_all_quizzes():
    questions = await db.quizzes.find({}, {"_id": 0}).to_list(500)
    return {"questions": questions}

@api_router.post("/quiz/check")
async def check_quiz_answer(req: QuizCheckRequest):
    question = await db.quizzes.find_one({"id": req.question_id}, {"_id": 0})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    is_correct = question["correct_answer"] == req.selected_answer
    return {
        "correct": is_correct,
        "correct_answer": question["correct_answer"],
        "explanation": question["explanation"]
    }

@api_router.get("/formulas")
async def get_formulas():
    formulas = await db.formulas.find({}, {"_id": 0}).to_list(200)
    return {"formulas": formulas}

@api_router.get("/formulas/category/{category}")
async def get_formulas_by_category(category: str):
    formulas = await db.formulas.find({"category": category}, {"_id": 0}).to_list(100)
    return {"formulas": formulas}

@api_router.post("/revision-plan")
async def generate_revision_plan(req: RevisionPlanRequest):
    from datetime import date as date_type
    import math

    # Parse exam date
    try:
        exam_date = datetime.fromisoformat(req.exam_date).date()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format")

    today = datetime.now(timezone.utc).date()
    days_until_exam = (exam_date - today).days
    if days_until_exam < 1:
        raise HTTPException(status_code=400, detail="Exam date must be in the future")

    # Get all topics
    topics = await db.topics.find({}, {"_id": 0}).sort("order", 1).to_list(200)

    # Score topics by priority (lower confidence = higher priority)
    categories = ["Number", "Algebra", "Ratio & Proportion", "Geometry & Measures", "Probability & Statistics"]
    category_priority = {}
    for cat in categories:
        confidence = req.confidence.get(cat, 3)
        category_priority[cat] = 6 - confidence  # invert: 1 confidence -> 5 priority

    # Sort topics: highest priority first, then by difficulty
    def topic_sort_key(t):
        prio = category_priority.get(t["category"], 3)
        return (-prio, -t.get("difficulty", 1))

    sorted_topics = sorted(topics, key=topic_sort_key)

    # Calculate weeks available
    weeks_available = max(1, days_until_exam // 7)
    topics_per_week = max(1, math.ceil(len(sorted_topics) / weeks_available))

    # Build weekly schedule
    schedule = []
    for week_num in range(weeks_available):
        start_idx = week_num * topics_per_week
        end_idx = min(start_idx + topics_per_week, len(sorted_topics))
        week_topics = sorted_topics[start_idx:end_idx]
        if not week_topics:
            break

        week_start = today + __import__('datetime').timedelta(days=week_num * 7)
        week_end = week_start + __import__('datetime').timedelta(days=6)

        # Determine focus category for the week
        cat_counts = {}
        for t in week_topics:
            cat_counts[t["category"]] = cat_counts.get(t["category"], 0) + 1
        focus_category = max(cat_counts, key=cat_counts.get) if cat_counts else "Mixed"

        schedule.append({
            "week": week_num + 1,
            "start_date": week_start.isoformat(),
            "end_date": week_end.isoformat(),
            "focus_category": focus_category,
            "topics": [{"id": t["id"], "title": t["title"], "category": t["category"], "difficulty": t["difficulty"]} for t in week_topics],
            "activities": [
                f"Study {len(week_topics)} topic(s) - focus on {focus_category}",
                "Complete worked examples for each topic",
                "Take quizzes on covered topics",
                f"Spend ~{req.study_hours_per_day} hour(s) per day",
            ]
        })

    # Add final revision weeks if space
    if weeks_available > len(schedule):
        remaining = weeks_available - len(schedule)
        for i in range(min(remaining, 3)):
            week_num = len(schedule)
            week_start = today + __import__('datetime').timedelta(days=week_num * 7)
            week_end = week_start + __import__('datetime').timedelta(days=6)

            weak_cats = [cat for cat, prio in sorted(category_priority.items(), key=lambda x: -x[1])[:2]]
            schedule.append({
                "week": week_num + 1,
                "start_date": week_start.isoformat(),
                "end_date": week_end.isoformat(),
                "focus_category": "Revision & Practice",
                "topics": [],
                "activities": [
                    f"Review weak areas: {', '.join(weak_cats)}",
                    f"Complete {req.exam_board} past papers under timed conditions",
                    "Review mistakes from quizzes and past papers",
                    "Practice mixed questions across all topics",
                ]
            })

    # Generate AI tips if requested
    ai_tips = []
    if req.use_ai and EMERGENT_LLM_KEY:
        try:
            weak_areas = [cat for cat, conf in req.confidence.items() if conf <= 2]
            strong_areas = [cat for cat, conf in req.confidence.items() if conf >= 4]

            session_id = str(uuid.uuid4())
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=session_id,
                system_message="You are a GCSE Maths revision expert. Give exactly 5 short, practical revision tips (1-2 sentences each). Use British English. Be encouraging. Return as a JSON array of strings."
            )
            chat.with_model("openai", "gpt-5.2")

            prompt = f"A student is preparing for their {req.exam_board} GCSE Maths exam in {days_until_exam} days. "
            if weak_areas:
                prompt += f"They're struggling with: {', '.join(weak_areas)}. "
            if strong_areas:
                prompt += f"They're strong in: {', '.join(strong_areas)}. "
            prompt += f"They can study {req.study_hours_per_day} hours per day. Give 5 personalised revision tips as a JSON array of strings."

            user_message = UserMessage(text=prompt)
            response = await chat.send_message(user_message)

            # Try to parse JSON from response
            import json
            try:
                # Find JSON array in response
                start = response.find('[')
                end = response.rfind(']') + 1
                if start != -1 and end > start:
                    ai_tips = json.loads(response[start:end])
            except Exception:
                ai_tips = [response]
        except Exception as e:
            logger.error(f"AI tips error: {str(e)}")
            ai_tips = [
                "Focus on your weakest topics first - that's where you'll gain the most marks.",
                "Do at least one past paper per week under timed conditions.",
                "Always show your working in the exam - you get marks for method!",
                "Use the formula sheet to memorise key formulas before the exam.",
                "Get a good night's sleep before the exam - a fresh brain works better!"
            ]

    # Summary stats
    weak_cats = [cat for cat, conf in req.confidence.items() if conf <= 2]
    strong_cats = [cat for cat, conf in req.confidence.items() if conf >= 4]

    return {
        "exam_board": req.exam_board,
        "exam_date": req.exam_date,
        "days_remaining": days_until_exam,
        "weeks_remaining": weeks_available,
        "total_topics": len(sorted_topics),
        "weak_areas": weak_cats,
        "strong_areas": strong_cats,
        "schedule": schedule,
        "ai_tips": ai_tips,
    }

@api_router.post("/ai-tutor")
async def ai_tutor(req: AITutorRequest):
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="AI service not configured")
    try:
        session_id = str(uuid.uuid4())
        system_msg = """You are a friendly, encouraging GCSE Maths tutor for UK students aged 14-16. 
Your role is to explain mathematical concepts in simple, clear language that teenagers can understand.

Rules:
- Break down every problem step by step
- Use real-world examples students can relate to
- Be encouraging and positive
- Use British English spelling (colour, favourite, etc.)
- Reference GCSE exam boards (Edexcel, AQA, OCR) where relevant
- Format your response with clear headings and bullet points
- If showing calculations, show every step clearly
- End with a quick tip or encouragement
- Keep explanations concise but thorough
- Use markdown formatting for clarity"""
        
        if req.topic:
            system_msg += f"\n\nThe student is currently studying: {req.topic}"
        if req.context:
            system_msg += f"\n\nAdditional context: {req.context}"

        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=system_msg
        )
        chat.with_model("openai", "gpt-5.2")

        user_message = UserMessage(text=req.question)
        response = await chat.send_message(user_message)
        return {"response": response, "session_id": session_id}
    except Exception as e:
        logger.error(f"AI Tutor error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@api_router.post("/seed")
async def seed_database():
    # Clear existing data
    await db.topics.delete_many({})
    await db.quizzes.delete_many({})
    await db.past_papers.delete_many({})
    await db.formulas.delete_many({})

    # --- TOPICS ---
    # Guided learning journey enrichments (YouTube video + Big Idea + Visual Example + Steps)
    enrichments = {
        "num-1": {
            "video_id": "Iq-6CjlEUW4",
            "big_idea": "Fractions, decimals and percentages are three languages that describe the SAME number — swap freely between them.",
            "visual_example": "**Convert `3/4` through all three forms**\n\n```\n3/4  ──►  3 ÷ 4 = 0.75  ──►  0.75 × 100 = 75%\n```\n\n| Form        | Value |\n|-------------|-------|\n| Fraction    | 3/4   |\n| Decimal     | 0.75  |\n| Percentage  | 75%   |",
            "step_by_step": [
                "Identify the form you have (fraction, decimal, or percentage).",
                "Fraction → Decimal: divide the top (numerator) by the bottom (denominator).",
                "Decimal → Percentage: multiply by 100 (slide the decimal point 2 places right).",
                "Percentage → Fraction: write over 100, then simplify using the HCF.",
                "Always sanity-check by picking a known benchmark (½ = 0.5 = 50%).",
            ],
        },
        "num-2": {
            "video_id": "cxGyZ3Yx9ow",
            "big_idea": "Powers are shorthand for repeated multiplication; standard form is shorthand for very big or very small numbers.",
            "visual_example": "**Write `0.000 045` in standard form**\n\n```\n0.000045\n └─┴─┴─┴─┴─►  move 5 places right\n      4.5\n```\n\n**Answer:** `4.5 × 10⁻⁵` (negative because the number is small).",
            "step_by_step": [
                "Place the decimal point after the first non-zero digit.",
                "Count how many places the decimal moved.",
                "If the original was LARGE (>10), the power is positive.",
                "If the original was SMALL (<1), the power is negative.",
                "Write as: A × 10ⁿ where 1 ≤ A < 10.",
            ],
        },
        "num-3": {
            "video_id": "oK-EFDLeEqc",
            "big_idea": "Every whole number has a unique fingerprint of prime factors — use this fingerprint to unlock HCF and LCM.",
            "visual_example": "**Find the HCF and LCM of 24 and 36**\n\n```\n24 = 2 × 2 × 2 × 3   =  2³ × 3\n36 = 2 × 2 × 3 × 3   =  2² × 3²\n\nHCF  =  2² × 3      =  12   (lowest powers of SHARED primes)\nLCM  =  2³ × 3²     =  72   (highest powers of ALL primes)\n```",
            "step_by_step": [
                "Build a factor tree to break each number into prime factors.",
                "Write each number as a product of primes in index form.",
                "HCF: multiply SHARED primes, using the LOWEST power that appears.",
                "LCM: multiply ALL primes, using the HIGHEST power that appears.",
                "Check: HCF × LCM should equal the two numbers multiplied.",
            ],
        },
        "num-4": {
            "video_id": "OP5Gokb6BV8",
            "big_idea": "Rounding keeps numbers tidy, but the true value always lives inside a small range called its error interval.",
            "visual_example": "**A length is given as `4.7 cm` to 1 d.p. Find the error interval.**\n\n```\n     4.65 cm  ─── 4.70 cm ─── 4.75 cm\n      ▲           (given)        ▲\n   lower bound               upper bound\n     (≤ included)           (< NOT included)\n```\n\n**Error interval:** `4.65 ≤ length < 4.75`",
            "step_by_step": [
                "Decide the degree of accuracy (e.g. 1 d.p., nearest 10).",
                "Halve that degree — this is your ± value.",
                "Lower bound = given value − half (USE ≤).",
                "Upper bound = given value + half (USE <).",
                "Write: lower bound ≤ value < upper bound.",
            ],
        },
        "alg-1": {
            "video_id": "ZJA1qz4XovY",
            "big_idea": "Expanding multiplies everything in the bracket; factorising reverses this by pulling the common factor back OUT.",
            "visual_example": "**Expand and simplify `(x + 3)(x + 5)` using FOIL**\n\n```\n  (x + 3)(x + 5)\n   │   │  │   │\n   └───┼──┘   │   F: x × x   = x²\n       └──────┘   O: x × 5   = 5x\n   ┌───┼──────┐   I: 3 × x   = 3x\n   │   │      │   L: 3 × 5   = 15\n   └───┘\n\nx² + 5x + 3x + 15  =  x² + 8x + 15\n```",
            "step_by_step": [
                "Label the brackets: First, Outer, Inner, Last (FOIL).",
                "Multiply each FOIL pair carefully (watch the signs!).",
                "Write out all four terms.",
                "Collect like terms in the middle.",
                "Simplify into the form ax² + bx + c.",
            ],
        },
        "alg-2": {
            "video_id": "30S7WxKcPwg",
            "big_idea": "An equation is a balanced scale — whatever you do to one side, you MUST do to the other.",
            "visual_example": "**Solve `4(x + 2) = 3(x + 5)`**\n\n```\n    4(x + 2)  =  3(x + 5)\n     4x + 8   =  3x + 15      (expand)\n        x + 8 =  15            (subtract 3x)\n            x =  7             (subtract 8)\n\nCheck: 4(7+2) = 36 ✓   3(7+5) = 36 ✓\n```",
            "step_by_step": [
                "Expand any brackets on both sides.",
                "Collect x-terms on ONE side (subtract the smaller one).",
                "Move constants to the OTHER side.",
                "Divide both sides by the coefficient of x.",
                "Substitute back to check your answer works.",
            ],
        },
        "alg-3": {
            "video_id": "phlus4x0UqM",
            "big_idea": "Two equations + two unknowns = one unique solution point where the lines meet.",
            "visual_example": "**Solve `3x + 2y = 16` and `5x + 2y = 22` by elimination**\n\n```\n   5x + 2y = 22\n − (3x + 2y = 16)      ← SUBTRACT (same 2y cancels)\n ─────────────────\n   2x       = 6\n        x  = 3\n\nSub into eq1:  3(3) + 2y = 16\n                    2y   = 7\n                     y   = 3.5\n```",
            "step_by_step": [
                "Line the two equations up, one above the other.",
                "Make the coefficient of one variable match (multiply if needed).",
                "Same signs → SUBTRACT. Different signs → ADD.",
                "Solve the resulting single-variable equation.",
                "Substitute back into an original equation to find the second variable.",
            ],
        },
        "alg-4": {
            "video_id": "J9op5M4uUHg",
            "big_idea": "Linear sequences grow by a fixed step — spot the step and you own the whole pattern.",
            "visual_example": "**Find the nth term of `5, 9, 13, 17, …`**\n\n```\nTerms:        5   9  13  17\n              └─┬─┘└─┬─┘└─┬─┘\nDifferences:   +4   +4   +4    ← common difference d = 4\n\nnth term = dn + (a − d)\n         = 4n + (5 − 4)\n         = 4n + 1\n\nCheck: n=1 → 5 ✓   n=4 → 17 ✓\n```",
            "step_by_step": [
                "Find the common difference d between consecutive terms.",
                "Identify the first term a.",
                "Use the formula: nth term = dn + (a − d).",
                "Simplify the constant.",
                "Verify by plugging in n = 1, 2, 3.",
            ],
        },
        "alg-5": {
            "video_id": "wJ_tLEwEEi8",
            "big_idea": "Every quadratic equation has up to two solutions — factorise if you can, use the formula when you can't.",
            "visual_example": "**Solve `x² + 5x + 6 = 0` by factorising**\n\n```\nFind two numbers that:\n   × give +6  and  + give +5     →  +2 and +3\n\n   x² + 5x + 6 = 0\n  (x + 2)(x + 3) = 0\n\nEither  x + 2 = 0  →  x = −2\nOr      x + 3 = 0  →  x = −3\n```",
            "step_by_step": [
                "Make one side = 0 (standard form: ax² + bx + c = 0).",
                "Try to factorise into (x + p)(x + q) where p×q = c and p+q = b.",
                "Set each bracket equal to zero.",
                "Solve the two tiny linear equations.",
                "If it won't factorise, reach for the quadratic formula.",
            ],
        },
        "alg-6": {
            "video_id": "WdSXjD0bxI4",
            "big_idea": "Every straight line lives by the rule `y = mx + c` — m is the slope, c is where it crosses the y-axis.",
            "visual_example": "**Find the equation of the line through `(1, 3)` and `(4, 9)`**\n\n```\nGradient  m = (9 − 3) / (4 − 1) = 6 / 3 = 2\n\nUsing (1, 3):   y  = mx + c\n                3  = 2(1) + c\n                c  = 1\n\nEquation:   y = 2x + 1\n```",
            "step_by_step": [
                "Pick two points on the line (x₁, y₁) and (x₂, y₂).",
                "Gradient m = (y₂ − y₁) / (x₂ − x₁).",
                "Substitute m and one point into y = mx + c to find c.",
                "Write the full equation y = mx + c.",
                "Sanity check by plugging the other point back in.",
            ],
        },
        "rat-1": {
            "video_id": "cflZnf9H5l4",
            "big_idea": "A ratio splits a total into equal-sized 'parts' — find the value of ONE part and you've unlocked everything.",
            "visual_example": "**Share £240 in the ratio `3 : 5 : 4`**\n\n```\nTotal parts = 3 + 5 + 4 = 12\nOne part    = 240 ÷ 12 = £20\n\n  3 parts  →  3 × 20 = £60\n  5 parts  →  5 × 20 = £100\n  4 parts  →  4 × 20 = £80\n                       ─────\nCheck total            £240 ✓\n```",
            "step_by_step": [
                "Add all the parts of the ratio to get the TOTAL parts.",
                "Divide the total quantity by total parts → value of ONE part.",
                "Multiply each share of the ratio by 'one part'.",
                "Add your answers back up to double-check the total.",
                "State units (£, kg, cm, …) clearly.",
            ],
        },
        "rat-2": {
            "video_id": "LAArcKjVVaM",
            "big_idea": "Compound interest is interest that earns interest — multiply by (1 + r/100) once for every year.",
            "visual_example": "**£250,000 house grows by 5% per year. Worth after 3 years?**\n\n```\nMultiplier:  1 + 5/100 = 1.05\n\nValue = 250,000 × 1.05 × 1.05 × 1.05\n      = 250,000 × 1.05³\n      = 250,000 × 1.157625\n      = £289,406.25\n```",
            "step_by_step": [
                "Turn the rate into a multiplier: 1 + r/100 (or 1 − r/100 for decrease).",
                "Raise the multiplier to the power of the number of years.",
                "Multiply the original amount by that result.",
                "Round sensibly (usually 2 d.p. for money).",
                "Compare with simple interest to see the compounding effect.",
            ],
        },
        "rat-3": {
            "video_id": "dHVK7IeLGT8",
            "big_idea": "Speed, distance and time are locked in a triangle — cover the one you want, the formula is what's left.",
            "visual_example": "**A car travels 150 km in 2.5 hours. Find the average speed.**\n\n```\n       ┌─────┐\n       │  D  │       cover S → S = D / T\n       ├──┬──┤       cover D → D = S × T\n       │S │T │       cover T → T = D / S\n       └──┴──┘\n\nSpeed = Distance / Time\n      = 150 / 2.5\n      = 60 km/h\n```",
            "step_by_step": [
                "Identify which quantity you need to find.",
                "Cover that letter in the S/D/T triangle.",
                "The remaining letters give the formula.",
                "Check that units match (convert minutes to hours if needed).",
                "State your answer with the correct unit (km/h, m/s, mph).",
            ],
        },
        "geo-1": {
            "video_id": "gVo8ZrtlSp0",
            "big_idea": "Every polygon's interior angles add up to `(n − 2) × 180°` — the exterior angles ALWAYS total 360°.",
            "visual_example": "**Find the interior angle of a regular octagon (n = 8)**\n\n```\nMethod A — Interior:\n   Sum  = (8 − 2) × 180° = 1080°\n   Each = 1080° ÷ 8     = 135°\n\nMethod B — Exterior:\n   Each exterior = 360° ÷ 8 = 45°\n   Interior      = 180° − 45° = 135°\n```",
            "step_by_step": [
                "Count the number of sides, n.",
                "Sum of interior angles = (n − 2) × 180°.",
                "For REGULAR polygons, divide by n to find each interior angle.",
                "Alternative: each exterior angle = 360° ÷ n.",
                "Interior + exterior always = 180° at each vertex.",
            ],
        },
        "geo-2": {
            "video_id": "iWLVTy_rGjs",
            "big_idea": "In any right-angled triangle, `a² + b² = c²` — and SOHCAHTOA unlocks every angle and side beyond that.",
            "visual_example": "**Find the hypotenuse of a right triangle with legs 5 cm and 12 cm**\n\n```\n        │╲\n        │ ╲  c  (hypotenuse)\n     5  │  ╲\n        │   ╲\n        └────╲\n          12\n\nc² = 5² + 12² = 25 + 144 = 169\nc  = √169 = 13 cm\n```",
            "step_by_step": [
                "Label the triangle: Hypotenuse (opposite right angle), Opposite, Adjacent.",
                "Finding the longest side? Use c = √(a² + b²).",
                "Finding a shorter side? Use a = √(c² − b²).",
                "For angles or non-hypotenuse sides with an angle, switch to SOHCAHTOA.",
                "Always check the hypotenuse is the longest side in the answer.",
            ],
        },
        "geo-3": {
            "video_id": "Of8p1SfOcR0",
            "big_idea": "2D shapes have area (square units); 3D shapes have volume (cubic units) — match the formula to the shape.",
            "visual_example": "**Volume of a cylinder with r = 4 cm and h = 10 cm**\n\n```\n        ___________\n       /           \\       V = π r² × h\n      │     r=4     │       (area of circle × height)\n      │             │\n      │    h = 10   │       = π × 16 × 10\n      │             │       = 160π\n       \\___________/        ≈ 502.7 cm³\n```",
            "step_by_step": [
                "Identify the shape and pick the correct formula.",
                "List the dimensions you're given.",
                "Substitute carefully — watch powers (r² ≠ 2r).",
                "Keep π exact until the final step.",
                "Finish with the correct unit (cm², cm³, m², m³…).",
            ],
        },
        "geo-4": {
            "video_id": "fwv7e5OyuzA",
            "big_idea": "There are four ways to move a shape: translate, reflect, rotate, enlarge — each needs a FULL description.",
            "visual_example": "**Describe: triangle A shifted 3 right and 2 up gives triangle B**\n\n```\nIt's a TRANSLATION.\n\n         ┌ 3 ┐\nVector = │   │       (3 right, 2 up)\n         └ 2 ┘\n\nTranslation by the column vector ⎛3⎞\n                                 ⎝2⎠\n```",
            "step_by_step": [
                "Has size changed? → enlargement (give scale factor + centre).",
                "Has shape flipped? → reflection (give mirror line).",
                "Has shape turned? → rotation (give angle + direction + centre).",
                "Has shape slid? → translation (give column vector).",
                "State EVERYTHING the transformation requires — full marks hinge on it.",
            ],
        },
        "sta-1": {
            "video_id": "PYEvSuz1Dxo",
            "big_idea": "Probability lives between 0 and 1 — multiply along tree branches for 'AND', add separate paths for 'OR'.",
            "visual_example": "**A bag has 3 red, 5 blue and 2 green balls. Find P(not blue).**\n\n```\nTotal balls = 3 + 5 + 2 = 10\n\nP(blue)     = 5/10 = 1/2\nP(not blue) = 1 − 1/2 = 1/2\n\nOr directly:  P(not blue) = (3 + 2)/10 = 5/10 = 1/2\n```",
            "step_by_step": [
                "Count total outcomes.",
                "Count favourable outcomes.",
                "P(event) = favourable / total.",
                "P(not event) = 1 − P(event).",
                "For combined events, draw a tree diagram — multiply along, add between.",
            ],
        },
        "sta-2": {
            "video_id": "x8oPXIrLMc0",
            "big_idea": "Mean, median and mode tell three different stories — the range tells you how spread out the data is.",
            "visual_example": "**Find the mean, median and mode of: `4, 7, 2, 9, 3, 5, 8, 7`**\n\n```\nOrdered:  2, 3, 4, 5, 7, 7, 8, 9\n\nMean   = (2+3+4+5+7+7+8+9) ÷ 8 = 45 ÷ 8 = 5.625\nMedian = middle pair = (5 + 7) ÷ 2 = 6\nMode   = 7   (appears twice)\nRange  = 9 − 2 = 7\n```",
            "step_by_step": [
                "Mean: add all values, divide by how many.",
                "Median: put IN ORDER first, then pick the middle (or mean of middle pair).",
                "Mode: the most frequent value (can be none, one, or many).",
                "Range: largest − smallest (a measure of spread, NOT an average).",
                "For grouped data, use midpoints to estimate the mean.",
            ],
        },
        "num-5": {
            "video_id": "ndU_cCbPAm4",
            "big_idea": "A surd is an irrational square root kept in EXACT form — simplify by pulling out square factors.",
            "visual_example": "**Simplify `√72`**\n\n```\n72 = 36 × 2        (36 is the biggest square factor)\n\n√72 = √(36 × 2)\n    = √36 × √2\n    =   6 × √2\n    =  6√2\n```",
            "step_by_step": [
                "Find the largest SQUARE factor of the number inside the root.",
                "Split the surd: √(a × b) = √a × √b.",
                "Take the square root of the square factor.",
                "Leave the irrational part as a surd (don't decimalise).",
                "To rationalise a denominator, multiply top AND bottom by the surd.",
            ],
        },
        "num-6": {
            "video_id": "DNKqOTp7PDI",
            "big_idea": "Your calculator is a tool, not a magic wand — use brackets, memory and Ans to stay in control of the order of operations.",
            "visual_example": "**Calculate `16.9 / (105 × 0.625)` accurately**\n\n```\nPress:   ( 105 × 0.625 ) =        → 65.625\nPress:   16.9 ÷ Ans       =        → 0.2575...\n\nAlways put the denominator in BRACKETS first.\nRound at the END, not during the calculation.\n```",
            "step_by_step": [
                "Use brackets around any denominator or grouped expression.",
                "Use the Ans / memory button to carry full precision forward.",
                "For powers, use the xʸ button; for roots, the √ or ʸ√x button.",
                "Keep answers EXACT as long as possible; round only the final value.",
                "Know the fraction button — it keeps answers tidy and exam-ready.",
            ],
        },
        "alg-7": {
            "video_id": "aexvnpH-jhI",
            "big_idea": "Solve inequalities like equations — BUT flip the sign whenever you multiply or divide by a negative.",
            "visual_example": "**Solve `3x − 5 < 7` and show on a number line**\n\n```\n3x − 5  <  7\n   3x   <  12       (+5 to both sides)\n    x   <  4        (÷3 — sign stays)\n\n──────○═══►          (○ = NOT included because <)\n      4\n```",
            "step_by_step": [
                "Treat the inequality like an equation to start.",
                "Isolate x using +, −, × and ÷.",
                "If you multiply or divide by a NEGATIVE, FLIP the inequality sign.",
                "Show the answer on a number line: open ○ for <, >; closed ● for ≤, ≥.",
                "For double inequalities (a < x < b), do the same to ALL three parts.",
            ],
        },
        "alg-8": {
            "video_id": "eWP15jyatIo",
            "big_idea": "A function is a machine: put x in, get f(x) out — iteration feeds the output back in, again and again.",
            "visual_example": "**If `f(x) = 2x + 3`, find `f(5)` and iterate `xₙ₊₁ = (10 − xₙ) / 2` starting from x₀ = 4**\n\n```\nf(5)   = 2(5) + 3 = 13\n\nIteration:\nx₁ = (10 − 4) / 2 = 3\nx₂ = (10 − 3) / 2 = 3.5\nx₃ = (10 − 3.5) / 2 = 3.25\n...converging to x = 10/3 ≈ 3.333\n```",
            "step_by_step": [
                "Substitute carefully into f(x) — everywhere you see x, put the value in brackets.",
                "For composite f(g(x)): work INSIDE-OUT — do g first, feed result into f.",
                "For the inverse f⁻¹(x): swap x and y, then rearrange to make y the subject.",
                "For iteration, plug xₙ into the formula to get xₙ₊₁.",
                "Keep full calculator accuracy — round only at the very end.",
            ],
        },
        "alg-9": {
            "video_id": "pd9Q-e1JvtE",
            "big_idea": "To PROVE a statement, write any number with a variable (like n), manipulate algebraically, and show the result MUST be true.",
            "visual_example": "**Prove that the sum of 3 consecutive integers is always divisible by 3**\n\n```\nLet the three consecutive integers be   n,  n+1,  n+2\n\nSum  =  n + (n+1) + (n+2)\n     =  3n + 3\n     =  3(n + 1)\n\n3 × (any integer)  is  divisible by 3.      ∎\n```",
            "step_by_step": [
                "Choose smart algebraic expressions: n for any integer, 2n for even, 2n+1 for odd.",
                "Form the expression the question asks about.",
                "Expand, collect and factor out the relevant factor.",
                "State the conclusion clearly (e.g. '…therefore it is divisible by 3').",
                "End with QED or ∎ for a professional finish.",
            ],
        },
        "rat-4": {
            "video_id": "kcOwC7uqJNE",
            "big_idea": "Direct proportion: `y = kx`. Inverse proportion: `y = k/x`. Find `k` FIRST — everything else follows.",
            "visual_example": "**`y` is directly proportional to `x²`. When `x = 2`, `y = 20`. Find `y` when `x = 5`**\n\n```\ny ∝ x²   →   y = k x²\n\nSub values:  20 = k × 2²\n              20 = 4k\n               k = 5\n\nFormula:     y = 5x²\n\nWhen x = 5:  y = 5 × 25 = 125\n```",
            "step_by_step": [
                "Translate the words: ∝ becomes = k × (expression).",
                "Substitute the given pair to find the constant k.",
                "Write the complete formula y = k × (expression).",
                "Use the formula to answer the actual question.",
                "Check: direct → both increase; inverse → one up, the other down.",
            ],
        },
        "rat-5": {
            "video_id": "oUcjmGThMdc",
            "big_idea": "Growth/decay multiplies by the SAME factor each period — a rate above 1 grows, below 1 decays.",
            "visual_example": "**A car worth £12,000 depreciates by 15% per year. What's it worth after 4 years?**\n\n```\nMultiplier:  1 − 15/100  =  0.85\n\nValue =  12,000 × 0.85⁴\n      =  12,000 × 0.52200625\n      =  £6,264.08  (to 2 d.p.)\n```",
            "step_by_step": [
                "Identify the per-period rate and turn it into a multiplier.",
                "Growth: multiplier > 1 (e.g. +5% → 1.05).",
                "Decay: multiplier < 1 (e.g. −20% → 0.80).",
                "Raise the multiplier to the power of the number of periods.",
                "Multiply by the starting amount for the final value.",
            ],
        },
        "geo-5": {
            "video_id": "vgMSLsos7Ew",
            "big_idea": "Circle theorems give you FREE angles — spot the shape (radius, tangent, cyclic quad, semicircle…) and the rule names itself.",
            "visual_example": "**Key circle theorems at a glance**\n\n```\n• Angle at centre  =  2 × angle at circumference (same arc)\n• Angle in a semicircle  =  90°\n• Angles in same segment  are EQUAL\n• Opposite angles of a cyclic quadrilateral  sum to 180°\n• Tangent  ⟂  radius at point of contact\n• Two tangents from a point  are EQUAL length\n• Alternate segment: tangent-chord angle = angle in alternate segment\n```",
            "step_by_step": [
                "Mark the radius, centre, tangent or chord on the diagram.",
                "Spot the shape: semicircle? cyclic quadrilateral? same arc?",
                "Quote the theorem you are using BY NAME in your working.",
                "Apply the rule to find the unknown angle.",
                "Check everything adds up: triangles = 180°, quadrilaterals = 360°.",
            ],
        },
        "geo-6": {
            "video_id": "HA6gjFLm2Gk",
            "big_idea": "Congruent = identical twins (same size AND shape). Similar = stretched siblings (same shape, scaled size).",
            "visual_example": "**Scale factor for length, area and volume**\n\n```\nLinear scale factor:    k\nArea scale factor:      k²\nVolume scale factor:    k³\n\nExample: if two similar cylinders have lengths in ratio 2 : 3,\n   surface areas are in ratio  2² : 3²  =  4 : 9\n   volumes        are in ratio  2³ : 3³  =  8 : 27\n```",
            "step_by_step": [
                "Congruent tests: SSS, SAS, ASA, RHS — match sides/angles exactly.",
                "Similar shapes: all angles equal, all corresponding sides in the same ratio.",
                "Find the linear scale factor k = new length / old length.",
                "For area, use k²; for volume, use k³.",
                "State WHICH test of congruence/similarity you used.",
            ],
        },
        "geo-7": {
            "video_id": "h02d922Q5wk",
            "big_idea": "A vector has size AND direction — written as a column `(x, y)` meaning x across, y up.",
            "visual_example": "**If `a = (3, 1)` and `b = (−2, 4)`, find `2a + b`**\n\n```\n2a = 2 × ⎛3⎞  =  ⎛6⎞\n        ⎝1⎠     ⎝2⎠\n\n2a + b  =  ⎛6⎞ + ⎛−2⎞  =  ⎛4⎞\n           ⎝2⎠   ⎝ 4⎠     ⎝6⎠\n```",
            "step_by_step": [
                "Write each vector as a column ⎛x⎞ / ⎝y⎠.",
                "To add: add x-components, add y-components.",
                "To subtract: subtract component by component.",
                "To scale (ka): multiply each component by k.",
                "For geometrical proofs, work out the path using vector addition.",
            ],
        },
        "geo-8": {
            "video_id": "8Wja7Ct_XvY",
            "big_idea": "A bearing is an angle measured CLOCKWISE from NORTH — always written as three digits (e.g. 045°, 180°, 305°).",
            "visual_example": "**Point B is on a bearing of 060° from A, 8 km away. Describe it.**\n\n```\n       N\n       │\n       │ 60°\n       │ ╱\n       │╱────── B  (8 km away)\n       A\n\nBearings rules:\n  • measure CLOCKWISE from NORTH\n  • use THREE DIGITS (060° not 60°)\n  • back bearing = bearing ± 180°\n```",
            "step_by_step": [
                "Draw a north line at the starting point.",
                "Measure the angle CLOCKWISE from north to the target.",
                "Write the angle as three digits: 060°, 135°, 270°.",
                "For the return bearing, add or subtract 180°.",
                "For scale drawings, convert using the scale (e.g. 1 cm : 2 km).",
            ],
        },
        "sta-3": {
            "video_id": "PYEvSuz1Dxo",
            "big_idea": "Tree diagrams map every possible outcome — multiply ALONG branches for AND, add ACROSS paths for OR.",
            "visual_example": "**A bag has 4 red and 6 blue balls. Two are drawn WITHOUT replacement. P(both red)?**\n\n```\n            4/10 ── R\n           /         \\ 3/9 ── R\n          /           \\ 6/9 ── B\n  Start ─┤\n          \\ 6/10 ── B  / 4/9 ── R\n                      \\ 5/9 ── B\n\nP(R, R) = 4/10 × 3/9 = 12/90 = 2/15\n```",
            "step_by_step": [
                "Draw the first stage's branches with their probabilities.",
                "Attach the second stage's branches to EACH first-stage outcome.",
                "Remember: without replacement → probabilities change on stage 2.",
                "Multiply ALONG the branches for combined outcomes.",
                "Add the relevant PATHS for 'OR' questions.",
            ],
        },
        "sta-4": {
            "video_id": "wGzp-wM90EU",
            "big_idea": "Histograms use FREQUENCY DENSITY (not frequency) so unequal class widths compare fairly — cumulative frequency finds the median and quartiles.",
            "visual_example": "**Converting frequency to frequency density**\n\n```\n| Class width | Frequency | Frequency density (f ÷ width) |\n|-------------|-----------|-------------------------------|\n|    0 – 5    |     40    |         40 / 5  =  8          |\n|    5 – 10   |     35    |         35 / 5  =  7          |\n|   10 – 20   |     60    |         60 / 10 =  6          |\n|   20 – 45   |     55    |         55 / 25 =  2.2        |\n```",
            "step_by_step": [
                "For histograms, ALWAYS compute frequency density = frequency ÷ class width.",
                "Plot bars of height = frequency density (width varies).",
                "For cumulative frequency, add each frequency to the running total.",
                "Plot cumulative frequency at the UPPER bound of each class.",
                "Median ≈ value at cumulative frequency = n/2; quartiles at n/4 and 3n/4.",
            ],
        },
        "sta-5": {
            "video_id": "VUaOCgJTPjI",
            "big_idea": "A scatter graph shows relationships — the line of best fit lets you predict, but NEVER extrapolate wildly.",
            "visual_example": "**Types of correlation**\n\n```\n Positive           Negative            No correlation\n correlation        correlation         (random)\n      ●                    ●                 ●   ●\n    ●                        ●             ●       ●\n  ●                            ●             ●  ●\n●                                ●         ●       ●\n───────────►       ───────────►          ───────────►\n```",
            "step_by_step": [
                "Plot each (x, y) pair as a single point.",
                "Describe the pattern: positive / negative / none, strong / weak.",
                "Draw a line of best fit THROUGH the trend (not forced through the origin).",
                "Use it to estimate — beware of extrapolating beyond the data.",
                "Name an outlier: a point that clearly doesn't follow the trend.",
            ],
        },
    }

    # --- TOPICS ---
    topics_data = [
        # NUMBER
        {
            "id": "num-1", "category": "Number", "title": "Fractions, Decimals & Percentages",
            "slug": "fractions-decimals-percentages", "tier": "Both", "difficulty": 2, "order": 1,
            "description": "Convert between fractions, decimals and percentages. Master the relationships between these three forms.",
            "explanation": """## Fractions, Decimals & Percentages

These three are just **different ways of writing the same thing!** Think of them as three languages saying the same number.

### The Big Idea
- A **fraction** is a part of a whole: 1/2 means 1 out of 2 equal parts
- A **decimal** is a fraction written using place value: 0.5 means 5 tenths
- A **percentage** means 'out of 100': 50% means 50 out of 100

### Converting Between Them

**Fraction to Decimal:** Divide the top by the bottom
- 3/4 = 3 / 4 = 0.75

**Decimal to Percentage:** Multiply by 100
- 0.75 x 100 = 75%

**Percentage to Fraction:** Put over 100 and simplify
- 75% = 75/100 = 3/4

### Key Equivalents to Memorise
| Fraction | Decimal | Percentage |
|----------|---------|------------|
| 1/2 | 0.5 | 50% |
| 1/4 | 0.25 | 25% |
| 3/4 | 0.75 | 75% |
| 1/5 | 0.2 | 20% |
| 1/3 | 0.333... | 33.3% |
| 1/10 | 0.1 | 10% |""",
            "worked_examples": [
                {"problem": "Convert 3/8 to a decimal and percentage", "solution": "Step 1: 3 / 8 = 0.375\nStep 2: 0.375 x 100 = 37.5%\nAnswer: 3/8 = 0.375 = 37.5%"},
                {"problem": "Convert 65% to a fraction in its simplest form", "solution": "Step 1: 65% = 65/100\nStep 2: Find HCF of 65 and 100 = 5\nStep 3: 65/100 = 13/20\nAnswer: 13/20"},
            ],
            "key_points": [
                "To convert fraction to decimal: divide numerator by denominator",
                "To convert decimal to percentage: multiply by 100",
                "To convert percentage to fraction: write over 100 then simplify",
                "Learn the common equivalents by heart for speed in exams",
            ]
        },
        {
            "id": "num-2", "category": "Number", "title": "Powers, Roots & Standard Form",
            "slug": "powers-roots-standard-form", "tier": "Both", "difficulty": 3, "order": 2,
            "description": "Understand indices, square/cube roots, and how to use standard form for very large or small numbers.",
            "explanation": """## Powers, Roots & Standard Form

### Powers (Indices)
A power tells you how many times to multiply a number by itself.
- 2^3 = 2 x 2 x 2 = 8 (2 cubed)
- 5^2 = 5 x 5 = 25 (5 squared)

### Index Laws
These are your **cheat codes** for working with powers:
1. **Multiplying:** a^m x a^n = a^(m+n) - ADD the powers
2. **Dividing:** a^m / a^n = a^(m-n) - SUBTRACT the powers
3. **Power of a power:** (a^m)^n = a^(mn) - MULTIPLY the powers
4. **Anything to power 0:** a^0 = 1
5. **Negative power:** a^(-n) = 1/a^n

### Standard Form
Used for very big or very small numbers: A x 10^n where 1 <= A < 10

- 45,000,000 = 4.5 x 10^7
- 0.00032 = 3.2 x 10^(-4)

**Top tip:** Count how many places the decimal point moves!""",
            "worked_examples": [
                {"problem": "Simplify 2^3 x 2^5", "solution": "Using the multiplication rule: add the powers\n2^3 x 2^5 = 2^(3+5) = 2^8 = 256"},
                {"problem": "Write 0.000045 in standard form", "solution": "Step 1: Move decimal 5 places right to get 4.5\nStep 2: Since we moved right, power is negative\nAnswer: 4.5 x 10^(-5)"},
            ],
            "key_points": [
                "When multiplying same base: ADD the indices",
                "When dividing same base: SUBTRACT the indices",
                "Standard form: number between 1 and 10, multiplied by power of 10",
                "Negative indices mean reciprocals: 2^(-3) = 1/8",
            ]
        },
        {
            "id": "num-3", "category": "Number", "title": "HCF, LCM & Prime Factors",
            "slug": "hcf-lcm-prime-factors", "tier": "Both", "difficulty": 2, "order": 3,
            "description": "Find highest common factors, lowest common multiples, and express numbers as products of prime factors.",
            "explanation": """## HCF, LCM & Prime Factors

### Prime Numbers
A prime number has exactly **2 factors**: 1 and itself.
First few primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...

### Prime Factor Decomposition
Breaking a number into a product of primes using a factor tree.

Example: 60 = 2 x 2 x 3 x 5 = 2^2 x 3 x 5

### HCF (Highest Common Factor)
The **largest** number that divides into both numbers.
Method: List prime factors, multiply the **common** ones.

### LCM (Lowest Common Multiple)
The **smallest** number both numbers divide into.
Method: List prime factors, multiply the **highest power** of each.

### Example: Find HCF and LCM of 12 and 18
- 12 = 2^2 x 3
- 18 = 2 x 3^2
- HCF = 2 x 3 = 6 (common factors, lowest powers)
- LCM = 2^2 x 3^2 = 36 (all factors, highest powers)""",
            "worked_examples": [
                {"problem": "Find the HCF and LCM of 24 and 36", "solution": "Step 1: Prime factorise\n24 = 2^3 x 3\n36 = 2^2 x 3^2\nStep 2: HCF = 2^2 x 3 = 12 (lowest powers of shared primes)\nStep 3: LCM = 2^3 x 3^2 = 72 (highest powers of all primes)"},
            ],
            "key_points": [
                "Use factor trees to find prime factors",
                "HCF: multiply common primes with LOWEST powers",
                "LCM: multiply ALL primes with HIGHEST powers",
                "HCF x LCM = product of the two numbers",
            ]
        },
        {
            "id": "num-4", "category": "Number", "title": "Rounding, Estimation & Bounds",
            "slug": "rounding-estimation-bounds", "tier": "Both", "difficulty": 2, "order": 4,
            "description": "Round numbers, make estimates for calculations, and understand upper and lower bounds.",
            "explanation": """## Rounding, Estimation & Bounds

### Rounding Rules
Look at the digit AFTER the one you're rounding to:
- If it's 5 or more, round UP
- If it's 4 or less, round DOWN

### Significant Figures
Count from the first non-zero digit:
- 3.456 to 2 s.f. = 3.5
- 0.00347 to 2 s.f. = 0.0035

### Estimation
Round each number to 1 significant figure, then calculate.
Example: 4.8 x 21.3 is approximately 5 x 20 = 100

### Error Intervals (Bounds)
When a number is rounded, there's a range of values it could actually be.
If x = 3.5 rounded to 1 d.p.: 3.45 <= x < 3.55

**Exam tip:** The lower bound is always included (<=) but the upper bound is NOT included (<).""",
            "worked_examples": [
                {"problem": "A length is 4.7 cm to 1 d.p. Find the error interval", "solution": "The value was rounded to 1 decimal place.\nLower bound = 4.65 cm\nUpper bound = 4.75 cm\nError interval: 4.65 <= length < 4.75"},
            ],
            "key_points": [
                "For estimation, round to 1 significant figure",
                "Lower bound: subtract half the degree of accuracy",
                "Upper bound: add half the degree of accuracy",
                "Upper bound uses < (strict inequality), lower uses <=",
            ]
        },
        # ALGEBRA
        {
            "id": "alg-1", "category": "Algebra", "title": "Expanding & Factorising Brackets",
            "slug": "expanding-factorising", "tier": "Both", "difficulty": 2, "order": 10,
            "description": "Master expanding single and double brackets, and factorising expressions including quadratics.",
            "explanation": """## Expanding & Factorising Brackets

### Expanding Single Brackets
Multiply everything INSIDE the bracket by the term OUTSIDE.

3(x + 4) = 3x + 12
-2(3y - 5) = -6y + 10

### Expanding Double Brackets (FOIL)
**F**irst, **O**uter, **I**nner, **L**ast

(x + 3)(x + 5)
= x^2 + 5x + 3x + 15
= x^2 + 8x + 15

### Factorising (the reverse!)
Take out the **common factor**:
6x + 12 = 6(x + 2)

### Factorising Quadratics
x^2 + 8x + 15 = (x + 3)(x + 5)

**Method:** Find two numbers that:
- MULTIPLY to give the last number (15)
- ADD to give the middle number (8)
- Answer: 3 and 5!

### Difference of Two Squares
a^2 - b^2 = (a + b)(a - b)
x^2 - 49 = (x + 7)(x - 7)""",
            "worked_examples": [
                {"problem": "Expand and simplify (2x + 3)(x - 4)", "solution": "F: 2x times x = 2x^2\nO: 2x times -4 = -8x\nI: 3 times x = 3x\nL: 3 times -4 = -12\nCombine: 2x^2 - 8x + 3x - 12\nSimplify: 2x^2 - 5x - 12"},
                {"problem": "Factorise x^2 - 5x - 14", "solution": "Find two numbers that multiply to -14 and add to -5\nFactors of -14: (-7, 2), (7, -2)...\n-7 + 2 = -5 (that's it!)\nAnswer: (x - 7)(x + 2)"},
            ],
            "key_points": [
                "Expanding: multiply each term inside by the term outside",
                "FOIL for double brackets: First, Outer, Inner, Last",
                "Factorising is the REVERSE of expanding",
                "For quadratics: find two numbers that multiply AND add correctly",
            ]
        },
        {
            "id": "alg-2", "category": "Algebra", "title": "Solving Linear Equations",
            "slug": "linear-equations", "tier": "Both", "difficulty": 2, "order": 11,
            "description": "Solve equations with one unknown, including those with brackets and unknowns on both sides.",
            "explanation": """## Solving Linear Equations

### The Golden Rule
Whatever you do to one side, you MUST do to the other side!
Think of it like a balance scale - keep it balanced!

### Simple Equations
3x + 5 = 20
3x = 20 - 5 = 15
x = 15 / 3 = 5

### Equations with Brackets
2(3x - 1) = 16
6x - 2 = 16 (expand first)
6x = 18
x = 3

### Unknowns on Both Sides
5x + 3 = 2x + 15
5x - 2x = 15 - 3 (collect like terms)
3x = 12
x = 4

### Step-by-Step Method
1. Expand any brackets
2. Collect x terms on one side
3. Collect number terms on the other
4. Divide to find x
5. CHECK by substituting back in!""",
            "worked_examples": [
                {"problem": "Solve 4(x + 2) = 3(x + 5)", "solution": "Step 1: Expand brackets\n4x + 8 = 3x + 15\nStep 2: Subtract 3x from both sides\nx + 8 = 15\nStep 3: Subtract 8 from both sides\nx = 7\nCheck: 4(7+2) = 4(9) = 36, 3(7+5) = 3(12) = 36 (correct!)"},
            ],
            "key_points": [
                "Always do the same operation to both sides",
                "Expand brackets before collecting terms",
                "Get all x terms on one side, numbers on the other",
                "Always check your answer by substituting back",
            ]
        },
        {
            "id": "alg-3", "category": "Algebra", "title": "Simultaneous Equations",
            "slug": "simultaneous-equations", "tier": "Both", "difficulty": 3, "order": 12,
            "description": "Solve pairs of equations with two unknowns using elimination and substitution methods.",
            "explanation": """## Simultaneous Equations

Two equations, two unknowns - we need BOTH methods!

### Method 1: Elimination
Make the coefficients of one variable the same, then add or subtract.

Example: 2x + 3y = 12 and 4x - 3y = 6
The y terms are +3y and -3y, so ADD the equations:
6x = 18, so x = 3
Substitute back: 2(3) + 3y = 12, 3y = 6, y = 2

### Method 2: Substitution
Rearrange one equation to make x or y the subject, then substitute.

Example: y = 2x + 1 and 3x + 2y = 12
Substitute: 3x + 2(2x + 1) = 12
3x + 4x + 2 = 12
7x = 10
x = 10/7

### When to Use Which?
- **Elimination:** when coefficients match up nicely
- **Substitution:** when one equation already has x= or y=""",
            "worked_examples": [
                {"problem": "Solve: 3x + 2y = 16 and 5x + 2y = 22", "solution": "Step 1: Same y coefficient, so SUBTRACT\n(5x + 2y) - (3x + 2y) = 22 - 16\n2x = 6\nx = 3\nStep 2: Sub x=3 into equation 1\n3(3) + 2y = 16\n9 + 2y = 16\n2y = 7\ny = 3.5\nAnswer: x = 3, y = 3.5"},
            ],
            "key_points": [
                "You need as many equations as unknowns",
                "Elimination: make coefficients equal, then add/subtract",
                "Substitution: rearrange one equation, plug into the other",
                "Always check answers in BOTH original equations",
            ]
        },
        {
            "id": "alg-4", "category": "Algebra", "title": "Sequences & nth Term",
            "slug": "sequences-nth-term", "tier": "Both", "difficulty": 2, "order": 13,
            "description": "Find patterns in sequences, determine the nth term rule for linear and quadratic sequences.",
            "explanation": """## Sequences & nth Term

### Arithmetic (Linear) Sequences
The difference between terms is CONSTANT.
3, 7, 11, 15, 19... (common difference = 4)

### Finding the nth Term (Linear)
nth term = dn + (a - d)
where d = common difference, a = first term

Example: 3, 7, 11, 15...
d = 4, a = 3
nth term = 4n + (3 - 4) = 4n - 1

**Quick check:** n=1: 4(1)-1 = 3 (first term - correct!)

### Quadratic Sequences (Higher)
The SECOND difference is constant.
1, 4, 9, 16, 25... (differences: 3, 5, 7, 9... second diff = 2)

If second difference = 2, starts with n^2
If second difference = 6, starts with 3n^2

### Geometric Sequences
Each term is multiplied by a constant ratio.
2, 6, 18, 54... (common ratio = 3)
nth term = a x r^(n-1)""",
            "worked_examples": [
                {"problem": "Find the nth term of: 5, 9, 13, 17...", "solution": "Step 1: Common difference d = 9 - 5 = 4\nStep 2: nth term = dn + (a - d) = 4n + (5 - 4) = 4n + 1\nCheck: n=1: 4(1)+1 = 5, n=2: 4(2)+1 = 9, n=3: 4(3)+1 = 13\nAnswer: 4n + 1"},
            ],
            "key_points": [
                "Arithmetic: constant first difference",
                "nth term of linear sequence: dn + (a - d)",
                "Quadratic: constant second difference",
                "Always check by substituting n = 1, 2, 3",
            ]
        },
        # RATIO & PROPORTION
        {
            "id": "rat-1", "category": "Ratio & Proportion", "title": "Ratio & Proportion",
            "slug": "ratio-proportion", "tier": "Both", "difficulty": 2, "order": 20,
            "description": "Simplify ratios, share amounts in a given ratio, and solve proportion problems.",
            "explanation": """## Ratio & Proportion

### What is a Ratio?
A ratio compares quantities of the SAME type.
If there are 3 boys and 5 girls: ratio = 3:5

### Simplifying Ratios
Divide both parts by their HCF.
12:18 = 2:3 (divided by 6)

### Sharing in a Ratio
Example: Share 120 in the ratio 2:3
1. Total parts = 2 + 3 = 5
2. One part = 120 / 5 = 24
3. First share = 2 x 24 = 48
4. Second share = 3 x 24 = 72

### Direct Proportion
If one quantity increases, the other increases at the same rate.
y = kx (k is the constant of proportionality)

### Inverse Proportion
If one increases, the other decreases.
y = k/x

### Speed, Distance, Time
Speed = Distance / Time
Remember the triangle: D on top, S and T on bottom.""",
            "worked_examples": [
                {"problem": "Share 240 in the ratio 3:5:4", "solution": "Step 1: Total parts = 3 + 5 + 4 = 12\nStep 2: One part = 240 / 12 = 20\nStep 3: First = 3 x 20 = 60\nSecond = 5 x 20 = 100\nThird = 4 x 20 = 80\nCheck: 60 + 100 + 80 = 240"},
            ],
            "key_points": [
                "Ratios compare quantities of the same type",
                "To share in a ratio: find total parts first, then multiply",
                "Direct proportion: y = kx (graph is straight line through origin)",
                "Inverse proportion: y = k/x (graph is a curve)",
            ]
        },
        {
            "id": "rat-2", "category": "Ratio & Proportion", "title": "Percentages & Interest",
            "slug": "percentages-interest", "tier": "Both", "difficulty": 2, "order": 21,
            "description": "Calculate percentage increase/decrease, find original values, and understand compound interest.",
            "explanation": """## Percentages & Interest

### Percentage of an Amount
Find 15% of 240:
Method 1: 0.15 x 240 = 36
Method 2: 10% = 24, 5% = 12, so 15% = 36

### Percentage Change
% change = (change / original) x 100

### Percentage Multipliers (the fast way!)
- Increase by 20%: multiply by 1.20
- Decrease by 15%: multiply by 0.85
- VAT of 20%: multiply by 1.20

### Reverse Percentages
A coat costs 68 after a 15% reduction. Original price?
68 = 0.85 x original
Original = 68 / 0.85 = 80

### Compound Interest
Amount = P(1 + r/100)^n
P = principal, r = rate, n = years

Example: 500 at 3% for 4 years
= 500 x 1.03^4 = 562.75""",
            "worked_examples": [
                {"problem": "A house valued at 250,000 increases by 5% each year. What is it worth after 3 years?", "solution": "Using compound interest:\nAmount = 250,000 x (1.05)^3\n= 250,000 x 1.157625\n= 289,406.25\nThe house is worth 289,406.25 after 3 years"},
            ],
            "key_points": [
                "Use multipliers for speed: 1 + rate for increase, 1 - rate for decrease",
                "Reverse percentage: divide by the multiplier to find original",
                "Compound interest: multiply by (1 + r/100) each year",
                "Simple interest: same amount added each year",
            ]
        },
        # GEOMETRY
        {
            "id": "geo-1", "category": "Geometry & Measures", "title": "Angles & Polygons",
            "slug": "angles-polygons", "tier": "Both", "difficulty": 2, "order": 30,
            "description": "Understand angle rules, interior/exterior angles of polygons, and parallel line theorems.",
            "explanation": """## Angles & Polygons

### Basic Angle Facts
- Angles on a straight line = 180 degrees
- Angles around a point = 360 degrees
- Vertically opposite angles are EQUAL
- Angles in a triangle = 180 degrees
- Angles in a quadrilateral = 360 degrees

### Parallel Lines
When a line crosses two parallel lines:
- **Alternate angles** (Z-shape) are equal
- **Corresponding angles** (F-shape) are equal
- **Co-interior angles** (C/U-shape) add up to 180 degrees

### Interior Angles of a Polygon
Sum of interior angles = (n - 2) x 180 degrees
- Triangle: (3-2) x 180 = 180 degrees
- Hexagon: (6-2) x 180 = 720 degrees

### Exterior Angles
- Exterior angles ALWAYS sum to 360 degrees
- Each exterior angle of a regular polygon = 360/n
- Interior + Exterior = 180 degrees

### Regular Polygons
All sides equal, all angles equal.
A regular pentagon: interior angle = 108 degrees""",
            "worked_examples": [
                {"problem": "Find the interior angle of a regular octagon", "solution": "Step 1: Sum of interior angles = (8-2) x 180 = 1080 degrees\nStep 2: Each interior angle = 1080 / 8 = 135 degrees\nAlternative: Exterior angle = 360/8 = 45 degrees\nInterior = 180 - 45 = 135 degrees"},
            ],
            "key_points": [
                "Sum of interior angles = (n-2) x 180",
                "Exterior angles always sum to 360",
                "Look for Z (alternate), F (corresponding), C (co-interior) shapes",
                "Regular polygon: each angle = (n-2) x 180 / n",
            ]
        },
        {
            "id": "geo-2", "category": "Geometry & Measures", "title": "Pythagoras' Theorem & Trigonometry",
            "slug": "pythagoras-trigonometry", "tier": "Both", "difficulty": 3, "order": 31,
            "description": "Use Pythagoras' theorem for right-angled triangles and SOHCAHTOA for trigonometric ratios.",
            "explanation": """## Pythagoras' Theorem & Trigonometry

### Pythagoras' Theorem
For right-angled triangles: **a^2 + b^2 = c^2**
where c is the HYPOTENUSE (longest side, opposite the right angle).

Finding the hypotenuse: c = sqrt(a^2 + b^2)
Finding a shorter side: a = sqrt(c^2 - b^2)

### SOHCAHTOA
The memory trick for trigonometry:
- **S**in = **O**pposite / **H**ypotenuse
- **C**os = **A**djacent / **H**ypotenuse
- **T**an = **O**pposite / **A**djacent

### Labelling the Triangle
1. **Hypotenuse:** opposite the right angle (always the longest)
2. **Opposite:** opposite the angle you're using
3. **Adjacent:** next to the angle you're using

### Finding an Angle
Use inverse trig: angle = sin^(-1), cos^(-1), or tan^(-1)

### Finding a Side
Rearrange the formula:
- If you have angle + hypotenuse, use sin or cos
- If you have angle + one other side, pick the right ratio""",
            "worked_examples": [
                {"problem": "A right triangle has sides 5 cm and 12 cm. Find the hypotenuse.", "solution": "Using Pythagoras: c^2 = a^2 + b^2\nc^2 = 5^2 + 12^2 = 25 + 144 = 169\nc = sqrt(169) = 13 cm"},
                {"problem": "Find angle x if opposite = 7 and hypotenuse = 10", "solution": "We have Opposite and Hypotenuse: use SOH\nsin(x) = 7/10 = 0.7\nx = sin^(-1)(0.7) = 44.4 degrees"},
            ],
            "key_points": [
                "Pythagoras: a^2 + b^2 = c^2 (c is hypotenuse)",
                "SOHCAHTOA: Sin=O/H, Cos=A/H, Tan=O/A",
                "Label your triangle first: Hypotenuse, Opposite, Adjacent",
                "Always check: does your answer make sense? Hypotenuse is always longest",
            ]
        },
        {
            "id": "geo-3", "category": "Geometry & Measures", "title": "Area, Perimeter & Volume",
            "slug": "area-perimeter-volume", "tier": "Both", "difficulty": 2, "order": 32,
            "description": "Calculate areas of 2D shapes, perimeters, and volumes of 3D solids including prisms and cylinders.",
            "explanation": """## Area, Perimeter & Volume

### 2D Shapes - Area
- **Rectangle:** l x w
- **Triangle:** 1/2 x base x height
- **Parallelogram:** base x height
- **Trapezium:** 1/2 x (a + b) x h
- **Circle:** pi x r^2

### 2D Shapes - Perimeter
Add up all the outer edges.
**Circle (circumference):** 2 x pi x r or pi x d

### 3D Shapes - Volume
- **Cuboid:** l x w x h
- **Prism:** area of cross-section x length
- **Cylinder:** pi x r^2 x h
- **Cone:** 1/3 x pi x r^2 x h
- **Sphere:** 4/3 x pi x r^3

### Surface Area
Sum of all the faces.
- **Cylinder:** 2 x pi x r^2 + 2 x pi x r x h
- **Sphere:** 4 x pi x r^2

### Units
Area: cm^2, m^2 (square units)
Volume: cm^3, m^3 (cubic units)""",
            "worked_examples": [
                {"problem": "Find the volume of a cylinder with radius 4 cm and height 10 cm", "solution": "Volume = pi x r^2 x h\n= pi x 4^2 x 10\n= pi x 16 x 10\n= 160 x pi\n= 502.7 cm^3 (1 d.p.)"},
            ],
            "key_points": [
                "Always check units and convert if needed",
                "Prism volume = cross-section area x length",
                "Don't confuse radius and diameter",
                "Leave answers in terms of pi unless told otherwise",
            ]
        },
        # PROBABILITY & STATISTICS
        {
            "id": "sta-1", "category": "Probability & Statistics", "title": "Probability Basics",
            "slug": "probability-basics", "tier": "Both", "difficulty": 2, "order": 40,
            "description": "Understand probability scales, calculate theoretical and experimental probabilities, and use probability diagrams.",
            "explanation": """## Probability Basics

### The Probability Scale
- Impossible = 0
- Certain = 1
- Everything else is between 0 and 1

P(event) = number of favourable outcomes / total number of outcomes

### Key Rules
1. P(something NOT happening) = 1 - P(it happening)
2. P(A or B) = P(A) + P(B) - P(A and B)
3. For mutually exclusive events: P(A or B) = P(A) + P(B)

### Expected Frequency
Expected = probability x number of trials
If P(heads) = 0.5 and you flip 100 times: expected heads = 50

### Relative Frequency
Estimated probability from experiments:
Relative frequency = frequency / total trials

### Tree Diagrams
- Branches show each outcome
- Multiply along branches for 'AND'
- Add different paths for 'OR'
- Probabilities on each set of branches add up to 1

### Venn Diagrams
- Circles represent events
- Overlap shows both events occurring
- Outside circles: neither event""",
            "worked_examples": [
                {"problem": "A bag has 3 red, 5 blue, and 2 green balls. Find P(not blue)", "solution": "Total balls = 3 + 5 + 2 = 10\nP(blue) = 5/10 = 1/2\nP(not blue) = 1 - 1/2 = 1/2\nOR directly: P(not blue) = (3+2)/10 = 5/10 = 1/2"},
            ],
            "key_points": [
                "Probability is always between 0 and 1",
                "All probabilities for an event must add to 1",
                "Tree diagrams: multiply along, add between paths",
                "Expected frequency = probability x number of trials",
            ]
        },
        {
            "id": "sta-2", "category": "Probability & Statistics", "title": "Averages & Representing Data",
            "slug": "averages-data", "tier": "Both", "difficulty": 2, "order": 41,
            "description": "Calculate mean, median, mode and range. Represent data using various charts and graphs.",
            "explanation": """## Averages & Representing Data

### The Three Averages + Range
- **Mean:** Add all values, divide by how many
- **Median:** Middle value when in ORDER
- **Mode:** Most COMMON value
- **Range:** Largest - Smallest (measures spread, NOT an average)

### Mean from a Frequency Table
Mean = sum of (value x frequency) / total frequency

### Median from a Frequency Table
Find the middle value using cumulative frequency.
If n values: median is the (n+1)/2 th value.

### Grouped Data
Use MIDPOINTS for estimated mean.
Cannot find exact mode or median - use modal class and class containing median.

### Data Representation
- **Bar chart:** comparing categories
- **Pie chart:** showing proportions (angles add to 360)
- **Scatter graph:** showing correlation between two variables
- **Histogram:** frequency density (not frequency!) on y-axis
- **Cumulative frequency:** find median and quartiles
- **Box plot:** shows median, quartiles, min, max""",
            "worked_examples": [
                {"problem": "Find the mean of: 4, 7, 2, 9, 3, 5, 8", "solution": "Step 1: Add all values\n4 + 7 + 2 + 9 + 3 + 5 + 8 = 38\nStep 2: Divide by how many values\n38 / 7 = 5.43 (2 d.p.)\nMean = 5.43"},
            ],
            "key_points": [
                "Median: put in ORDER first, then find middle",
                "Mode: most frequent (can have no mode or multiple modes)",
                "Mean is affected by outliers; median is not",
                "For grouped data, use midpoints for estimated mean",
            ]
        },
        {
            "id": "alg-5", "category": "Algebra", "title": "Solving Quadratic Equations",
            "slug": "quadratic-equations", "tier": "Both", "difficulty": 3, "order": 14,
            "description": "Solve quadratics by factorising, using the formula, and completing the square.",
            "explanation": """## Solving Quadratic Equations

A quadratic equation has the form: ax^2 + bx + c = 0

### Method 1: Factorising
x^2 + 5x + 6 = 0
(x + 2)(x + 3) = 0
x = -2 or x = -3

### Method 2: The Quadratic Formula
x = (-b +/- sqrt(b^2 - 4ac)) / 2a

This works for ALL quadratics, even when factorising is hard.

### Method 3: Completing the Square (Higher)
x^2 + 6x + 2 = 0
(x + 3)^2 - 9 + 2 = 0
(x + 3)^2 = 7
x = -3 +/- sqrt(7)

### The Discriminant
b^2 - 4ac tells you how many solutions:
- Positive: 2 real solutions
- Zero: 1 repeated solution
- Negative: no real solutions

### Top Tip
Always check if you can factorise first - it's quicker!
If the question says "give to 2 d.p.", use the formula.""",
            "worked_examples": [
                {"problem": "Solve 2x^2 + 5x - 3 = 0", "solution": "Using the quadratic formula:\na = 2, b = 5, c = -3\nx = (-5 +/- sqrt(25 + 24)) / 4\nx = (-5 +/- sqrt(49)) / 4\nx = (-5 +/- 7) / 4\nx = 2/4 = 0.5 or x = -12/4 = -3"},
            ],
            "key_points": [
                "Always try factorising first",
                "Use the formula when factorising is difficult",
                "The discriminant tells you the number of solutions",
                "Completing the square: halve the coefficient of x",
            ]
        },
        {
            "id": "geo-4", "category": "Geometry & Measures", "title": "Transformations",
            "slug": "transformations", "tier": "Both", "difficulty": 2, "order": 33,
            "description": "Understand and perform translations, reflections, rotations and enlargements.",
            "explanation": """## Transformations

### 4 Types of Transformation

**1. Translation** - sliding a shape
Described by a column vector: (x, y) where x = right, y = up
Negative x = left, negative y = down

**2. Reflection** - flipping a shape
State the **line of reflection** (mirror line)
Common lines: x-axis, y-axis, y = x, y = -x, x = 2, etc.

**3. Rotation** - turning a shape
State: **angle**, **direction** (clockwise/anticlockwise), **centre of rotation**
Use tracing paper in the exam!

**4. Enlargement** - making bigger or smaller
State: **scale factor** and **centre of enlargement**
- Scale factor > 1: shape gets bigger
- Scale factor between 0 and 1: shape gets smaller
- Negative scale factor: shape is inverted

### Key Points for Exams
When DESCRIBING a transformation, you MUST state ALL required information:
- Translation: the vector
- Reflection: the mirror line
- Rotation: angle + direction + centre
- Enlargement: scale factor + centre""",
            "worked_examples": [
                {"problem": "Describe the single transformation that maps triangle A to triangle B (moved 3 right and 2 up)", "solution": "This is a Translation by the vector (3, 2)\nAlways check: has the shape changed size? No = not enlargement\nIs it flipped? No = not reflection\nHas it turned? No = not rotation\nSo it must be a translation!"},
            ],
            "key_points": [
                "Translation: column vector only",
                "Reflection: MUST state the mirror line",
                "Rotation: MUST state angle, direction AND centre",
                "Enlargement: MUST state scale factor AND centre",
            ]
        },
        {
            "id": "rat-3", "category": "Ratio & Proportion", "title": "Speed, Distance & Time",
            "slug": "speed-distance-time", "tier": "Both", "difficulty": 2, "order": 22,
            "description": "Calculate speed, distance and time. Understand compound measures and unit conversions.",
            "explanation": """## Speed, Distance & Time

### The Triangle
```
    D
  -----
  S | T
```
- Speed = Distance / Time
- Distance = Speed x Time
- Time = Distance / Speed

### Units
- Speed: km/h, m/s, mph
- Distance: km, m, miles
- Time: hours, minutes, seconds

### Converting Units
km/h to m/s: divide by 3.6
m/s to km/h: multiply by 3.6

### Other Compound Measures
- **Density** = Mass / Volume (g/cm^3)
- **Pressure** = Force / Area (N/m^2)
- **Population density** = Population / Area

### Real-Life Graphs
Distance-time graphs:
- Horizontal line = stationary
- Steeper line = faster speed
- Gradient = speed""",
            "worked_examples": [
                {"problem": "A car travels 150 km in 2.5 hours. Find the average speed.", "solution": "Speed = Distance / Time\nSpeed = 150 / 2.5\nSpeed = 60 km/h"},
            ],
            "key_points": [
                "Cover the quantity you want in the triangle to find the formula",
                "Make sure units are consistent before calculating",
                "Average speed = total distance / total time",
                "On a distance-time graph, gradient = speed",
            ]
        },
        {
            "id": "alg-6", "category": "Algebra", "title": "Linear Graphs",
            "slug": "linear-graphs", "tier": "Both", "difficulty": 2, "order": 15,
            "description": "Plot and interpret straight line graphs, find gradients and y-intercepts, use y = mx + c.",
            "explanation": """## Linear Graphs (y = mx + c)

### The Equation of a Line
y = mx + c where:
- **m** = gradient (steepness)
- **c** = y-intercept (where it crosses the y-axis)

### Finding the Gradient
Gradient = rise / run = change in y / change in x

Pick two points on the line and calculate:
m = (y2 - y1) / (x2 - x1)

Positive gradient: line goes UP from left to right
Negative gradient: line goes DOWN from left to right

### Plotting a Line
1. Find the y-intercept (set x = 0)
2. Use the gradient to find more points
3. Or find 3 points by substituting x values

### Parallel & Perpendicular Lines
- **Parallel lines** have the SAME gradient
- **Perpendicular lines**: gradients multiply to -1
  m1 x m2 = -1

Example: If a line has gradient 2, the perpendicular gradient is -1/2""",
            "worked_examples": [
                {"problem": "Find the equation of a line through (1, 3) and (4, 9)", "solution": "Step 1: Gradient = (9-3)/(4-1) = 6/3 = 2\nStep 2: Use y = mx + c with point (1,3)\n3 = 2(1) + c\nc = 1\nEquation: y = 2x + 1"},
            ],
            "key_points": [
                "m is the gradient (slope), c is the y-intercept",
                "Parallel lines: same gradient, different intercept",
                "Perpendicular: gradients multiply to give -1",
                "Horizontal lines: y = constant, Vertical lines: x = constant",
            ]
        },
    ]

    # Insert topics (with guided-journey enrichments merged in)
    for topic in topics_data:
        enrich = enrichments.get(topic["id"], {})
        topic.update(enrich)
        await db.topics.insert_one(topic)

    # --- QUIZ QUESTIONS ---
    quiz_data = [
        # Fractions quiz
        {"id": "q-num1-1", "topic_id": "num-1", "topic_title": "Fractions, Decimals & Percentages", "question": "Convert 3/5 to a percentage.", "options": ["30%", "50%", "60%", "65%"], "correct_answer": 2, "explanation": "3/5 = 3 divided by 5 = 0.6. Then 0.6 x 100 = 60%", "difficulty": 1},
        {"id": "q-num1-2", "topic_id": "num-1", "topic_title": "Fractions, Decimals & Percentages", "question": "What is 0.375 as a fraction in simplest form?", "options": ["3/8", "375/100", "3/4", "37/100"], "correct_answer": 0, "explanation": "0.375 = 375/1000. Simplify by dividing by 125: 375/1000 = 3/8", "difficulty": 2},
        {"id": "q-num1-3", "topic_id": "num-1", "topic_title": "Fractions, Decimals & Percentages", "question": "Which is the largest: 2/3, 0.65, or 60%?", "options": ["2/3", "0.65", "60%", "They are all equal"], "correct_answer": 0, "explanation": "2/3 = 0.667, 0.65, 60% = 0.6. So 2/3 (0.667) is the largest.", "difficulty": 2},
        # Powers quiz
        {"id": "q-num2-1", "topic_id": "num-2", "topic_title": "Powers, Roots & Standard Form", "question": "Simplify 3^2 x 3^4", "options": ["3^6", "3^8", "9^6", "3^2"], "correct_answer": 0, "explanation": "When multiplying with the same base, ADD the powers: 3^(2+4) = 3^6", "difficulty": 1},
        {"id": "q-num2-2", "topic_id": "num-2", "topic_title": "Powers, Roots & Standard Form", "question": "Write 45,000 in standard form.", "options": ["4.5 x 10^3", "4.5 x 10^4", "45 x 10^3", "0.45 x 10^5"], "correct_answer": 1, "explanation": "45,000 = 4.5 x 10,000 = 4.5 x 10^4. Remember: first number must be between 1 and 10.", "difficulty": 1},
        # HCF LCM quiz
        {"id": "q-num3-1", "topic_id": "num-3", "topic_title": "HCF, LCM & Prime Factors", "question": "What is the HCF of 24 and 36?", "options": ["6", "8", "12", "72"], "correct_answer": 2, "explanation": "24 = 2^3 x 3, 36 = 2^2 x 3^2. HCF = 2^2 x 3 = 12", "difficulty": 2},
        {"id": "q-num3-2", "topic_id": "num-3", "topic_title": "HCF, LCM & Prime Factors", "question": "What is the LCM of 6 and 8?", "options": ["24", "48", "14", "2"], "correct_answer": 0, "explanation": "6 = 2 x 3, 8 = 2^3. LCM = 2^3 x 3 = 24", "difficulty": 1},
        # Algebra quiz
        {"id": "q-alg1-1", "topic_id": "alg-1", "topic_title": "Expanding & Factorising Brackets", "question": "Expand 3(2x + 5)", "options": ["6x + 5", "6x + 15", "5x + 15", "6x + 8"], "correct_answer": 1, "explanation": "3 x 2x = 6x, and 3 x 5 = 15. So 3(2x + 5) = 6x + 15", "difficulty": 1},
        {"id": "q-alg1-2", "topic_id": "alg-1", "topic_title": "Expanding & Factorising Brackets", "question": "Factorise x^2 + 7x + 12", "options": ["(x+3)(x+4)", "(x+2)(x+6)", "(x+1)(x+12)", "(x+6)(x+1)"], "correct_answer": 0, "explanation": "Find two numbers that multiply to 12 and add to 7: 3 and 4. So (x+3)(x+4)", "difficulty": 2},
        {"id": "q-alg2-1", "topic_id": "alg-2", "topic_title": "Solving Linear Equations", "question": "Solve: 3x + 7 = 22", "options": ["x = 5", "x = 3", "x = 7", "x = 15"], "correct_answer": 0, "explanation": "3x + 7 = 22. Subtract 7: 3x = 15. Divide by 3: x = 5", "difficulty": 1},
        {"id": "q-alg2-2", "topic_id": "alg-2", "topic_title": "Solving Linear Equations", "question": "Solve: 5(x - 2) = 3x + 4", "options": ["x = 7", "x = 3", "x = -7", "x = 14"], "correct_answer": 0, "explanation": "5x - 10 = 3x + 4. Subtract 3x: 2x - 10 = 4. Add 10: 2x = 14. Divide: x = 7", "difficulty": 2},
        # Sequences
        {"id": "q-alg4-1", "topic_id": "alg-4", "topic_title": "Sequences & nth Term", "question": "Find the next term in: 3, 7, 11, 15, ...", "options": ["17", "18", "19", "21"], "correct_answer": 2, "explanation": "Common difference = 4. Next term = 15 + 4 = 19", "difficulty": 1},
        {"id": "q-alg4-2", "topic_id": "alg-4", "topic_title": "Sequences & nth Term", "question": "What is the nth term of: 5, 8, 11, 14, ...?", "options": ["3n + 2", "3n + 5", "5n + 3", "3n - 2"], "correct_answer": 0, "explanation": "Common difference d = 3. nth term = 3n + (5-3) = 3n + 2. Check: n=1: 3(1)+2 = 5", "difficulty": 2},
        # Ratio
        {"id": "q-rat1-1", "topic_id": "rat-1", "topic_title": "Ratio & Proportion", "question": "Share 200 in the ratio 3:7", "options": ["60 and 140", "30 and 170", "100 and 100", "80 and 120"], "correct_answer": 0, "explanation": "Total parts = 3 + 7 = 10. One part = 200/10 = 20. So 3 x 20 = 60 and 7 x 20 = 140", "difficulty": 1},
        # Percentages
        {"id": "q-rat2-1", "topic_id": "rat-2", "topic_title": "Percentages & Interest", "question": "Increase 80 by 15%", "options": ["92", "95", "88", "82"], "correct_answer": 0, "explanation": "15% of 80 = 0.15 x 80 = 12. So 80 + 12 = 92. Or: 80 x 1.15 = 92", "difficulty": 1},
        # Geometry
        {"id": "q-geo1-1", "topic_id": "geo-1", "topic_title": "Angles & Polygons", "question": "What is the sum of interior angles of a hexagon?", "options": ["540", "720", "360", "1080"], "correct_answer": 1, "explanation": "(6-2) x 180 = 4 x 180 = 720 degrees", "difficulty": 1},
        {"id": "q-geo2-1", "topic_id": "geo-2", "topic_title": "Pythagoras' Theorem & Trigonometry", "question": "A right triangle has legs of 3 cm and 4 cm. What is the hypotenuse?", "options": ["5 cm", "7 cm", "6 cm", "25 cm"], "correct_answer": 0, "explanation": "c^2 = 3^2 + 4^2 = 9 + 16 = 25. c = sqrt(25) = 5 cm", "difficulty": 1},
        {"id": "q-geo3-1", "topic_id": "geo-3", "topic_title": "Area, Perimeter & Volume", "question": "Find the area of a circle with radius 7 cm (to 1 d.p.)", "options": ["153.9 cm^2", "44.0 cm^2", "49.0 cm^2", "21.98 cm^2"], "correct_answer": 0, "explanation": "Area = pi x r^2 = pi x 49 = 153.9 cm^2", "difficulty": 1},
        # Probability
        {"id": "q-sta1-1", "topic_id": "sta-1", "topic_title": "Probability Basics", "question": "A fair dice is rolled. What is P(even number)?", "options": ["1/6", "1/3", "1/2", "2/3"], "correct_answer": 2, "explanation": "Even numbers: 2, 4, 6 = 3 outcomes. Total = 6. P(even) = 3/6 = 1/2", "difficulty": 1},
        {"id": "q-sta2-1", "topic_id": "sta-2", "topic_title": "Averages & Representing Data", "question": "Find the median of: 3, 7, 1, 9, 5", "options": ["5", "7", "3", "1"], "correct_answer": 0, "explanation": "In order: 1, 3, 5, 7, 9. Middle value = 5", "difficulty": 1},
        # Quadratics
        {"id": "q-alg5-1", "topic_id": "alg-5", "topic_title": "Solving Quadratic Equations", "question": "Solve x^2 - 5x + 6 = 0", "options": ["x = 2 and x = 3", "x = -2 and x = -3", "x = 1 and x = 6", "x = -1 and x = -6"], "correct_answer": 0, "explanation": "Factorise: (x-2)(x-3) = 0. So x = 2 or x = 3", "difficulty": 2},
        # Linear Graphs
        {"id": "q-alg6-1", "topic_id": "alg-6", "topic_title": "Linear Graphs", "question": "What is the gradient of y = 3x - 7?", "options": ["3", "-7", "7", "-3"], "correct_answer": 0, "explanation": "In y = mx + c, m is the gradient. Here m = 3", "difficulty": 1},
        # Transformations
        {"id": "q-geo4-1", "topic_id": "geo-4", "topic_title": "Transformations", "question": "What information must you give for a rotation?", "options": ["Angle, direction, and centre", "Scale factor and centre", "Mirror line", "Column vector"], "correct_answer": 0, "explanation": "A rotation requires: angle, direction (CW/ACW), and centre of rotation", "difficulty": 1},
        # Speed
        {"id": "q-rat3-1", "topic_id": "rat-3", "topic_title": "Speed, Distance & Time", "question": "A car travels 120 km in 1.5 hours. What is its average speed?", "options": ["80 km/h", "60 km/h", "90 km/h", "180 km/h"], "correct_answer": 0, "explanation": "Speed = Distance / Time = 120 / 1.5 = 80 km/h", "difficulty": 1},
    ]

    for q in quiz_data:
        await db.quizzes.insert_one(q)

    # --- PAST PAPERS ---
    past_papers_data = [
        # Edexcel
        {"id": "pp-ed-2024-1f", "board": "Edexcel", "year": "2024", "paper_number": 1, "tier": "Foundation", "calculator_allowed": False, "description": "Paper 1 Non-Calculator (Foundation) - June 2024", "link": "https://qualifications.pearson.com/en/qualifications/edexcel-gcses/mathematics-2015.html", "practice_questions": [
            {"question": "Work out 3/4 + 2/5", "answer": "3/4 + 2/5 = 15/20 + 8/20 = 23/20 = 1 3/20", "marks": 2, "topic": "Fractions"},
            {"question": "Simplify 4x + 3y - 2x + 5y", "answer": "4x - 2x + 3y + 5y = 2x + 8y", "marks": 2, "topic": "Algebra"},
            {"question": "A shape has 5 sides. Calculate the sum of its interior angles.", "answer": "(5-2) x 180 = 540 degrees", "marks": 2, "topic": "Geometry"},
        ]},
        {"id": "pp-ed-2024-2f", "board": "Edexcel", "year": "2024", "paper_number": 2, "tier": "Foundation", "calculator_allowed": True, "description": "Paper 2 Calculator (Foundation) - June 2024", "link": "https://qualifications.pearson.com/en/qualifications/edexcel-gcses/mathematics-2015.html", "practice_questions": [
            {"question": "Calculate 15% of 340", "answer": "0.15 x 340 = 51", "marks": 2, "topic": "Percentages"},
            {"question": "The probability of picking a red ball is 0.35. What is the probability of NOT picking a red ball?", "answer": "1 - 0.35 = 0.65", "marks": 1, "topic": "Probability"},
        ]},
        {"id": "pp-ed-2024-3f", "board": "Edexcel", "year": "2024", "paper_number": 3, "tier": "Foundation", "calculator_allowed": True, "description": "Paper 3 Calculator (Foundation) - June 2024", "link": "https://qualifications.pearson.com/en/qualifications/edexcel-gcses/mathematics-2015.html", "practice_questions": [
            {"question": "Share 240 in the ratio 3:5", "answer": "Total parts = 8, one part = 30. Answer: 90 and 150", "marks": 2, "topic": "Ratio"},
        ]},
        {"id": "pp-ed-2024-1h", "board": "Edexcel", "year": "2024", "paper_number": 1, "tier": "Higher", "calculator_allowed": False, "description": "Paper 1 Non-Calculator (Higher) - June 2024", "link": "https://qualifications.pearson.com/en/qualifications/edexcel-gcses/mathematics-2015.html", "practice_questions": [
            {"question": "Solve x^2 - 6x + 8 = 0", "answer": "(x-2)(x-4) = 0, so x = 2 or x = 4", "marks": 3, "topic": "Quadratics"},
            {"question": "Simplify (2^3 x 2^5) / 2^2", "answer": "2^(3+5-2) = 2^6 = 64", "marks": 2, "topic": "Indices"},
        ]},
        {"id": "pp-ed-2023-1f", "board": "Edexcel", "year": "2023", "paper_number": 1, "tier": "Foundation", "calculator_allowed": False, "description": "Paper 1 Non-Calculator (Foundation) - June 2023", "link": "https://qualifications.pearson.com/en/qualifications/edexcel-gcses/mathematics-2015.html", "practice_questions": [
            {"question": "Work out 24 x 15 without a calculator", "answer": "24 x 15 = 24 x 10 + 24 x 5 = 240 + 120 = 360", "marks": 3, "topic": "Number"},
        ]},
        {"id": "pp-ed-2023-2h", "board": "Edexcel", "year": "2023", "paper_number": 2, "tier": "Higher", "calculator_allowed": True, "description": "Paper 2 Calculator (Higher) - June 2023", "link": "https://qualifications.pearson.com/en/qualifications/edexcel-gcses/mathematics-2015.html", "practice_questions": [
            {"question": "A circle has circumference 31.4 cm. Find its radius.", "answer": "C = 2 x pi x r. So r = 31.4 / (2 x pi) = 5 cm", "marks": 2, "topic": "Circles"},
        ]},
        # AQA
        {"id": "pp-aqa-2024-1f", "board": "AQA", "year": "2024", "paper_number": 1, "tier": "Foundation", "calculator_allowed": False, "description": "Paper 1 Non-Calculator (Foundation) - June 2024", "link": "https://www.aqa.org.uk/subjects/mathematics/gcse/mathematics-8300", "practice_questions": [
            {"question": "Write 0.7 as a fraction", "answer": "0.7 = 7/10", "marks": 1, "topic": "Fractions"},
            {"question": "Find the next two terms: 2, 6, 10, 14, ...", "answer": "Common difference = 4. Next terms: 18, 22", "marks": 2, "topic": "Sequences"},
        ]},
        {"id": "pp-aqa-2024-2f", "board": "AQA", "year": "2024", "paper_number": 2, "tier": "Foundation", "calculator_allowed": True, "description": "Paper 2 Calculator (Foundation) - June 2024", "link": "https://www.aqa.org.uk/subjects/mathematics/gcse/mathematics-8300", "practice_questions": [
            {"question": "A car travels 195 miles in 3 hours. Calculate the average speed.", "answer": "Speed = 195 / 3 = 65 mph", "marks": 2, "topic": "Speed"},
        ]},
        {"id": "pp-aqa-2024-3h", "board": "AQA", "year": "2024", "paper_number": 3, "tier": "Higher", "calculator_allowed": True, "description": "Paper 3 Calculator (Higher) - June 2024", "link": "https://www.aqa.org.uk/subjects/mathematics/gcse/mathematics-8300", "practice_questions": [
            {"question": "Find the equation of the line through (2, 5) with gradient 3", "answer": "y = 3x + c. Using (2,5): 5 = 6 + c, so c = -1. Answer: y = 3x - 1", "marks": 3, "topic": "Linear Graphs"},
        ]},
        {"id": "pp-aqa-2023-1f", "board": "AQA", "year": "2023", "paper_number": 1, "tier": "Foundation", "calculator_allowed": False, "description": "Paper 1 Non-Calculator (Foundation) - June 2023", "link": "https://www.aqa.org.uk/subjects/mathematics/gcse/mathematics-8300", "practice_questions": [
            {"question": "Work out 3/4 of 360", "answer": "360 / 4 = 90, then 90 x 3 = 270", "marks": 2, "topic": "Fractions"},
        ]},
        {"id": "pp-aqa-2023-2h", "board": "AQA", "year": "2023", "paper_number": 2, "tier": "Higher", "calculator_allowed": True, "description": "Paper 2 Calculator (Higher) - June 2023", "link": "https://www.aqa.org.uk/subjects/mathematics/gcse/mathematics-8300", "practice_questions": [
            {"question": "Solve the simultaneous equations: 2x + y = 7 and x - y = 2", "answer": "Add: 3x = 9, x = 3. Sub: 3 - y = 2, y = 1. Solution: x=3, y=1", "marks": 3, "topic": "Simultaneous Equations"},
        ]},
        # OCR
        {"id": "pp-ocr-2024-1f", "board": "OCR", "year": "2024", "paper_number": 1, "tier": "Foundation", "calculator_allowed": False, "description": "Paper 1 Non-Calculator (Foundation) - June 2024", "link": "https://www.ocr.org.uk/qualifications/gcse/mathematics-j560-from-2015/", "practice_questions": [
            {"question": "Simplify the ratio 15:25", "answer": "Divide both by 5: 15:25 = 3:5", "marks": 1, "topic": "Ratio"},
            {"question": "Find the mean of 3, 5, 7, 4, 6", "answer": "Sum = 25. Mean = 25 / 5 = 5", "marks": 2, "topic": "Averages"},
        ]},
        {"id": "pp-ocr-2024-2f", "board": "OCR", "year": "2024", "paper_number": 2, "tier": "Foundation", "calculator_allowed": True, "description": "Paper 2 Calculator (Foundation) - June 2024", "link": "https://www.ocr.org.uk/qualifications/gcse/mathematics-j560-from-2015/", "practice_questions": [
            {"question": "A bag contains 4 red and 6 blue counters. What is P(red)?", "answer": "P(red) = 4/10 = 2/5", "marks": 2, "topic": "Probability"},
        ]},
        {"id": "pp-ocr-2024-3h", "board": "OCR", "year": "2024", "paper_number": 3, "tier": "Higher", "calculator_allowed": True, "description": "Paper 3 Calculator (Higher) - June 2024", "link": "https://www.ocr.org.uk/qualifications/gcse/mathematics-j560-from-2015/", "practice_questions": [
            {"question": "Find the volume of a cone with radius 5 cm and height 12 cm", "answer": "V = 1/3 x pi x 5^2 x 12 = 100pi = 314.2 cm^3", "marks": 3, "topic": "Volume"},
        ]},
        {"id": "pp-ocr-2023-1f", "board": "OCR", "year": "2023", "paper_number": 1, "tier": "Foundation", "calculator_allowed": False, "description": "Paper 1 Non-Calculator (Foundation) - June 2023", "link": "https://www.ocr.org.uk/qualifications/gcse/mathematics-j560-from-2015/", "practice_questions": [
            {"question": "Convert 3/8 to a decimal", "answer": "3 / 8 = 0.375", "marks": 1, "topic": "Fractions"},
        ]},
    ]

    for paper in past_papers_data:
        await db.past_papers.insert_one(paper)

    # --- FORMULAS ---
    formulas_data = [
        {"id": "f-1", "category": "Number", "name": "Percentage Change", "formula": "% change = (change / original) x 100", "description": "Calculate the percentage increase or decrease", "usage_example": "Price goes from 40 to 50: change = 10, % = (10/40) x 100 = 25%"},
        {"id": "f-2", "category": "Number", "name": "Compound Interest", "formula": "A = P(1 + r/100)^n", "description": "Calculate compound interest where P is principal, r is rate, n is years", "usage_example": "500 at 3% for 4 years: 500 x 1.03^4 = 562.75"},
        {"id": "f-3", "category": "Algebra", "name": "Quadratic Formula", "formula": "x = (-b +/- sqrt(b^2 - 4ac)) / 2a", "description": "Solve ax^2 + bx + c = 0", "usage_example": "Solve x^2 + 5x + 6 = 0: a=1, b=5, c=6"},
        {"id": "f-4", "category": "Algebra", "name": "Straight Line", "formula": "y = mx + c", "description": "m = gradient, c = y-intercept", "usage_example": "Gradient 2, y-intercept 3: y = 2x + 3"},
        {"id": "f-5", "category": "Geometry & Measures", "name": "Area of Triangle", "formula": "A = 1/2 x base x height", "description": "Area of any triangle using base and perpendicular height", "usage_example": "Base 8, height 5: A = 1/2 x 8 x 5 = 20"},
        {"id": "f-6", "category": "Geometry & Measures", "name": "Area of Circle", "formula": "A = pi x r^2", "description": "Area of a circle using radius", "usage_example": "Radius 7: A = pi x 49 = 153.9"},
        {"id": "f-7", "category": "Geometry & Measures", "name": "Circumference", "formula": "C = 2 x pi x r = pi x d", "description": "Circumference (perimeter) of a circle", "usage_example": "Radius 5: C = 2 x pi x 5 = 31.4"},
        {"id": "f-8", "category": "Geometry & Measures", "name": "Pythagoras' Theorem", "formula": "a^2 + b^2 = c^2", "description": "For right-angled triangles where c is the hypotenuse", "usage_example": "Sides 3 and 4: c^2 = 9 + 16 = 25, c = 5"},
        {"id": "f-9", "category": "Geometry & Measures", "name": "Volume of Cuboid", "formula": "V = l x w x h", "description": "Volume of a cuboid (rectangular box)", "usage_example": "3 x 4 x 5 = 60 cm^3"},
        {"id": "f-10", "category": "Geometry & Measures", "name": "Volume of Cylinder", "formula": "V = pi x r^2 x h", "description": "Volume of a cylinder", "usage_example": "Radius 3, height 10: V = pi x 9 x 10 = 282.7"},
        {"id": "f-11", "category": "Geometry & Measures", "name": "Volume of Sphere", "formula": "V = 4/3 x pi x r^3", "description": "Volume of a sphere", "usage_example": "Radius 6: V = 4/3 x pi x 216 = 904.8"},
        {"id": "f-12", "category": "Geometry & Measures", "name": "Trigonometry (SOHCAHTOA)", "formula": "sin = O/H, cos = A/H, tan = O/A", "description": "Trig ratios for right-angled triangles", "usage_example": "Opp=3, Hyp=5: sin(x) = 3/5, x = 36.9 degrees"},
        {"id": "f-13", "category": "Geometry & Measures", "name": "Interior Angles Sum", "formula": "Sum = (n - 2) x 180", "description": "Sum of interior angles of an n-sided polygon", "usage_example": "Pentagon (n=5): (5-2) x 180 = 540 degrees"},
        {"id": "f-14", "category": "Geometry & Measures", "name": "Area of Trapezium", "formula": "A = 1/2 x (a + b) x h", "description": "Area of a trapezium where a and b are parallel sides", "usage_example": "Parallel sides 5 and 9, height 4: A = 1/2 x 14 x 4 = 28"},
        {"id": "f-15", "category": "Probability & Statistics", "name": "Probability", "formula": "P(event) = favourable outcomes / total outcomes", "description": "Basic probability formula", "usage_example": "P(rolling 6 on dice) = 1/6"},
        {"id": "f-16", "category": "Ratio & Proportion", "name": "Speed, Distance, Time", "formula": "S = D/T, D = S x T, T = D/S", "description": "Relationship between speed, distance and time", "usage_example": "120km in 2 hours: S = 120/2 = 60 km/h"},
        {"id": "f-17", "category": "Ratio & Proportion", "name": "Density", "formula": "Density = Mass / Volume", "description": "Relationship between density, mass and volume", "usage_example": "Mass 500g, Volume 200cm^3: D = 2.5 g/cm^3"},
        {"id": "f-18", "category": "Geometry & Measures", "name": "Surface Area of Cylinder", "formula": "SA = 2 x pi x r^2 + 2 x pi x r x h", "description": "Total surface area of a cylinder", "usage_example": "r=3, h=10: SA = 2pi(9) + 2pi(30) = 245.0"},
        {"id": "f-19", "category": "Algebra", "name": "nth Term (Linear)", "formula": "nth term = dn + (a - d)", "description": "Find the nth term of an arithmetic sequence. d = common difference, a = first term", "usage_example": "Sequence 3,7,11,15: d=4, a=3. nth term = 4n - 1"},
        {"id": "f-20", "category": "Geometry & Measures", "name": "Volume of Cone", "formula": "V = 1/3 x pi x r^2 x h", "description": "Volume of a cone", "usage_example": "r=4, h=9: V = 1/3 x pi x 16 x 9 = 150.8"},
    ]

    for f in formulas_data:
        await db.formulas.insert_one(f)

    # --- INSERT ADDITIONAL CONTENT ---
    from seed_data import ADDITIONAL_TOPICS, ADDITIONAL_QUIZZES, ADDITIONAL_PAST_PAPERS, ADDITIONAL_FORMULAS, PAPERS_2020_2021

    for topic in ADDITIONAL_TOPICS:
        enrich = enrichments.get(topic["id"], {})
        topic.update(enrich)
        await db.topics.insert_one(topic)
    for q in ADDITIONAL_QUIZZES:
        await db.quizzes.insert_one(q)
    for paper in ADDITIONAL_PAST_PAPERS:
        await db.past_papers.insert_one(paper)
    for paper in PAPERS_2020_2021:
        await db.past_papers.insert_one(paper)
    for f in ADDITIONAL_FORMULAS:
        await db.formulas.insert_one(f)

    total_topics = len(topics_data) + len(ADDITIONAL_TOPICS)
    total_quizzes = len(quiz_data) + len(ADDITIONAL_QUIZZES)
    total_papers = len(past_papers_data) + len(ADDITIONAL_PAST_PAPERS) + len(PAPERS_2020_2021)
    total_formulas = len(formulas_data) + len(ADDITIONAL_FORMULAS)

    return {"message": "Database seeded successfully", "topics": total_topics, "quizzes": total_quizzes, "papers": total_papers, "formulas": total_formulas}

@api_router.get("/stats")
async def get_stats():
    topics_count = await db.topics.count_documents({})
    quizzes_count = await db.quizzes.count_documents({})
    papers_count = await db.past_papers.count_documents({})
    formulas_count = await db.formulas.count_documents({})
    categories = await db.topics.distinct("category")
    return {
        "topics": topics_count,
        "quizzes": quizzes_count,
        "papers": papers_count,
        "formulas": formulas_count,
        "categories": len(categories)
    }

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
