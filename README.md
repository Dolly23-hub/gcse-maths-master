# GCSE Maths Master

A free, open-access revision platform for UK students sitting GCSE Maths (Edexcel, AQA, OCR). Every topic follows a guided **7-step learning journey** — video explanation, big idea, visual example, step-by-step method, a mini quiz, an AI tutor, and links to practice.

![Made with React](https://img.shields.io/badge/frontend-React-61dafb)
![Made with FastAPI](https://img.shields.io/badge/backend-FastAPI-009688)
![MongoDB](https://img.shields.io/badge/db-MongoDB-47a248)
![License: MIT](https://img.shields.io/badge/license-MIT-yellow)

---

## ✨ Features

- **33 full topics** across Number, Algebra, Ratio & Proportion, Geometry & Measures, and Probability & Statistics.
- **7-step guided learning journey** for every topic:
  1. 🎥 **Video Explanation** — embedded Corbettmaths YouTube videos
  2. 💡 **Big Idea** — one core insight
  3. 📊 **Visual Example** — formatted worked example
  4. 🔄 **Step-by-step Method** — numbered, exam-ready procedure
  5. 🧠 **Try it yourself** — instant-feedback mini quiz
  6. 🤖 **AI Tutor** — topic-aware chat powered by GPT-5.2
  7. ➡️ **Continue to examples** — jump to practice quizzes & past papers
- **84 quiz questions** with instant marking and explanations.
- **38 past papers** from 2020–2024 (Edexcel, AQA, OCR — Foundation and Higher).
- **30 formulas** on a printable formula sheet.
- **AI Revision Planner** — personalised weekly study plan with 5 AI-generated revision tips.
- **Progress tracking** (localStorage) and exam countdown.
- **Neo-Brutalist UI** — bold, high-contrast, mobile-responsive, shadcn/ui + Tailwind.

---

## 🏗️ Tech Stack

| Layer      | Technology                                                 |
|------------|------------------------------------------------------------|
| Frontend   | React 18, React Router, Tailwind CSS, shadcn/ui, lucide-react, axios, react-markdown |
| Backend    | FastAPI, Motor (async MongoDB), Pydantic v2                |
| Database   | MongoDB                                                    |
| AI         | OpenAI `gpt-5.2` via emergentintegrations using Emergent LLM Key |

---

## 📁 Project Structure

```
.
├── backend/
│   ├── server.py           # FastAPI app, API routes, DB seed
│   ├── seed_data.py        # Additional topics, quizzes, papers, formulas
│   ├── requirements.txt
│   ├── tests/              # pytest suite
│   └── .env                # MONGO_URL, DB_NAME, EMERGENT_LLM_KEY
├── frontend/
│   ├── src/
│   │   ├── pages/          # HomePage, TopicsPage, TopicDetailPage, QuizPage, …
│   │   ├── components/     # Navbar + shadcn/ui primitives
│   │   ├── utils/          # progress tracking
│   │   ├── App.js
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env                # REACT_APP_BACKEND_URL
├── memory/
│   └── PRD.md              # Product requirements & history
└── README.md
```

---

## 🚀 Run Locally

### Prerequisites

- **Python** 3.11+
- **Node.js** 18+ and **Yarn**
- **MongoDB** running locally (or a MongoDB Atlas URI)
- An **Emergent LLM Key** (for the AI Tutor / Revision Planner tips) — optional; the app still works without AI features.

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/gcse-maths-master.git
cd gcse-maths-master
```

### 2. Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate            # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=gcse_maths
EMERGENT_LLM_KEY=your_emergent_llm_key_here
```

Start the API server:

```bash
uvicorn server:app --reload --port 8001
```

Seed the database (one-off):

```bash
curl -X POST http://localhost:8001/api/seed
```

### 3. Frontend setup

In a new terminal:

```bash
cd frontend
yarn install
```

Create `frontend/.env`:

```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

Start the dev server:

```bash
yarn start
```

Open **http://localhost:3000** — and you're in. 🎉

---

## 🔌 API Endpoints

All routes are prefixed with `/api`.

| Method | Route                                  | Description                              |
|--------|----------------------------------------|------------------------------------------|
| GET    | `/api/topics`                          | List all topics                          |
| GET    | `/api/topics/{topic_id}`               | Full topic with guided-journey fields    |
| GET    | `/api/topics/category/{category}`      | Topics filtered by category              |
| GET    | `/api/quizzes/{topic_id}`              | Quiz questions for a topic               |
| POST   | `/api/quiz/check`                      | Check a selected answer                  |
| GET    | `/api/past-papers/{board}`             | Past papers by exam board                |
| GET    | `/api/formulas`                        | All formulas                             |
| POST   | `/api/ai-tutor`                        | Ask the AI tutor (topic-aware)           |
| POST   | `/api/revision-plan`                   | Generate a personalised revision plan    |
| POST   | `/api/seed`                            | (Re)seed the database                    |

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/
```

---

## 🧑‍🎨 Design Notes

- **Neo-Brutalist** aesthetic — thick black borders, offset shadows, flat bold colours per category.
- Every interactive element has a `data-testid` for reliable automated testing.
- Mobile-first responsive layout; typography scales from `text-base` to `text-5xl`.

---

## 🚢 Deploying

The app is designed for Emergent's one-click deployment, but you can also deploy it yourself:

- **Frontend:** Vercel, Netlify, or any static host (build with `yarn build`).
- **Backend:** Railway, Fly.io, Render, or any ASGI host. Make sure `MONGO_URL` is set.
- **Database:** MongoDB Atlas (free tier works).

Remember to update `REACT_APP_BACKEND_URL` on the frontend to your deployed API URL.

---

## 🙏 Credits

- Video explanations courtesy of the phenomenal **[Corbettmaths](https://www.youtube.com/@corbettmaths)** YouTube channel.
- Exam board references: **Edexcel / Pearson**, **AQA**, **OCR**.
- Built with ❤️ on [Emergent](https://emergent.sh).

---

## 📄 License

MIT — free to use, modify and share. Please keep a credit to Corbettmaths for the video content.
