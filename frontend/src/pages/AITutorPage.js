import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import { toast } from "sonner";
import { Send, Bot, User, Loader2, Sparkles, Trash2 } from "lucide-react";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const SUGGESTED_QUESTIONS = [
  "Explain Pythagoras' theorem step by step",
  "How do I solve simultaneous equations?",
  "What's the difference between HCF and LCM?",
  "Help me understand probability tree diagrams",
  "How do I find the nth term of a sequence?",
  "Explain how to use SOHCAHTOA",
];

export default function AITutorPage() {
  const [searchParams] = useSearchParams();
  const initialTopic = searchParams.get("topic") || "";
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (initialTopic) {
      setInput(`Explain ${initialTopic} in simple terms with examples`);
    }
  }, [initialTopic]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (text) => {
    const question = text || input.trim();
    if (!question || loading) return;

    const newMessages = [...messages, { role: "user", content: question }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post(`${API}/ai-tutor`, {
        question,
        topic: initialTopic || undefined,
      });
      setMessages([...newMessages, { role: "assistant", content: res.data.response }]);
    } catch (e) {
      console.error("AI Tutor error:", e);
      toast.error("AI Tutor is having trouble. Please try again.");
      setMessages([
        ...newMessages,
        { role: "assistant", content: "Sorry, I'm having a bit of trouble right now. Please try asking your question again!" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    toast.info("Chat cleared");
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <section className="py-8 sm:py-10 border-b-2 border-black bg-neutral-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 data-testid="ai-tutor-title" className="font-heading text-3xl sm:text-4xl font-bold mb-2">
                AI Maths Tutor
              </h1>
              <p className="text-neutral-500 text-sm sm:text-base">
                Ask any GCSE Maths question and get step-by-step help.
              </p>
            </div>
            {messages.length > 0 && (
              <button
                data-testid="clear-chat-btn"
                onClick={clearChat}
                className="neo-btn bg-white text-black text-sm flex items-center gap-2"
              >
                <Trash2 size={14} /> Clear
              </button>
            )}
          </div>
        </div>
      </section>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto pb-48">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {messages.length === 0 ? (
            <div data-testid="ai-tutor-empty-state" className="text-center py-12">
              <div className="w-20 h-20 bg-black text-white rounded-2xl flex items-center justify-center mx-auto mb-6 border-2 border-black shadow-hard">
                <Sparkles size={32} />
              </div>
              <h2 className="font-heading text-2xl font-bold mb-2">What do you need help with?</h2>
              <p className="text-neutral-500 mb-8 max-w-md mx-auto">
                I'm your personal GCSE Maths tutor. Ask me anything and I'll explain it step by step!
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-2xl mx-auto">
                {SUGGESTED_QUESTIONS.map((q, i) => (
                  <button
                    key={i}
                    data-testid={`suggested-question-${i}`}
                    onClick={() => sendMessage(q)}
                    className="neo-card cursor-pointer text-left text-sm hover:shadow-[6px_6px_0px_0px_#000] p-4"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, i) => (
                <div
                  key={i}
                  data-testid={`chat-message-${i}`}
                  className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  {msg.role === "assistant" && (
                    <div className="w-9 h-9 bg-black text-white rounded-lg border-2 border-black flex items-center justify-center flex-shrink-0 shadow-hard-sm">
                      <Bot size={18} />
                    </div>
                  )}
                  <div
                    className={`max-w-[85%] sm:max-w-[75%] rounded-xl p-4 border-2 border-black ${
                      msg.role === "user"
                        ? "bg-black text-white"
                        : "bg-white shadow-hard-sm"
                    }`}
                  >
                    {msg.role === "assistant" ? (
                      <div className="markdown-content prose prose-sm max-w-none">
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                    ) : (
                      <p>{msg.content}</p>
                    )}
                  </div>
                  {msg.role === "user" && (
                    <div className="w-9 h-9 bg-blue-600 text-white rounded-lg border-2 border-black flex items-center justify-center flex-shrink-0 shadow-hard-sm">
                      <User size={18} />
                    </div>
                  )}
                </div>
              ))}
              {loading && (
                <div data-testid="ai-tutor-loading" className="flex gap-3">
                  <div className="w-9 h-9 bg-black text-white rounded-lg border-2 border-black flex items-center justify-center flex-shrink-0">
                    <Bot size={18} />
                  </div>
                  <div className="bg-white rounded-xl p-4 border-2 border-black shadow-hard-sm">
                    <Loader2 size={20} className="animate-spin text-neutral-400" />
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t-2 border-black">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex gap-3">
            <textarea
              data-testid="ai-tutor-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me anything about GCSE Maths..."
              rows={1}
              className="flex-1 px-4 py-3 border-2 border-black rounded-lg focus:outline-none focus:shadow-hard transition-shadow resize-none font-body"
            />
            <button
              data-testid="ai-tutor-send-btn"
              onClick={() => sendMessage()}
              disabled={!input.trim() || loading}
              className="neo-btn-primary px-4 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? <Loader2 size={20} className="animate-spin" /> : <Send size={20} />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
