import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import { ArrowLeft, Brain, Lightbulb, CheckCircle, ChevronDown, ChevronUp, BookOpen } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { markTopicViewed } from "@/utils/progress";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const CATEGORY_COLORS = {
  "Number": { bg: "bg-blue-50", text: "text-blue-600", pill: "bg-blue-600", border: "border-blue-600" },
  "Algebra": { bg: "bg-violet-50", text: "text-violet-600", pill: "bg-violet-600", border: "border-violet-600" },
  "Ratio & Proportion": { bg: "bg-orange-50", text: "text-orange-600", pill: "bg-orange-600", border: "border-orange-600" },
  "Geometry & Measures": { bg: "bg-green-50", text: "text-green-600", pill: "bg-green-600", border: "border-green-600" },
  "Probability & Statistics": { bg: "bg-pink-50", text: "text-pink-600", pill: "bg-pink-600", border: "border-pink-600" },
};

export default function TopicDetailPage() {
  const { topicId } = useParams();
  const [topic, setTopic] = useState(null);
  const [loading, setLoading] = useState(true);
  const [expandedExample, setExpandedExample] = useState(null);

  useEffect(() => {
    fetchTopic();
  }, [topicId]);

  const fetchTopic = async () => {
    try {
      const res = await axios.get(`${API}/topics/${topicId}`);
      setTopic(res.data);
      markTopicViewed(topicId);
    } catch (e) {
      console.error("Error fetching topic:", e);
    } finally {
      setLoading(false);
    }
  };

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
        </div>
      </section>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Explanation */}
        <div data-testid="topic-explanation" className="neo-card-static mb-10">
          <div className="flex items-center gap-2 mb-6">
            <BookOpen size={20} className={colors.text} />
            <h2 className="font-heading text-2xl font-bold">Explanation</h2>
          </div>
          <div className="markdown-content prose max-w-none">
            <ReactMarkdown>{topic.explanation}</ReactMarkdown>
          </div>
        </div>

        {/* Key Points */}
        {topic.key_points && topic.key_points.length > 0 && (
          <div data-testid="topic-key-points" className="neo-card-static mb-10 border-yellow-500">
            <div className="flex items-center gap-2 mb-4">
              <Lightbulb size={20} className="text-yellow-600" />
              <h2 className="font-heading text-2xl font-bold">Key Points to Remember</h2>
            </div>
            <ul className="space-y-3">
              {topic.key_points.map((point, i) => (
                <li key={i} className="flex items-start gap-3">
                  <CheckCircle size={18} className="text-green-600 mt-0.5 flex-shrink-0" />
                  <span className="text-neutral-700">{point}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Worked Examples */}
        {topic.worked_examples && topic.worked_examples.length > 0 && (
          <div data-testid="topic-worked-examples" className="mb-10">
            <h2 className="font-heading text-2xl font-bold mb-6 flex items-center gap-2">
              <Brain size={22} className={colors.text} />
              Worked Examples
            </h2>
            <div className="space-y-4">
              {topic.worked_examples.map((ex, i) => (
                <div key={i} className="border-2 border-black rounded-xl overflow-hidden">
                  <button
                    data-testid={`worked-example-${i}`}
                    onClick={() => setExpandedExample(expandedExample === i ? null : i)}
                    className="w-full p-5 flex items-center justify-between bg-white hover:bg-neutral-50 transition-colors text-left"
                  >
                    <div>
                      <span className={`text-xs font-bold ${colors.text} uppercase tracking-wide`}>Example {i + 1}</span>
                      <p className="font-bold mt-1">{ex.problem}</p>
                    </div>
                    {expandedExample === i ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </button>
                  {expandedExample === i && (
                    <div className="p-5 border-t-2 border-black bg-neutral-50">
                      <p className="text-xs font-bold text-green-600 uppercase tracking-wide mb-2">Solution</p>
                      <pre className="font-mono text-sm whitespace-pre-wrap leading-relaxed">{ex.solution}</pre>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-4 pt-4">
          <Link
            to={`/quiz/${topicId}`}
            data-testid="topic-quiz-btn"
            className="neo-btn-primary inline-flex items-center gap-2"
          >
            <Brain size={18} />
            Practice Quiz
          </Link>
          <Link
            to={`/ai-tutor?topic=${encodeURIComponent(topic.title)}`}
            data-testid="topic-ai-tutor-btn"
            className="neo-btn bg-white text-black hover:bg-neutral-50 inline-flex items-center gap-2"
          >
            <Lightbulb size={18} />
            Ask AI Tutor
          </Link>
        </div>
      </div>
    </div>
  );
}
