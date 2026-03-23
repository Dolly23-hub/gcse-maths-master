import { useState, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import { toast } from "sonner";
import {
  CalendarDays, Clock, Target, ChevronDown, ChevronUp,
  Sparkles, Loader2, BookOpen, Brain, FileText, ArrowRight,
  CheckCircle2, AlertTriangle, Star
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Link } from "react-router-dom";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const CATEGORIES = [
  { name: "Number", color: "bg-blue-600", lightBg: "bg-blue-50", text: "text-blue-600" },
  { name: "Algebra", color: "bg-violet-600", lightBg: "bg-violet-50", text: "text-violet-600" },
  { name: "Ratio & Proportion", color: "bg-orange-600", lightBg: "bg-orange-50", text: "text-orange-600" },
  { name: "Geometry & Measures", color: "bg-green-600", lightBg: "bg-green-50", text: "text-green-600" },
  { name: "Probability & Statistics", color: "bg-pink-600", lightBg: "bg-pink-50", text: "text-pink-600" },
];

const BOARDS = ["Edexcel", "AQA", "OCR"];

const CONFIDENCE_LABELS = {
  1: "Very Weak",
  2: "Weak",
  3: "OK",
  4: "Good",
  5: "Strong",
};

const CONFIDENCE_COLORS = {
  1: "bg-red-500",
  2: "bg-orange-500",
  3: "bg-yellow-500",
  4: "bg-green-400",
  5: "bg-green-600",
};

export default function RevisionPlannerPage() {
  const [step, setStep] = useState(1); // 1: setup, 2: results
  const [board, setBoard] = useState("Edexcel");
  const [examDate, setExamDate] = useState("2026-05-14");
  const [studyHours, setStudyHours] = useState(1);
  const [confidence, setConfidence] = useState({
    "Number": 3,
    "Algebra": 3,
    "Ratio & Proportion": 3,
    "Geometry & Measures": 3,
    "Probability & Statistics": 3,
  });
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState(null);
  const [expandedWeek, setExpandedWeek] = useState(null);

  const handleConfidenceChange = (category, value) => {
    setConfidence((prev) => ({ ...prev, [category]: value }));
  };

  const generatePlan = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/revision-plan`, {
        exam_board: board,
        exam_date: examDate,
        confidence,
        study_hours_per_day: studyHours,
        use_ai: true,
      });
      setPlan(res.data);
      setStep(2);
      toast.success("Your revision plan is ready!");
    } catch (e) {
      console.error(e);
      toast.error(e.response?.data?.detail || "Failed to generate plan. Check your exam date.");
    } finally {
      setLoading(false);
    }
  };

  const getCategoryConfig = (name) => {
    return CATEGORIES.find((c) => c.name === name) || CATEGORIES[0];
  };

  // Step 1: Setup form
  if (step === 1) {
    return (
      <div className="min-h-screen">
        {/* Header */}
        <section className="py-12 sm:py-16 border-b-2 border-black bg-indigo-50 dot-pattern relative overflow-hidden">
          <div className="absolute top-10 right-10 w-64 h-64 bg-indigo-200 rounded-full opacity-50 blur-3xl" />
          <div className="absolute bottom-0 left-20 w-56 h-56 bg-purple-200 rounded-full opacity-40 blur-3xl" />
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 relative">
            <h1 data-testid="planner-title" className="font-heading text-4xl sm:text-5xl font-bold mb-3">
              Revision Planner
            </h1>
            <p className="text-slate-600 text-base sm:text-lg">
              Tell us about yourself and we'll create a personalised study schedule with AI-powered tips.
            </p>
          </div>
        </section>

        <section className="py-12 sm:py-16">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Exam Board */}
            <div data-testid="planner-board-section" className="neo-card-static mb-8">
              <h2 className="font-heading text-xl font-bold mb-4 flex items-center gap-2">
                <FileText size={20} />
                Which exam board are you doing?
              </h2>
              <div className="flex flex-wrap gap-3">
                {BOARDS.map((b) => (
                  <button
                    key={b}
                    data-testid={`planner-board-${b.toLowerCase()}`}
                    onClick={() => setBoard(b)}
                    className={`px-5 py-3 rounded-lg font-bold border-2 border-black transition-all duration-200 ${
                      board === b
                        ? "bg-black text-white shadow-hard-sm"
                        : "bg-white text-black hover:bg-neutral-100"
                    }`}
                  >
                    {b}
                  </button>
                ))}
              </div>
            </div>

            {/* Exam Date */}
            <div data-testid="planner-date-section" className="neo-card-static mb-8">
              <h2 className="font-heading text-xl font-bold mb-4 flex items-center gap-2">
                <CalendarDays size={20} />
                When is your first exam?
              </h2>
              <input
                data-testid="planner-exam-date"
                type="date"
                value={examDate}
                onChange={(e) => setExamDate(e.target.value)}
                className="w-full sm:w-auto px-4 py-3 border-2 border-black rounded-lg font-mono focus:outline-none focus:shadow-hard transition-shadow"
              />
              <p className="text-sm text-slate-500 mt-2">
                2026 GCSE Maths Paper 1: 14 May 2026 | Paper 2: 3 June 2026 | Paper 3: 10 June 2026
              </p>
            </div>

            {/* Study Hours */}
            <div data-testid="planner-hours-section" className="neo-card-static mb-8">
              <h2 className="font-heading text-xl font-bold mb-4 flex items-center gap-2">
                <Clock size={20} />
                How many hours per day can you study?
              </h2>
              <div className="flex flex-wrap gap-3">
                {[0.5, 1, 1.5, 2, 3].map((h) => (
                  <button
                    key={h}
                    data-testid={`planner-hours-${h}`}
                    onClick={() => setStudyHours(h)}
                    className={`px-4 py-2.5 rounded-lg font-bold border-2 border-black transition-all duration-200 ${
                      studyHours === h
                        ? "bg-black text-white shadow-hard-sm"
                        : "bg-white text-black hover:bg-neutral-100"
                    }`}
                  >
                    {h} hr{h !== 1 ? "s" : ""}
                  </button>
                ))}
              </div>
            </div>

            {/* Confidence Rating */}
            <div data-testid="planner-confidence-section" className="neo-card-static mb-8">
              <h2 className="font-heading text-xl font-bold mb-2 flex items-center gap-2">
                <Target size={20} />
                Rate your confidence in each topic
              </h2>
              <p className="text-sm text-slate-500 mb-6">1 = Very Weak, 5 = Strong. Be honest - this helps us prioritise!</p>
              <div className="space-y-5">
                {CATEGORIES.map((cat) => {
                  const val = confidence[cat.name];
                  return (
                    <div key={cat.name} data-testid={`confidence-${cat.name.toLowerCase().replace(/\s+/g, "-")}`}>
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <div className={`w-3 h-6 rounded-full ${cat.color}`} />
                          <span className="font-bold text-sm">{cat.name}</span>
                        </div>
                        <Badge className={`${CONFIDENCE_COLORS[val]} text-white border-0 text-xs`}>
                          {CONFIDENCE_LABELS[val]}
                        </Badge>
                      </div>
                      <div className="flex gap-2">
                        {[1, 2, 3, 4, 5].map((level) => (
                          <button
                            key={level}
                            onClick={() => handleConfidenceChange(cat.name, level)}
                            className={`flex-1 py-2 rounded-lg border-2 border-black text-sm font-bold transition-all duration-200 ${
                              val >= level
                                ? `${CONFIDENCE_COLORS[level]} text-white`
                                : "bg-white text-black hover:bg-neutral-50"
                            }`}
                          >
                            {level}
                          </button>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Generate Button */}
            <button
              data-testid="planner-generate-btn"
              onClick={generatePlan}
              disabled={loading}
              className="neo-btn-primary w-full text-lg py-4 flex items-center justify-center gap-3"
            >
              {loading ? (
                <>
                  <Loader2 size={22} className="animate-spin" />
                  Generating your plan...
                </>
              ) : (
                <>
                  <Sparkles size={22} />
                  Generate My Revision Plan
                </>
              )}
            </button>
          </div>
        </section>
      </div>
    );
  }

  // Step 2: Results
  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="py-10 sm:py-14 border-b-2 border-black bg-indigo-50 relative overflow-hidden">
        <div className="absolute top-10 right-10 w-56 h-56 bg-indigo-200 rounded-full opacity-50 blur-3xl" />
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 data-testid="plan-results-title" className="font-heading text-3xl sm:text-4xl font-bold mb-2">
                Your Revision Plan
              </h1>
              <p className="text-slate-600 text-sm sm:text-base">
                Personalised for {plan.exam_board} GCSE Maths
              </p>
            </div>
            <button
              data-testid="planner-edit-btn"
              onClick={() => setStep(1)}
              className="neo-btn bg-white text-black text-sm"
            >
              Edit Settings
            </button>
          </div>
        </div>
      </section>

      {/* Summary Cards */}
      <section className="border-b-2 border-black bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div data-testid="plan-days" className="neo-card-static text-center p-4">
              <div className="font-heading text-3xl font-bold text-blue-600">{plan.days_remaining}</div>
              <div className="text-xs text-slate-500 font-medium mt-1">Days Left</div>
            </div>
            <div data-testid="plan-weeks" className="neo-card-static text-center p-4">
              <div className="font-heading text-3xl font-bold text-violet-600">{plan.weeks_remaining}</div>
              <div className="text-xs text-slate-500 font-medium mt-1">Weeks</div>
            </div>
            <div data-testid="plan-topics" className="neo-card-static text-center p-4">
              <div className="font-heading text-3xl font-bold text-orange-600">{plan.total_topics}</div>
              <div className="text-xs text-slate-500 font-medium mt-1">Topics</div>
            </div>
            <div data-testid="plan-board" className="neo-card-static text-center p-4">
              <div className="font-heading text-xl font-bold text-pink-600">{plan.exam_board}</div>
              <div className="text-xs text-slate-500 font-medium mt-1">Board</div>
            </div>
          </div>
        </div>
      </section>

      {/* Weak & Strong Areas */}
      <section className="border-b-2 border-black bg-neutral-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {plan.weak_areas.length > 0 && (
              <div data-testid="plan-weak-areas" className="flex items-start gap-3 bg-red-50 border-2 border-red-300 rounded-xl p-4">
                <AlertTriangle size={20} className="text-red-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="font-bold text-sm text-red-700">Priority Areas</p>
                  <p className="text-sm text-red-600">{plan.weak_areas.join(", ")}</p>
                </div>
              </div>
            )}
            {plan.strong_areas.length > 0 && (
              <div data-testid="plan-strong-areas" className="flex items-start gap-3 bg-green-50 border-2 border-green-300 rounded-xl p-4">
                <CheckCircle2 size={20} className="text-green-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="font-bold text-sm text-green-700">Strong Areas</p>
                  <p className="text-sm text-green-600">{plan.strong_areas.join(", ")}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* AI Tips */}
      {plan.ai_tips && plan.ai_tips.length > 0 && (
        <section data-testid="plan-ai-tips" className="border-b-2 border-black bg-amber-50">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <h2 className="font-heading text-xl font-bold mb-4 flex items-center gap-2">
              <Sparkles size={20} className="text-amber-600" />
              AI Personalised Tips
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {plan.ai_tips.map((tip, i) => (
                <div key={i} className="bg-white border-2 border-black rounded-lg p-4 shadow-hard-sm">
                  <div className="flex items-start gap-3">
                    <div className="w-7 h-7 bg-amber-500 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 border-2 border-black">
                      {i + 1}
                    </div>
                    <p className="text-sm leading-relaxed">{tip}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Weekly Schedule */}
      <section className="py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="font-heading text-2xl font-bold mb-6 flex items-center gap-2">
            <CalendarDays size={24} />
            Weekly Schedule
          </h2>
          <div className="space-y-4">
            {plan.schedule.map((week) => {
              const catConfig = getCategoryConfig(week.focus_category);
              const isExpanded = expandedWeek === week.week;
              const startDate = new Date(week.start_date);
              const endDate = new Date(week.end_date);
              const formatDate = (d) => d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });

              return (
                <div
                  key={week.week}
                  data-testid={`schedule-week-${week.week}`}
                  className="border-2 border-black rounded-xl bg-white overflow-hidden"
                >
                  <button
                    onClick={() => setExpandedWeek(isExpanded ? null : week.week)}
                    className="w-full p-5 flex items-center justify-between hover:bg-neutral-50 transition-colors text-left"
                  >
                    <div className="flex items-center gap-4">
                      <div className={`w-12 h-12 ${catConfig.color} text-white rounded-lg border-2 border-black flex items-center justify-center font-heading font-bold`}>
                        W{week.week}
                      </div>
                      <div>
                        <p className="font-bold">Week {week.week}: {week.focus_category}</p>
                        <p className="text-sm text-slate-500">
                          {formatDate(startDate)} - {formatDate(endDate)} | {week.topics.length} topic{week.topics.length !== 1 ? "s" : ""}
                        </p>
                      </div>
                    </div>
                    {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </button>

                  {isExpanded && (
                    <div className="border-t-2 border-black p-5 bg-neutral-50">
                      {/* Activities */}
                      <div className="mb-5">
                        <h4 className="font-bold text-sm mb-3 uppercase tracking-wide text-slate-500">What to do</h4>
                        <ul className="space-y-2">
                          {week.activities.map((act, i) => (
                            <li key={i} className="flex items-start gap-2 text-sm">
                              <CheckCircle2 size={16} className="text-green-600 mt-0.5 flex-shrink-0" />
                              <span>{act}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* Topics */}
                      {week.topics.length > 0 && (
                        <div>
                          <h4 className="font-bold text-sm mb-3 uppercase tracking-wide text-slate-500">Topics to cover</h4>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {week.topics.map((topic) => {
                              const tc = getCategoryConfig(topic.category);
                              return (
                                <Link
                                  key={topic.id}
                                  to={`/topics/${topic.id}`}
                                  data-testid={`plan-topic-${topic.id}`}
                                  className="flex items-center gap-3 bg-white border-2 border-black rounded-lg p-3 hover:shadow-hard-sm transition-all group"
                                >
                                  <div className={`w-8 h-8 ${tc.lightBg} ${tc.text} rounded-md border border-black flex items-center justify-center`}>
                                    <BookOpen size={14} />
                                  </div>
                                  <div className="flex-1 min-w-0">
                                    <p className="font-bold text-sm truncate group-hover:underline">{topic.title}</p>
                                    <div className="flex items-center gap-1">
                                      {[1, 2, 3, 4, 5].map((d) => (
                                        <div key={d} className={`w-1.5 h-1.5 rounded-full ${d <= topic.difficulty ? tc.color : "bg-neutral-200"}`} />
                                      ))}
                                    </div>
                                  </div>
                                  <ArrowRight size={14} className="text-neutral-400 group-hover:text-black" />
                                </Link>
                              );
                            })}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Quick Actions */}
      <section className="py-8 border-t-2 border-black bg-neutral-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap gap-4 justify-center">
            <Link
              to="/topics"
              data-testid="plan-go-topics"
              className="neo-btn-primary inline-flex items-center gap-2"
            >
              <BookOpen size={18} /> Start Studying
            </Link>
            <Link
              to="/quiz"
              data-testid="plan-go-quiz"
              className="neo-btn bg-white text-black inline-flex items-center gap-2"
            >
              <Brain size={18} /> Take a Quiz
            </Link>
            <Link
              to={`/past-papers?board=${plan.exam_board}`}
              data-testid="plan-go-papers"
              className="neo-btn bg-white text-black inline-flex items-center gap-2"
            >
              <FileText size={18} /> Past Papers
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
