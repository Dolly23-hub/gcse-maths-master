import { useState, useEffect } from "react";
import { useSearchParams, Link } from "react-router-dom";
import axios from "axios";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { FileText, ExternalLink, Calculator, Ban, ChevronDown, ChevronUp, ArrowRight } from "lucide-react";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const BOARD_CONFIG = {
  Edexcel: { color: "bg-blue-600", textColor: "text-blue-600", borderColor: "border-blue-600", shadow: "neo-shadow-edexcel", spec: "1MA1", link: "https://qualifications.pearson.com/en/qualifications/edexcel-gcses/mathematics-2015.html" },
  AQA: { color: "bg-pink-600", textColor: "text-pink-600", borderColor: "border-pink-600", shadow: "neo-shadow-aqa", spec: "8300", link: "https://www.aqa.org.uk/subjects/mathematics/gcse/mathematics-8300" },
  OCR: { color: "bg-orange-600", textColor: "text-orange-600", borderColor: "border-orange-600", shadow: "neo-shadow-ocr", spec: "J560", link: "https://www.ocr.org.uk/qualifications/gcse/mathematics-j560-from-2015/" },
};

export default function PastPapersPage() {
  const [searchParams] = useSearchParams();
  const initialBoard = searchParams.get("board") || "Edexcel";
  const [activeBoard, setActiveBoard] = useState(initialBoard);
  const [papers, setPapers] = useState({});
  const [loading, setLoading] = useState(true);
  const [expandedPaper, setExpandedPaper] = useState(null);

  useEffect(() => {
    fetchAllPapers();
  }, []);

  const fetchAllPapers = async () => {
    try {
      const [edRes, aqaRes, ocrRes] = await Promise.all([
        axios.get(`${API}/past-papers/Edexcel`),
        axios.get(`${API}/past-papers/AQA`),
        axios.get(`${API}/past-papers/OCR`),
      ]);
      setPapers({
        Edexcel: edRes.data.papers,
        AQA: aqaRes.data.papers,
        OCR: ocrRes.data.papers,
      });
    } catch (e) {
      console.error("Error fetching past papers:", e);
    } finally {
      setLoading(false);
    }
  };

  const boardConfig = BOARD_CONFIG[activeBoard];

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="py-12 sm:py-16 border-b-2 border-black bg-neutral-50 dot-pattern">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 data-testid="past-papers-title" className="font-heading text-4xl sm:text-5xl font-bold mb-3">
            Past Papers Hub
          </h1>
          <p className="text-neutral-500 text-base sm:text-lg max-w-xl">
            Practice questions modelled on real exam papers from Edexcel, AQA, and OCR.
          </p>
        </div>
      </section>

      {/* Tabs */}
      <section className="py-8 sm:py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Tabs value={activeBoard} onValueChange={setActiveBoard} className="w-full">
            <TabsList
              data-testid="exam-board-tabs"
              className="bg-neutral-100 border-2 border-black p-1.5 rounded-xl gap-2 w-full sm:w-auto flex"
            >
              {Object.keys(BOARD_CONFIG).map((board) => (
                <TabsTrigger
                  key={board}
                  value={board}
                  data-testid={`tab-${board.toLowerCase()}`}
                  className="data-[state=active]:bg-white data-[state=active]:text-black data-[state=active]:border-2 data-[state=active]:border-black data-[state=active]:shadow-hard-sm rounded-lg px-4 sm:px-6 py-2.5 font-bold text-neutral-500 transition-all flex-1 sm:flex-none"
                >
                  {board}
                </TabsTrigger>
              ))}
            </TabsList>

            {Object.entries(BOARD_CONFIG).map(([board, config]) => (
              <TabsContent key={board} value={board} className="mt-8">
                {/* Board Info Card */}
                <div data-testid={`board-info-${board.toLowerCase()}`} className={`border-2 border-black rounded-xl p-6 mb-8 ${config.shadow} bg-white`}>
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-3 mb-2">
                        <span className={`${config.color} text-white px-3 py-1 rounded-md border-2 border-black font-heading font-bold text-xl`}>
                          {board}
                        </span>
                        <span className="font-mono text-sm text-neutral-400">{config.spec}</span>
                      </div>
                      <p className="text-neutral-600 text-sm">
                        3 papers per tier (Foundation & Higher) | 90 minutes each | Paper 1 is non-calculator
                      </p>
                    </div>
                    <a
                      href={config.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      data-testid={`board-link-${board.toLowerCase()}`}
                      className={`neo-btn ${config.color} text-white inline-flex items-center gap-2 text-sm`}
                    >
                      Official Site <ExternalLink size={14} />
                    </a>
                  </div>
                </div>

                {/* Papers List */}
                {loading ? (
                  <div data-testid="papers-loading" className="text-center py-12">
                    <div className="inline-block w-8 h-8 border-4 border-black border-t-transparent rounded-full animate-spin" />
                  </div>
                ) : (
                  <div className="space-y-4">
                    {(papers[board] || []).map((paper) => (
                      <div
                        key={paper.id}
                        data-testid={`paper-card-${paper.id}`}
                        className="border-2 border-black rounded-xl bg-white overflow-hidden"
                      >
                        <button
                          onClick={() => setExpandedPaper(expandedPaper === paper.id ? null : paper.id)}
                          className="w-full p-5 flex items-center justify-between hover:bg-neutral-50 transition-colors text-left"
                        >
                          <div className="flex items-center gap-4">
                            <div className={`w-10 h-10 ${config.color} text-white rounded-lg border-2 border-black flex items-center justify-center`}>
                              <FileText size={18} />
                            </div>
                            <div>
                              <p className="font-bold">{paper.description}</p>
                              <div className="flex flex-wrap items-center gap-2 mt-1">
                                <Badge variant="outline" className="border-2 text-xs font-mono">{paper.tier}</Badge>
                                <Badge variant="outline" className="border-2 text-xs font-mono flex items-center gap-1">
                                  {paper.calculator_allowed ? <Calculator size={12} /> : <Ban size={12} />}
                                  {paper.calculator_allowed ? "Calculator" : "Non-Calc"}
                                </Badge>
                                <span className="text-xs text-neutral-400">{paper.practice_questions.length} practice Q's</span>
                              </div>
                            </div>
                          </div>
                          {expandedPaper === paper.id ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                        </button>

                        {expandedPaper === paper.id && (
                          <div className="border-t-2 border-black p-5 bg-neutral-50">
                            <h4 className="font-heading font-bold mb-4">Practice Questions</h4>
                            <div className="space-y-4">
                              {paper.practice_questions.map((q, i) => (
                                <PracticeQuestion key={i} question={q} index={i} config={config} />
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </TabsContent>
            ))}
          </Tabs>
        </div>
      </section>
    </div>
  );
}

function PracticeQuestion({ question, index, config }) {
  const [showAnswer, setShowAnswer] = useState(false);

  return (
    <div className="border-2 border-black rounded-lg bg-white p-4">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className={`text-xs font-bold ${config.textColor} uppercase`}>Q{index + 1}</span>
            <Badge variant="secondary" className="text-xs">{question.topic}</Badge>
            <span className="text-xs text-neutral-400">[{question.marks} marks]</span>
          </div>
          <p className="font-medium">{question.question}</p>
        </div>
      </div>
      <button
        data-testid={`show-answer-${index}`}
        onClick={() => setShowAnswer(!showAnswer)}
        className="mt-3 text-sm font-bold flex items-center gap-1 hover:gap-2 transition-all"
      >
        {showAnswer ? "Hide Answer" : "Show Answer"} 
        {showAnswer ? <ChevronUp size={14} /> : <ArrowRight size={14} />}
      </button>
      {showAnswer && (
        <div className="mt-3 p-3 bg-green-50 border-2 border-green-600 rounded-lg">
          <pre className="font-mono text-sm whitespace-pre-wrap">{question.answer}</pre>
        </div>
      )}
    </div>
  );
}
