import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { BookOpen, FileText, Brain, Calculator, FlaskConical, ArrowRight, Star, ChevronRight, Clock, TrendingUp, Trophy, Target } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { getOverallProgress, getTopicsViewed, getTotalQuizScore } from "@/utils/progress";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const CATEGORIES = [
  { name: "Number", color: "bg-blue-600", textColor: "text-blue-600", icon: "1+2", count: "" },
  { name: "Algebra", color: "bg-violet-600", textColor: "text-violet-600", icon: "x=y", count: "" },
  { name: "Ratio & Proportion", color: "bg-orange-600", textColor: "text-orange-600", icon: "3:5", count: "" },
  { name: "Geometry & Measures", color: "bg-green-600", textColor: "text-green-600", icon: "GEO", count: "" },
  { name: "Probability & Statistics", color: "bg-pink-600", textColor: "text-pink-600", icon: "P(x)", count: "" },
];

const FEATURES = [
  {
    icon: BookOpen,
    title: "Topic Explanations",
    description: "Every GCSE Maths topic explained clearly with worked examples and key points",
    link: "/topics",
    color: "border-blue-600",
  },
  {
    icon: FileText,
    title: "Past Papers",
    description: "Practice with questions from Edexcel, AQA, and OCR boards across multiple years",
    link: "/past-papers",
    color: "border-pink-600",
  },
  {
    icon: Brain,
    title: "Interactive Quizzes",
    description: "Test yourself with instant feedback and detailed explanations on every question",
    link: "/quiz",
    color: "border-orange-600",
  },
  {
    icon: Calculator,
    title: "Formula Sheet",
    description: "All the key formulas you need in one quick reference with usage examples",
    link: "/formulas",
    color: "border-green-600",
  },
  {
    icon: FlaskConical,
    title: "AI Tutor",
    description: "Ask anything and get step-by-step help from your AI maths tutor powered by GPT",
    link: "/ai-tutor",
    color: "border-violet-600",
  },
];

// Exam countdown: 2026 dates
const EXAM_DATES = [
  { board: "All Boards", paper: "Paper 1 (Non-Calculator)", date: new Date("2026-05-14T09:00:00"), color: "bg-blue-600" },
  { board: "All Boards", paper: "Paper 2 (Calculator)", date: new Date("2026-06-03T09:00:00"), color: "bg-pink-600" },
  { board: "All Boards", paper: "Paper 3 (Calculator)", date: new Date("2026-06-10T09:00:00"), color: "bg-orange-600" },
];

function getCountdown(targetDate) {
  const now = new Date();
  const diff = targetDate - now;
  if (diff <= 0) return { days: 0, hours: 0, expired: true };
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  return { days, hours, expired: false };
}

