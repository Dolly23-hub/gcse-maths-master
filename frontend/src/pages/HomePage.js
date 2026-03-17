import { Link } from "react-router-dom";
import { BookOpen, FileText, Brain, Calculator, FlaskConical, ArrowRight, Star, Target, Zap, ChevronRight } from "lucide-react";

const CATEGORIES = [
  { name: "Number", color: "bg-blue-600", textColor: "text-blue-600", icon: "1+2", count: "4 topics" },
  { name: "Algebra", color: "bg-violet-600", textColor: "text-violet-600", icon: "x=y", count: "6 topics" },
  { name: "Ratio & Proportion", color: "bg-orange-600", textColor: "text-orange-600", icon: "3:5", count: "3 topics" },
  { name: "Geometry & Measures", color: "bg-green-600", textColor: "text-green-600", icon: "GEO", count: "4 topics" },
  { name: "Probability & Statistics", color: "bg-pink-600", textColor: "text-pink-600", icon: "P(x)", count: "2 topics" },
];

const FEATURES = [
  {
    icon: BookOpen,
    title: "Topic Explanations",
    description: "Every GCSE Maths topic explained clearly with worked examples",
    link: "/topics",
    color: "border-blue-600",
    shadowColor: "shadow-hard-edexcel",
  },
  {
    icon: FileText,
    title: "Past Papers",
    description: "Practice with questions from Edexcel, AQA, and OCR boards",
    link: "/past-papers",
    color: "border-pink-600",
    shadowColor: "shadow-hard-aqa",
  },
  {
    icon: Brain,
    title: "Interactive Quizzes",
    description: "Test yourself with instant feedback on every question",
    link: "/quiz",
    color: "border-orange-600",
    shadowColor: "shadow-hard-ocr",
  },
  {
    icon: Calculator,
    title: "Formula Sheet",
    description: "All the key formulas you need in one quick reference",
    link: "/formulas",
    color: "border-green-600",
    shadowColor: "hover:shadow-[4px_4px_0px_0px_#16A34A]",
  },
  {
    icon: FlaskConical,
    title: "AI Tutor",
    description: "Ask anything and get step-by-step help from your AI maths tutor",
    link: "/ai-tutor",
    color: "border-violet-600",
    shadowColor: "hover:shadow-[4px_4px_0px_0px_#8B5CF6]",
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section data-testid="hero-section" className="relative py-16 sm:py-24 lg:py-32 overflow-hidden bg-blue-50">
        {/* Decorative colour blobs */}
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

      {/* Stats Bar */}
      <section className="border-y-2 border-black bg-violet-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {[
              { stat: "19+", label: "Topics Covered", emoji: "book" },
              { stat: "25+", label: "Quiz Questions", emoji: "brain" },
              { stat: "3", label: "Exam Boards", emoji: "clipboard" },
              { stat: "20+", label: "Key Formulas", emoji: "calculator" },
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
                  <p className="text-sm text-neutral-500">{cat.count}</p>
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
              { name: "Edexcel", color: "bg-blue-600", shadow: "neo-shadow-edexcel", desc: "Most popular board (64% of entries)", tag: "1MA1" },
              { name: "AQA", color: "bg-pink-600", shadow: "neo-shadow-aqa", desc: "Real-world applications focus", tag: "8300" },
              { name: "OCR", color: "bg-orange-600", shadow: "neo-shadow-ocr", desc: "Problem-solving emphasis", tag: "J560" },
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
