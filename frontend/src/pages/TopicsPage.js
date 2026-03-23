import { useState, useEffect } from "react";
import { Link, useSearchParams } from "react-router-dom";
import axios from "axios";
import { BookOpen, ChevronRight, Search, Filter, CheckCircle2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { getTopicsViewed, getQuizScore } from "@/utils/progress";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const CATEGORY_COLORS = {
  "Number": { bg: "bg-blue-50", text: "text-blue-600", border: "border-blue-600", pill: "bg-blue-600" },
  "Algebra": { bg: "bg-violet-50", text: "text-violet-600", border: "border-violet-600", pill: "bg-violet-600" },
  "Ratio & Proportion": { bg: "bg-orange-50", text: "text-orange-600", border: "border-orange-600", pill: "bg-orange-600" },
  "Geometry & Measures": { bg: "bg-green-50", text: "text-green-600", border: "border-green-600", pill: "bg-green-600" },
  "Probability & Statistics": { bg: "bg-pink-50", text: "text-pink-600", border: "border-pink-600", pill: "bg-pink-600" },
};

const CATEGORIES = ["All", "Number", "Algebra", "Ratio & Proportion", "Geometry & Measures", "Probability & Statistics"];

export default function TopicsPage() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchParams, setSearchParams] = useSearchParams();
  const activeCategory = searchParams.get("category") || "All";

  useEffect(() => {
    fetchTopics();
  }, []);

  const fetchTopics = async () => {
    try {
      const res = await axios.get(`${API}/topics`);
      setTopics(res.data.topics);
    } catch (e) {
      console.error("Error fetching topics:", e);
    } finally {
      setLoading(false);
    }
  };

  const filteredTopics = topics.filter((t) => {
    const matchesCategory = activeCategory === "All" || t.category === activeCategory;
    const matchesSearch = t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          t.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const groupedTopics = {};
  filteredTopics.forEach((t) => {
    if (!groupedTopics[t.category]) groupedTopics[t.category] = [];
    groupedTopics[t.category].push(t);
  });

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="py-12 sm:py-16 border-b-2 border-black bg-neutral-50 dot-pattern">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 data-testid="topics-page-title" className="font-heading text-4xl sm:text-5xl font-bold mb-3">
            GCSE Maths Topics
          </h1>
          <p className="text-neutral-500 text-base sm:text-lg max-w-xl">
            Every topic explained simply. Click on any topic to learn more.
          </p>
        </div>
      </section>

      {/* Search + Filter */}
      <section className="border-b-2 border-black bg-white sticky top-16 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col sm:flex-row gap-4">
            {/* Search */}
            <div className="relative flex-1">
              <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
              <input
                data-testid="topics-search-input"
                type="text"
                placeholder="Search topics..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border-2 border-black rounded-lg focus:outline-none focus:shadow-hard transition-shadow font-body"
              />
            </div>
            {/* Category filter pills */}
            <div className="flex flex-wrap gap-2">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat}
                  data-testid={`filter-${cat.toLowerCase().replace(/\s+/g, "-")}`}
                  onClick={() => setSearchParams(cat === "All" ? {} : { category: cat })}
                  className={`px-3 py-1.5 rounded-lg text-sm font-bold border-2 border-black transition-all duration-200 ${
                    activeCategory === cat
                      ? "bg-black text-white shadow-hard-sm"
                      : "bg-white text-black hover:bg-neutral-100"
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Topics Grid */}
      <section className="py-12 sm:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {loading ? (
            <div data-testid="topics-loading" className="text-center py-12">
              <div className="inline-block w-8 h-8 border-4 border-black border-t-transparent rounded-full animate-spin" />
              <p className="mt-4 text-neutral-500">Loading topics...</p>
            </div>
          ) : filteredTopics.length === 0 ? (
            <div data-testid="topics-empty" className="text-center py-12">
              <p className="text-neutral-500">No topics found. Try a different search or category.</p>
            </div>
          ) : (
            Object.entries(groupedTopics).map(([category, catTopics]) => {
              const colors = CATEGORY_COLORS[category] || CATEGORY_COLORS["Number"];
              return (
                <div key={category} className="mb-12" data-testid={`category-group-${category}`}>
                  <div className="flex items-center gap-3 mb-6">
                    <div className={`w-3 h-8 ${colors.pill} rounded-full`} />
                    <h2 className="font-heading text-2xl font-bold">{category}</h2>
                    <Badge variant="secondary" className="font-mono text-xs">{catTopics.length} topics</Badge>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {catTopics.map((topic) => {
                      const viewed = getTopicsViewed().includes(topic.id);
                      const quizResult = getQuizScore(topic.id);
                      return (
                        <Link
                          key={topic.id}
                          to={`/topics/${topic.id}`}
                          data-testid={`topic-card-${topic.id}`}
                          className={`neo-card cursor-pointer group ${colors.border}`}
                        >
                          <div className="flex items-start justify-between mb-3">
                            <div className={`w-10 h-10 rounded-lg ${colors.bg} ${colors.text} flex items-center justify-center border-2 border-black`}>
                              <BookOpen size={18} />
                            </div>
                            <div className="flex items-center gap-2">
                              {viewed && (
                                <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center" title="Studied">
                                  <CheckCircle2 size={14} className="text-green-600" />
                                </div>
                              )}
                              <Badge variant="outline" className="font-mono text-xs border-2">{topic.tier}</Badge>
                            </div>
                          </div>
                          <h3 className="font-heading text-lg font-bold mb-2 group-hover:underline">{topic.title}</h3>
                          <p className="text-sm text-neutral-500 leading-relaxed line-clamp-2">{topic.description}</p>
                          <div className="mt-4 flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <div className="flex items-center gap-1">
                                {[1, 2, 3, 4, 5].map((d) => (
                                  <div
                                    key={d}
                                    className={`w-2 h-2 rounded-full ${d <= topic.difficulty ? colors.pill : "bg-neutral-200"}`}
                                  />
                                ))}
                              </div>
                              {quizResult && (
                                <span className="text-xs font-mono text-green-600 font-bold ml-1">
                                  {quizResult.score}/{quizResult.total}
                                </span>
                              )}
                            </div>
                            <ChevronRight size={18} className="text-neutral-400 group-hover:text-black transition-colors" />
                          </div>
                        </Link>
                      );
                    })}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </section>
    </div>
  );
}
