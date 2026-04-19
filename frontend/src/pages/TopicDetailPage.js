import { useState, useEffect, useRef } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import {
  ArrowLeft,
  ArrowRight,
  Video,
  Lightbulb,
  BarChart3,
  ListOrdered,
  Brain,
  Bot,
  CheckCircle2,
  XCircle,
  Send,
  Loader2,
  BookOpen,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { markTopicViewed } from "@/utils/progress";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const CATEGORY_COLORS = {
  "Number": { bg: "bg-blue-50", text: "text-blue-600", pill: "bg-blue-600", border: "border-blue-600", accent: "bg-blue-600" },
  "Algebra": { bg: "bg-violet-50", text: "text-violet-600", pill: "bg-violet-600", border: "border-violet-600", accent: "bg-violet-600" },
  "Ratio & Proportion": { bg: "bg-orange-50", text: "text-orange-600", pill: "bg-orange-600", border: "border-orange-600", accent: "bg-orange-600" },
  "Geometry & Measures": { bg: "bg-green-50", text: "text-green-600", pill: "bg-green-600", border: "border-green-600", accent: "bg-green-600" },
  "Probability & Statistics": { bg: "bg-pink-50", text: "text-pink-600", pill: "bg-pink-600", border: "border-pink-600", accent: "bg-pink-600" },
};

function SectionHeader({ step, icon: Icon, title, colors }) {
  return (
    <div className="flex items-center gap-3 mb-5">
      <div className={`${colors.accent} text-white w-10 h-10 flex items-center justify-center border-2 border-black rounded-full font-heading font-bold shadow-[2px_2px_0_0_rgba(0,0,0,1)]`}>
        {step}
      </div>
      <Icon size={22} className={colors.text} />
      <h2 className="font-heading text-2xl sm:text-3xl font-bold">{title}</h2>
    </div>
  );
}

function TryItYourself({ quizzes, colors }) {
  const [selected, setSelected] = useState({});
  const [revealed, setRevealed] = useState({});

  const pick = quizzes.slice(0, 2);

  if (pick.length === 0) {
    return (
      <p data-testid="try-it-yourself-empty" className="text-neutral-600">
        Practice questions for this topic are coming soon — try the Practice Quiz below!
      </p>
    );
  }

  const handleSelect = (qid, idx) => {
    if (revealed[qid]) return;
    setSelected({ ...selected, [qid]: idx });
  };

  const handleCheck = (qid) => {
    setRevealed({ ...revealed, [qid]: true });
  };

  return (
    <div className="space-y-5" data-testid="try-it-yourself">
      {pick.map((q) => {
        const sel = selected[q.id];
        const shown = revealed[q.id];
        const isCorrect = shown && sel === q.correct_answer;

        return (
          <div key={q.id} className="border-2 border-black rounded-xl p-5 bg-white" data-testid={`try-it-q-${q.id}`}>
            <p className="font-bold mb-4">{q.question}</p>
            <div className="grid gap-2 sm:grid-cols-2 mb-4">
              {q.options.map((opt, i) => {
                const chosen = sel === i;
                const correctOpt = shown && i === q.correct_answer;
                const wrongOpt = shown && chosen && i !== q.correct_answer;
                return (
                  <button
                    key={i}
                    data-testid={`try-it-opt-${q.id}-${i}`}
                    onClick={() => handleSelect(q.id, i)}
                    disabled={shown}
                    className={`text-left px-4 py-3 border-2 border-black rounded-lg font-mono transition-all
                      ${correctOpt ? "bg-green-200" : ""}
                      ${wrongOpt ? "bg-red-200" : ""}
                      ${!shown && chosen ? `${colors.accent} text-white` : ""}
                      ${!shown && !chosen ? "bg-white hover:bg-neutral-50" : ""}
                    `}
                  >
                    {String.fromCharCode(65 + i)}. {opt}
                  </button>
                );
              })}
            </div>
            {!shown ? (
              <button
                data-testid={`try-it-check-${q.id}`}
                onClick={() => handleCheck(q.id)}
                disabled={sel === undefined}
                className="neo-btn-primary text-sm disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Check Answer
              </button>
            ) : (
              <div className={`border-2 border-black rounded-lg p-4 ${isCorrect ? "bg-green-50" : "bg-red-50"}`} data-testid={`try-it-feedback-${q.id}`}>
                <div className="flex items-center gap-2 mb-2 font-bold">
                  {isCorrect ? (
                    <>
                      <CheckCircle2 size={18} className="text-green-700" /> Correct!
                    </>
                  ) : (
                    <>
                      <XCircle size={18} className="text-red-700" /> Not quite.
                    </>
                  )}
                </div>
                <p className="text-sm text-neutral-700 leading-relaxed">{q.explanation}</p>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

function InlineAITutor({ topicTitle, colors }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const endRef = useRef(null);

  const starters = [
    `Give me a simple, step-by-step walkthrough of ${topicTitle}.`,
    `What mistakes do students usually make with ${topicTitle}?`,
    `Can you give me a harder practice question on ${topicTitle}?`,
  ];

  const ask = async (text) => {
    if (!text.trim()) return;
    setLoading(true);
    setError("");
    setAnswer("");
    try {
      const res = await axios.post(`${API}/ai-tutor`, {
        question: text,
        topic: topicTitle,
      });
      setAnswer(res.data.response);
      setTimeout(() => endRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" }), 100);
    } catch (e) {
      setError("Sorry, the tutor is unavailable right now. Please try again in a moment.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div data-testid="inline-ai-tutor" className="space-y-4">
      <p className="text-neutral-700">
        Stuck on something? Ask our AI tutor anything about <strong>{topicTitle}</strong>.
      </p>

      <div className="flex flex-wrap gap-2">
        {starters.map((s, i) => (
          <button
            key={i}
            data-testid={`ai-starter-${i}`}
            onClick={() => {
              setQuestion(s);
              ask(s);
            }}
            className="text-xs sm:text-sm px-3 py-2 border-2 border-black rounded-full bg-white hover:bg-neutral-50 font-bold transition-all"
          >
            {s}
          </button>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          data-testid="ai-input"
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") ask(question);
          }}
          placeholder={`Ask about ${topicTitle}…`}
          className="flex-1 px-4 py-3 border-2 border-black rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-black"
          disabled={loading}
        />
        <button
          data-testid="ai-send"
          onClick={() => ask(question)}
          disabled={loading || !question.trim()}
          className={`${colors.accent} text-white border-2 border-black rounded-lg px-4 font-bold flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed shadow-[3px_3px_0_0_rgba(0,0,0,1)] hover:translate-y-[1px] hover:shadow-[2px_2px_0_0_rgba(0,0,0,1)] transition-all`}
        >
          {loading ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
        </button>
      </div>

      {error && (
        <p data-testid="ai-error" className="text-red-600 font-bold text-sm">
          {error}
        </p>
      )}

      {loading && (
        <div data-testid="ai-loading" className="flex items-center gap-3 p-4 border-2 border-black rounded-lg bg-neutral-50">
          <Loader2 size={18} className="animate-spin" />
          <span className="text-sm text-neutral-600">Your tutor is thinking…</span>
        </div>
      )}

      {answer && (
        <div data-testid="ai-answer" className="border-2 border-black rounded-xl p-5 bg-white">
          <div className="markdown-content prose prose-sm max-w-none">
            <ReactMarkdown>{answer}</ReactMarkdown>
          </div>
          <div ref={endRef} />
        </div>
      )}
    </div>
  );
}

export default function TopicDetailPage() {
  const { topicId } = useParams();
  const [topic, setTopic] = useState(null);
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    (async () => {
      try {
        const [tRes, qRes] = await Promise.all([
          axios.get(`${API}/topics/${topicId}`),
          axios.get(`${API}/quizzes/${topicId}`),
        ]);
        if (cancelled) return;
        setTopic(tRes.data);
        setQuizzes(qRes.data.questions || []);
        markTopicViewed(topicId);
      } catch (e) {
        console.error("Error fetching topic:", e);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [topicId]);

  if (loading) {
    return (
      <div data-testid="topic-detail-loading" className="flex items-center justify-center min-h-[60vh]">
        <div className="w-8 h-8 border-4 border-black border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!topic) {
    return (
      <div data-testid="topic-not-found" className="flex flex-col items-center justify-center min-h-[60vh]">
        <p className="text-lg text-neutral-500 mb-4">Topic not found</p>
        <Link to="/topics" className="neo-btn-primary">Back to Topics</Link>
      </div>
    );
  }

  const colors = CATEGORY_COLORS[topic.category] || CATEGORY_COLORS["Number"];

  return (
    <div className="min-h-screen pb-16">
      {/* Header */}
      <section className={`py-8 sm:py-12 border-b-2 border-black ${colors.bg}`}>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <Link
            to="/topics"
            data-testid="back-to-topics"
            className="inline-flex items-center gap-2 text-sm font-bold mb-6 hover:gap-3 transition-all"
          >
            <ArrowLeft size={16} /> Back to Topics
          </Link>
          <div className="flex flex-wrap items-center gap-3 mb-4">
            <Badge className={`${colors.pill} text-white border-2 border-black font-bold`}>{topic.category}</Badge>
            <Badge variant="outline" className="border-2 border-black font-mono">{topic.tier}</Badge>
            <div className="flex items-center gap-1">
              {[1, 2, 3, 4, 5].map((d) => (
                <div key={d} className={`w-2 h-2 rounded-full ${d <= topic.difficulty ? colors.pill : "bg-neutral-300"}`} />
              ))}
            </div>
          </div>
          <h1 data-testid="topic-detail-title" className="font-heading text-3xl sm:text-4xl lg:text-5xl font-bold mb-3">
            {topic.title}
          </h1>
          <p className="text-neutral-600 text-base sm:text-lg">{topic.description}</p>

          {/* Journey progress dots */}
          <div data-testid="journey-progress" className="flex items-center gap-1.5 mt-6" aria-label="Learning journey progress">
            {[1, 2, 3, 4, 5, 6, 7].map((s) => (
              <div key={s} className={`h-1.5 rounded-full ${colors.accent} flex-1 max-w-[40px]`} />
            ))}
          </div>
        </div>
      </section>

      {/* Guided journey content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">

        {/* 1. Video Explanation */}
        <section data-testid="section-video" className="scroll-mt-24" id="video">
          <SectionHeader step={1} icon={Video} title="Video Explanation" colors={colors} />
          {topic.video_id ? (
            <div className="border-2 border-black rounded-xl overflow-hidden shadow-[6px_6px_0_0_rgba(0,0,0,1)]">
              <div className="relative w-full" style={{ paddingTop: "56.25%" }}>
                <iframe
                  data-testid="video-iframe"
                  className="absolute inset-0 w-full h-full"
                  src={`https://www.youtube.com/embed/${topic.video_id}?rel=0&modestbranding=1`}
                  title={`${topic.title} — video explanation`}
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              </div>
            </div>
          ) : (
            <p className="text-neutral-600">Video coming soon for this topic.</p>
          )}
          <p className="text-xs text-neutral-500 mt-3">Tip: watch on 1.25× speed and pause whenever something isn't clear.</p>
        </section>

        {/* 2. Big Idea */}
        <section data-testid="section-big-idea" className="scroll-mt-24" id="big-idea">
          <SectionHeader step={2} icon={Lightbulb} title="Big Idea" colors={colors} />
          <div className="border-2 border-black rounded-xl p-6 sm:p-8 bg-yellow-100 shadow-[6px_6px_0_0_rgba(0,0,0,1)]">
            <p data-testid="big-idea-text" className="font-heading text-xl sm:text-2xl leading-snug">
              {topic.big_idea || "One core idea to keep in mind as you work through this topic."}
            </p>
          </div>
        </section>

        {/* 3. Visual Example */}
        <section data-testid="section-visual-example" className="scroll-mt-24" id="visual-example">
          <SectionHeader step={3} icon={BarChart3} title="Visual Example" colors={colors} />
          <div className="border-2 border-black rounded-xl p-5 sm:p-7 bg-white">
            <div className="markdown-content prose max-w-none" data-testid="visual-example-content">
              <ReactMarkdown>{topic.visual_example || "A worked example for this topic will appear here."}</ReactMarkdown>
            </div>
          </div>
        </section>

        {/* 4. Step-by-step */}
        <section data-testid="section-step-by-step" className="scroll-mt-24" id="steps">
          <SectionHeader step={4} icon={ListOrdered} title="Step-by-step Method" colors={colors} />
          {topic.step_by_step && topic.step_by_step.length > 0 ? (
            <ol className="space-y-3" data-testid="step-list">
              {topic.step_by_step.map((step, i) => (
                <li
                  key={i}
                  data-testid={`step-${i}`}
                  className="flex gap-4 border-2 border-black rounded-xl p-4 bg-white hover:bg-neutral-50 transition-colors"
                >
                  <div className={`${colors.accent} text-white font-heading font-bold w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-full border-2 border-black`}>
                    {i + 1}
                  </div>
                  <p className="text-neutral-800 leading-relaxed pt-1">{step}</p>
                </li>
              ))}
            </ol>
          ) : (
            <div className="markdown-content prose max-w-none border-2 border-black rounded-xl p-5 bg-white">
              <ReactMarkdown>{topic.explanation}</ReactMarkdown>
            </div>
          )}

          {topic.key_points && topic.key_points.length > 0 && (
            <div data-testid="key-points" className="mt-6 border-2 border-black rounded-xl p-5 bg-neutral-50">
              <div className="flex items-center gap-2 mb-3">
                <BookOpen size={18} className={colors.text} />
                <h3 className="font-heading font-bold">Remember…</h3>
              </div>
              <ul className="space-y-2">
                {topic.key_points.map((p, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <CheckCircle2 size={16} className="text-green-600 mt-0.5 flex-shrink-0" />
                    <span>{p}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>

        {/* 5. Try it yourself */}
        <section data-testid="section-try-it" className="scroll-mt-24" id="try-it">
          <SectionHeader step={5} icon={Brain} title="Try it yourself" colors={colors} />
          <TryItYourself quizzes={quizzes} colors={colors} />
        </section>

        {/* 6. AI Tutor (inline) */}
        <section data-testid="section-ai-tutor" className="scroll-mt-24" id="ai-tutor">
          <SectionHeader step={6} icon={Bot} title="Ask the AI Tutor" colors={colors} />
          <div className="border-2 border-black rounded-xl p-5 sm:p-6 bg-white shadow-[6px_6px_0_0_rgba(0,0,0,1)]">
            <InlineAITutor topicTitle={topic.title} colors={colors} />
          </div>
        </section>

        {/* 7. Continue to examples */}
        <section data-testid="section-continue" className="scroll-mt-24" id="continue">
          <SectionHeader step={7} icon={ArrowRight} title="Continue to examples" colors={colors} />
          <div className="border-2 border-black rounded-xl p-6 bg-black text-white">
            <p className="mb-5 text-neutral-200">
              You've worked through the full journey for <strong>{topic.title}</strong>. Time to
              lock it in with practice questions and past-paper style problems.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link
                to={`/quiz/${topicId}`}
                data-testid="continue-quiz-btn"
                className={`${colors.accent} text-white border-2 border-white rounded-lg px-5 py-3 font-bold inline-flex items-center gap-2 shadow-[4px_4px_0_0_rgba(255,255,255,1)] hover:translate-y-[1px] hover:shadow-[2px_2px_0_0_rgba(255,255,255,1)] transition-all`}
              >
                <Brain size={18} /> Practice Quiz
              </Link>
              <Link
                to="/past-papers"
                data-testid="continue-papers-btn"
                className="bg-white text-black border-2 border-white rounded-lg px-5 py-3 font-bold inline-flex items-center gap-2 shadow-[4px_4px_0_0_rgba(255,255,255,1)] hover:translate-y-[1px] hover:shadow-[2px_2px_0_0_rgba(255,255,255,1)] transition-all"
              >
                <ArrowRight size={18} /> Past Paper Questions
              </Link>
              <Link
                to="/topics"
                data-testid="continue-topics-btn"
                className="bg-transparent text-white border-2 border-white rounded-lg px-5 py-3 font-bold inline-flex items-center gap-2 hover:bg-white hover:text-black transition-all"
              >
                More Topics
              </Link>
            </div>
          </div>
        </section>

        {/* Worked examples (kept for backwards compat, collapsed) */}
        {topic.worked_examples && topic.worked_examples.length > 0 && (
          <details data-testid="extra-worked-examples" className="border-2 border-black rounded-xl p-5 bg-neutral-50">
            <summary className="font-heading font-bold cursor-pointer">More worked examples</summary>
            <div className="mt-4 space-y-4">
              {topic.worked_examples.map((ex, i) => (
                <div key={i} className="border-2 border-black rounded-lg p-4 bg-white">
                  <p className="font-bold mb-2">{ex.problem}</p>
                  <pre className="font-mono text-sm whitespace-pre-wrap leading-relaxed text-neutral-700">{ex.solution}</pre>
                </div>
              ))}
            </div>
          </details>
        )}
      </div>
    </div>
  );
}
