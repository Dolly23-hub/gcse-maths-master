import { useState, useEffect } from "react";
import axios from "axios";
import { Calculator, Search, ChevronDown, ChevronUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const CATEGORY_COLORS = {
  "Number": { bg: "bg-blue-50", text: "text-blue-600", pill: "bg-blue-600" },
  "Algebra": { bg: "bg-violet-50", text: "text-violet-600", pill: "bg-violet-600" },
  "Ratio & Proportion": { bg: "bg-orange-50", text: "text-orange-600", pill: "bg-orange-600" },
  "Geometry & Measures": { bg: "bg-green-50", text: "text-green-600", pill: "bg-green-600" },
  "Probability & Statistics": { bg: "bg-pink-50", text: "text-pink-600", pill: "bg-pink-600" },
};

export default function FormulaSheetPage() {
  const [formulas, setFormulas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedFormula, setExpandedFormula] = useState(null);

  useEffect(() => {
    fetchFormulas();
  }, []);

  const fetchFormulas = async () => {
    try {
      const res = await axios.get(`${API}/formulas`);
      setFormulas(res.data.formulas);
    } catch (e) {
      console.error("Error fetching formulas:", e);
    } finally {
      setLoading(false);
    }
  };

  const filtered = formulas.filter(
    (f) =>
      f.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      f.formula.toLowerCase().includes(searchQuery.toLowerCase()) ||
      f.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const grouped = {};
  filtered.forEach((f) => {
    if (!grouped[f.category]) grouped[f.category] = [];
    grouped[f.category].push(f);
  });

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="py-12 sm:py-16 border-b-2 border-black bg-neutral-50 dot-pattern">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 data-testid="formula-sheet-title" className="font-heading text-4xl sm:text-5xl font-bold mb-3">
            Formula Sheet
          </h1>
          <p className="text-neutral-500 text-base sm:text-lg max-w-xl">
            All the key GCSE Maths formulas in one place. Your quick reference guide.
          </p>
        </div>
      </section>

      {/* Search */}
      <section className="border-b-2 border-black bg-white sticky top-16 z-40">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="relative">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
            <input
              data-testid="formula-search-input"
              type="text"
              placeholder="Search formulas..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 border-2 border-black rounded-lg focus:outline-none focus:shadow-hard transition-shadow font-body"
            />
          </div>
        </div>
      </section>

      {/* Formulas */}
      <section className="py-12 sm:py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {loading ? (
            <div data-testid="formulas-loading" className="text-center py-12">
              <div className="inline-block w-8 h-8 border-4 border-black border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (
            Object.entries(grouped).map(([category, catFormulas]) => {
              const colors = CATEGORY_COLORS[category] || CATEGORY_COLORS["Number"];
              return (
                <div key={category} className="mb-12" data-testid={`formula-category-${category}`}>
                  <div className="flex items-center gap-3 mb-6">
                    <div className={`w-3 h-8 ${colors.pill} rounded-full`} />
                    <h2 className="font-heading text-2xl font-bold">{category}</h2>
                    <Badge variant="secondary" className="font-mono text-xs">{catFormulas.length}</Badge>
                  </div>
                  <div className="space-y-3">
                    {catFormulas.map((formula) => (
                      <div
                        key={formula.id}
                        data-testid={`formula-card-${formula.id}`}
                        className="border-2 border-black rounded-xl bg-white overflow-hidden"
                      >
                        <button
                          onClick={() => setExpandedFormula(expandedFormula === formula.id ? null : formula.id)}
                          className="w-full p-4 sm:p-5 flex items-center justify-between hover:bg-neutral-50 transition-colors text-left gap-4"
                        >
                          <div className="flex items-center gap-4 flex-1 min-w-0">
                            <div className={`w-10 h-10 ${colors.bg} ${colors.text} rounded-lg border-2 border-black flex items-center justify-center flex-shrink-0`}>
                              <Calculator size={18} />
                            </div>
                            <div className="min-w-0">
                              <p className="font-bold truncate">{formula.name}</p>
                              <p className="font-mono text-sm text-neutral-600 truncate">{formula.formula}</p>
                            </div>
                          </div>
                          {expandedFormula === formula.id ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                        </button>

                        {expandedFormula === formula.id && (
                          <div className="border-t-2 border-black p-5 bg-neutral-50">
                            <p className="text-sm text-neutral-600 mb-3">{formula.description}</p>
                            <div className="bg-white border-2 border-black rounded-lg p-4">
                              <p className="text-xs font-bold text-neutral-400 uppercase tracking-wide mb-1">Example</p>
                              <p className="font-mono text-sm">{formula.usage_example}</p>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
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