export default function HomePage() {
  const [stats, setStats] = useState({ topics: 0, quizzes: 0, papers: 0, formulas: 0, categories: 5 });
  const [categoryCounts, setCategoryCounts] = useState({});
  const [countdown, setCountdown] = useState(getCountdown(EXAM_DATES[0].date));

  useEffect(() => {
    fetchStats();
    fetchTopicsForCounts();
    const timer = setInterval(() => setCountdown(getCountdown(EXAM_DATES[0].date)), 60000);
    return () => clearInterval(timer);
  }, []);

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API}/stats`);
      setStats(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchTopicsForCounts = async () => {
    try {
      const res = await axios.get(`${API}/topics`);
      const counts = {};
      res.data.topics.forEach(t => {
        counts[t.category] = (counts[t.category] || 0) + 1;
      });
      setCategoryCounts(counts);
    } catch (e) {
      console.error(e);
    }
  };

  const viewedTopics = getTopicsViewed();
  const progressPercent = getOverallProgress(stats.topics);
  const quizScore = getTotalQuizScore();

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section data-testid="hero-section" className="relative py-16 sm:py-24 lg:py-32 overflow-hidden bg-blue-50">
        <div className="absolute top-10 right-10 w-64 h-64 bg-blue-200 rounded-full opacity-60 blur-3xl" />
        <div className="absolute bottom-0 left-20 w-80 h-80 bg-violet-200 rounded-full opacity-50 blur-3xl" />
        <div className="absolute top-1/2 right-1/3 w-48 h-48 bg-pink-200 rounded-full opacity-40 blur-3xl" />
        <div className="absolute inset-0 dot-pattern opacity-30" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-bold mb-6 animate-fade-in-up border-2 border-black shadow-hard-sm">
              <Star size={14} />
              Free GCSE Maths Revision
            </div>
            <h1
              data-testid="hero-title"
              className="font-heading text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6 animate-fade-in-up stagger-1 text-slate-900"
            >
              Ace your <span className="text-blue-600">GCSE Maths</span> exam with confidence
            </h1>
            <p
              data-testid="hero-subtitle"
              className="text-base sm:text-lg text-slate-600 mb-8 max-w-2xl leading-relaxed animate-fade-in-up stagger-2"
            >
              Everything you need to smash your maths GCSE. Clear explanations, past paper practice, 
              interactive quizzes, and an AI tutor that never gets tired of your questions.
            </p>
            <div className="flex flex-wrap gap-4 animate-fade-in-up stagger-3">
              <Link
                to="/topics"
                data-testid="hero-start-learning-btn"
                className="neo-btn-primary inline-flex items-center gap-2"
              >
                Start Learning
                <ArrowRight size={18} />
              </Link>
              <Link
                to="/ai-tutor"
                data-testid="hero-ai-tutor-btn"
                className="neo-btn bg-white text-black hover:bg-blue-50 border-2 border-black"
              >
                Ask AI Tutor
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Exam Countdown */}
      <section data-testid="exam-countdown" className="border-y-2 border-black bg-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-3 mb-4">
            <Clock size={20} className="text-yellow-400" />
            <h3 className="font-heading font-bold text-lg">2026 GCSE Exam Countdown</h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {EXAM_DATES.map((exam, i) => {
              const cd = getCountdown(exam.date);
              return (
                <div key={i} data-testid={`countdown-${i}`} className="bg-slate-800 rounded-xl p-4 border border-slate-700">
                  <div className="flex items-center gap-2 mb-2">
                    <div className={`w-3 h-3 rounded-full ${exam.color}`} />
                    <span className="text-xs text-slate-400 font-bold uppercase">{exam.board}</span>
                  </div>
                  <p className="font-medium text-sm mb-2">{exam.paper}</p>
                  <p className="text-xs text-slate-500 mb-1">{exam.date.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })}</p>
                  {cd.expired ? (
                    <span className="text-green-400 font-bold text-sm">Completed</span>
                  ) : (
                    <span className="font-heading font-bold text-2xl text-yellow-400">{cd.days} <span className="text-sm text-slate-400">days</span></span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Progress Bar (if user has started) */}
      {viewedTopics.length > 0 && (
        <section data-testid="progress-section" className="border-b-2 border-black bg-emerald-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-emerald-600 text-white rounded-lg border-2 border-black flex items-center justify-center">
                  <TrendingUp size={20} />
                </div>
                <div>
                  <p className="font-heading font-bold">Your Progress</p>
                  <p className="text-sm text-slate-600">{viewedTopics.length} of {stats.topics} topics studied</p>
                </div>
              </div>
              <div className="flex items-center gap-6">
                <div className="flex-1 sm:w-48">
                  <Progress value={progressPercent} className="h-3 border-2 border-black rounded-full" />
                  <p className="text-xs text-slate-500 mt-1 text-right">{progressPercent}%</p>
                </div>
                {quizScore.total > 0 && (
                  <div className="flex items-center gap-2 bg-white border-2 border-black rounded-lg px-3 py-2 shadow-hard-sm">
                    <Trophy size={16} className="text-yellow-600" />
                    <span className="font-mono text-sm font-bold">{quizScore.correct}/{quizScore.total}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Stats Bar */}
      <section className="border-b-2 border-black bg-violet-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {[
              { stat: `${stats.topics}+`, label: "Topics Covered" },
              { stat: `${stats.quizzes}+`, label: "Quiz Questions" },
              { stat: "3", label: "Exam Boards" },
              { stat: `${stats.formulas}+`, label: "Key Formulas" },
            ].map((item, i) => (
              <div key={i} data-testid={`stat-${i}`}>
                <div className="font-heading text-4xl font-bold">{item.stat}</div>
                <div className="text-sm text-violet-200 font-medium mt-1">{item.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section data-testid="features-section" className="py-16 sm:py-24 bg-amber-50 relative overflow-hidden">
        <div className="absolute -top-20 -right-20 w-72 h-72 bg-orange-200 rounded-full opacity-40 blur-3xl" />
        <div className="absolute bottom-10 left-10 w-56 h-56 bg-yellow-200 rounded-full opacity-40 blur-3xl" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <h2 className="font-heading text-3xl sm:text-4xl font-bold mb-3">
            Everything you need
          </h2>
          <p className="text-slate-600 mb-12 text-base sm:text-lg max-w-xl">
            From topic breakdowns to AI-powered help, we've got your revision sorted.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((feature, i) => {
              const Icon = feature.icon;
              return (
                <Link
                  key={i}
                  to={feature.link}
                  data-testid={`feature-card-${i}`}
                  className={`neo-card cursor-pointer group ${feature.color}`}
                >
                  <div className={`w-12 h-12 rounded-lg border-2 border-black flex items-center justify-center mb-4 ${feature.color.replace('border-', 'bg-').replace('-600', '-50')}`}>
                    <Icon size={24} className={feature.color.replace('border-', 'text-')} />
                  </div>
                  <h3 className="font-heading text-xl font-bold mb-2">{feature.title}</h3>
                  <p className="text-neutral-500 text-sm leading-relaxed">{feature.description}</p>
                  <div className="mt-4 flex items-center gap-1 text-sm font-bold group-hover:gap-2 transition-all">
                    Explore <ChevronRight size={16} />
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* Topic Categories */}
      <section data-testid="categories-section" className="py-16 sm:py-24 bg-green-50 border-y-2 border-black relative overflow-hidden">
        <div className="absolute top-20 right-20 w-72 h-72 bg-green-200 rounded-full opacity-50 blur-3xl" />
        <div className="absolute -bottom-10 left-1/3 w-64 h-64 bg-teal-200 rounded-full opacity-40 blur-3xl" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <h2 className="font-heading text-3xl sm:text-4xl font-bold mb-3">
            GCSE Maths Topics
          </h2>
          <p className="text-slate-600 mb-12 text-base sm:text-lg">
            The complete syllabus, broken down into 5 clear categories.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {CATEGORIES.map((cat, i) => (
              <Link
                key={i}
                to={`/topics?category=${encodeURIComponent(cat.name)}`}
                data-testid={`category-card-${i}`}
                className="neo-card cursor-pointer group flex items-center gap-4"
              >
                <div className={`w-14 h-14 ${cat.color} text-white rounded-lg border-2 border-black flex items-center justify-center font-mono text-sm font-bold flex-shrink-0`}>
                  {cat.icon}
                </div>
                <div>
                  <h3 className="font-heading text-lg font-bold">{cat.name}</h3>
                  <p className="text-sm text-neutral-500">{categoryCounts[cat.name] || 0} topics</p>
                </div>
                <ChevronRight size={20} className="ml-auto text-neutral-400 group-hover:text-black transition-colors" />
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Exam Boards Quick Access */}
      <section data-testid="exam-boards-section" className="py-16 sm:py-24 bg-pink-50 relative overflow-hidden">
        <div className="absolute top-10 left-10 w-60 h-60 bg-pink-200 rounded-full opacity-50 blur-3xl" />
        <div className="absolute bottom-20 right-20 w-56 h-56 bg-rose-200 rounded-full opacity-40 blur-3xl" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <h2 className="font-heading text-3xl sm:text-4xl font-bold mb-3">
            Past Papers by Exam Board
          </h2>
          <p className="text-slate-600 mb-12 text-base sm:text-lg">
            Practice with questions from your specific exam board.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { name: "Edexcel", color: "bg-blue-600", shadow: "neo-shadow-edexcel", desc: "Most popular board (64% of entries). Broad and in-depth, especially algebra and geometry.", tag: "1MA1" },
              { name: "AQA", color: "bg-pink-600", shadow: "neo-shadow-aqa", desc: "Real-world applications focus. Accessible language with gradual difficulty.", tag: "8300" },
              { name: "OCR", color: "bg-orange-600", shadow: "neo-shadow-ocr", desc: "Problem-solving emphasis. Straightforward structure with real-world focus.", tag: "J560" },
            ].map((board, i) => (
              <Link
                key={i}
                to={`/past-papers?board=${board.name}`}
                data-testid={`board-card-${board.name.toLowerCase()}`}
                className={`border-2 border-black rounded-xl p-6 ${board.shadow} transition-all duration-200 hover:-translate-y-1 cursor-pointer group bg-white`}
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className={`${board.color} text-white px-3 py-1 rounded-md border-2 border-black font-heading font-bold text-lg`}>
                    {board.name}
                  </div>
                  <span className="font-mono text-xs text-neutral-400">{board.tag}</span>
                </div>
                <p className="text-sm text-neutral-600 mb-4">{board.desc}</p>
                <div className="flex items-center gap-1 text-sm font-bold group-hover:gap-2 transition-all">
                  View Papers <ArrowRight size={14} />
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Study Tips Section */}
      <section data-testid="study-tips-section" className="py-16 sm:py-24 bg-sky-50 relative overflow-hidden">
        <div className="absolute top-10 right-10 w-56 h-56 bg-sky-200 rounded-full opacity-40 blur-3xl" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <h2 className="font-heading text-3xl sm:text-4xl font-bold mb-3">
            Top Revision Tips
          </h2>
          <p className="text-slate-600 mb-12 text-base sm:text-lg">
            How to get the most out of your GCSE Maths revision.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { num: "01", title: "Little & Often", desc: "30 minutes daily beats 5 hours once a week. Consistency is key!" },
              { num: "02", title: "Practice Papers", desc: "Do past papers under timed conditions. This is the single best way to revise." },
              { num: "03", title: "Show Your Working", desc: "You get marks for method even if the final answer is wrong. Always show steps!" },
              { num: "04", title: "Learn from Mistakes", desc: "When you get something wrong, understand WHY. That's where real learning happens." },
            ].map((tip, i) => (
              <div key={i} data-testid={`study-tip-${i}`} className="neo-card-static">
                <div className="font-heading text-4xl font-bold text-slate-200 mb-3">{tip.num}</div>
                <h3 className="font-heading text-lg font-bold mb-2">{tip.title}</h3>
                <p className="text-sm text-slate-600 leading-relaxed">{tip.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 sm:py-24 bg-blue-600 text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-10 left-20 w-32 h-32 border-4 border-white rounded-full" />
          <div className="absolute bottom-10 right-32 w-24 h-24 border-4 border-white rounded-lg rotate-45" />
          <div className="absolute top-1/2 left-1/2 w-40 h-40 border-4 border-white rounded-full" />
          <div className="absolute top-20 right-1/4 w-16 h-16 border-4 border-white" />
        </div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative">
          <h2 className="font-heading text-3xl sm:text-4xl font-bold mb-4">
            Ready to smash your GCSE?
          </h2>
          <p className="text-blue-100 mb-8 max-w-lg mx-auto">
            Start revising now with clear explanations, practice questions, and AI-powered help.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              to="/topics"
              data-testid="cta-start-btn"
              className="neo-btn bg-white text-blue-700 border-2 border-black hover:bg-blue-50 font-bold"
            >
              Start Revising
            </Link>
            <Link
              to="/ai-tutor"
              data-testid="cta-ai-btn"
              className="neo-btn bg-transparent text-white border-2 border-white hover:bg-white/10 font-bold"
            >
              Try AI Tutor
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t-2 border-black py-8 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="font-heading font-bold text-sm">
              GCSE Maths Master
            </div>
            <div className="text-sm text-slate-500">
              Covering Edexcel, AQA & OCR exam boards
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
