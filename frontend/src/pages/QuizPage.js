import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { toast } from "sonner";
import { Brain, CheckCircle, XCircle, ArrowRight, RotateCcw, Trophy, ChevronRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function QuizPage() {
  const { topicId } = useParams();
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [result, setResult] = useState(null);
  const [score, setScore] = useState(0);
  const [answered, setAnswered] = useState(0);
  const [quizComplete, setQuizComplete] = useState(false);
  const [topics, setTopics] = useState([]);
  const [showTopicSelect, setShowTopicSelect] = useState(!topicId);

  useEffect(() => {
    if (topicId) {
      fetchQuiz(topicId);
    } else {
      fetchAllTopics();
    }
  }, [topicId]);

  const fetchAllTopics = async () => {
    try {
      const res = await axios.get(`${API}/topics`);
      setTopics(res.data.topics);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const fetchQuiz = async (id) => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/quizzes/${id}`);
      if (res.data.questions.length === 0) {
        // Try all quizzes
        const allRes = await axios.get(`${API}/quizzes`);
        setQuestions(allRes.data.questions.slice(0, 10));
      } else {
        setQuestions(res.data.questions);
      }
      resetQuiz();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
      setShowTopicSelect(false);
    }
  };

  const startAllQuiz = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/quizzes`);
      setQuestions(res.data.questions);
      resetQuiz();
      setShowTopicSelect(false);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const resetQuiz = () => {
    setCurrentIndex(0);
    setSelectedAnswer(null);
    setResult(null);
    setScore(0);
    setAnswered(0);
    setQuizComplete(false);
  };

  const handleAnswer = async (answerIndex) => {
    if (result !== null) return;
    setSelectedAnswer(answerIndex);

    try {
      const res = await axios.post(`${API}/quiz/check`, {
        question_id: questions[currentIndex].id,
        selected_answer: answerIndex,
      });
      setResult(res.data);
      setAnswered((a) => a + 1);
      if (res.data.correct) {
        setScore((s) => s + 1);
        toast.success("Correct! Well done!");
      } else {
        toast.error("Not quite - check the explanation!");
      }
    } catch (e) {
      console.error(e);
      toast.error("Error checking answer");
    }
  };

  const nextQuestion = () => {
    if (currentIndex + 1 >= questions.length) {
      setQuizComplete(true);
    } else {
      setCurrentIndex((i) => i + 1);
      setSelectedAnswer(null);
      setResult(null);
    }
  };

  if (loading) {
    return (
      <div data-testid="quiz-loading" className="flex items-center justify-center min-h-[60vh]">
        <div className="w-8 h-8 border-4 border-black border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  // Topic selection screen
  if (showTopicSelect) {
    return (
      <div className="min-h-screen">
        <section className="py-12 sm:py-16 border-b-2 border-black bg-neutral-50 dot-pattern">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 data-testid="quiz-page-title" className="font-heading text-4xl sm:text-5xl font-bold mb-3">
              Practice Quizzes
            </h1>
            <p className="text-neutral-500 text-base sm:text-lg">
              Choose a topic or take a mixed quiz to test your knowledge.
            </p>
          </div>
        </section>

        <section className="py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* All Topics Quiz */}
            <button
              data-testid="quiz-all-topics-btn"
              onClick={startAllQuiz}
              className="w-full neo-card cursor-pointer group mb-8 border-violet-600 text-left"
            >
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-violet-600 text-white rounded-lg border-2 border-black flex items-center justify-center">
                  <Brain size={24} />
                </div>
                <div className="flex-1">
                  <h3 className="font-heading text-xl font-bold">Mixed Quiz - All Topics</h3>
                  <p className="text-sm text-neutral-500">Test yourself on everything</p>
                </div>
                <ChevronRight size={24} className="text-neutral-400 group-hover:text-black" />
              </div>
            </button>

            {/* By Topic */}
            <h2 className="font-heading text-2xl font-bold mb-6">Or choose a topic:</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {topics.map((topic) => (
                <Link
                  key={topic.id}
                  to={`/quiz/${topic.id}`}
                  data-testid={`quiz-topic-${topic.id}`}
                  className="neo-card cursor-pointer group text-left"
                >
                  <h3 className="font-heading font-bold mb-1">{topic.title}</h3>
                  <div className="flex items-center justify-between">
                    <Badge variant="secondary" className="text-xs">{topic.category}</Badge>
                    <ChevronRight size={18} className="text-neutral-400 group-hover:text-black" />
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      </div>
    );
  }

  // Quiz Complete screen
  if (quizComplete) {
    const percentage = Math.round((score / questions.length) * 100);
    let message = "";
    let emoji = "";
    if (percentage === 100) { message = "Perfect score! You're a maths genius!"; emoji = "star"; }
    else if (percentage >= 80) { message = "Brilliant work! Nearly there!"; emoji = "trophy"; }
    else if (percentage >= 60) { message = "Good effort! Keep practising!"; emoji = "thumbsup"; }
    else if (percentage >= 40) { message = "Not bad! Review the topics and try again."; emoji = "muscle"; }
    else { message = "Keep going! Every practice session makes you better."; emoji = "rocket"; }

    return (
      <div className="min-h-screen flex items-center justify-center py-12">
        <div data-testid="quiz-results" className="neo-card-static max-w-md w-full mx-4 text-center">
          <div className="w-20 h-20 bg-black text-white rounded-full flex items-center justify-center mx-auto mb-6 border-2 border-black">
            <Trophy size={36} />
          </div>
          <h2 className="font-heading text-3xl font-bold mb-2">Quiz Complete!</h2>
          <p className="text-neutral-500 mb-6">{message}</p>
          
          <div className="neo-card-static mb-6">
            <div className="font-heading text-5xl font-bold mb-2">{score}/{questions.length}</div>
            <p className="text-neutral-500 text-sm">{percentage}% correct</p>
            <Progress value={percentage} className="mt-3 h-3 border-2 border-black rounded-full" />
          </div>

          <div className="flex flex-col gap-3">
            <button
              data-testid="quiz-retry-btn"
              onClick={resetQuiz}
              className="neo-btn-primary inline-flex items-center justify-center gap-2"
            >
              <RotateCcw size={16} /> Try Again
            </button>
            <Link
              to="/quiz"
              data-testid="quiz-back-btn"
              className="neo-btn bg-white text-black text-center"
            >
              Choose Another Quiz
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Active quiz
  const currentQ = questions[currentIndex];
  const progress = ((currentIndex) / questions.length) * 100;

  return (
    <div className="min-h-screen py-8 sm:py-12">
      <div className="max-w-2xl mx-auto px-4 sm:px-6">
        {/* Progress */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-bold">
              Question {currentIndex + 1} of {questions.length}
            </span>
            <span className="text-sm font-bold text-green-600">
              Score: {score}/{answered}
            </span>
          </div>
          <Progress data-testid="quiz-progress" value={progress} className="h-3 border-2 border-black rounded-full" />
        </div>

        {/* Question Card */}
        <div data-testid="quiz-question-card" className="neo-card-static mb-6">
          <Badge variant="secondary" className="text-xs mb-3">{currentQ.topic_title}</Badge>
          <h2 className="font-heading text-xl sm:text-2xl font-bold">{currentQ.question}</h2>
        </div>

        {/* Options */}
        <div className="space-y-3 mb-6">
          {currentQ.options.map((option, i) => {
            let optionClass = "quiz-option";
            if (result !== null) {
              if (i === result.correct_answer) optionClass += " correct";
              else if (i === selectedAnswer && !result.correct) optionClass += " incorrect";
            } else if (i === selectedAnswer) {
              optionClass += " selected";
            }

            return (
              <button
                key={i}
                data-testid={`quiz-option-${i}`}
                onClick={() => handleAnswer(i)}
                disabled={result !== null}
                className={`${optionClass} w-full text-left flex items-center gap-3`}
              >
                <span className="w-8 h-8 rounded-lg border-2 border-black flex items-center justify-center font-bold text-sm bg-neutral-50 flex-shrink-0">
                  {String.fromCharCode(65 + i)}
                </span>
                <span className="font-medium">{option}</span>
                {result !== null && i === result.correct_answer && (
                  <CheckCircle size={20} className="ml-auto text-green-600" />
                )}
                {result !== null && i === selectedAnswer && !result.correct && i !== result.correct_answer && (
                  <XCircle size={20} className="ml-auto text-red-600" />
                )}
              </button>
            );
          })}
        </div>

        {/* Explanation */}
        {result && (
          <div
            data-testid="quiz-explanation"
            className={`p-4 rounded-xl border-2 mb-6 ${
              result.correct
                ? "bg-green-50 border-green-600"
                : "bg-red-50 border-red-600"
            }`}
          >
            <p className={`font-bold text-sm mb-1 ${result.correct ? "text-green-700" : "text-red-700"}`}>
              {result.correct ? "Correct!" : "Not quite right"}
            </p>
            <p className="text-sm">{result.explanation}</p>
          </div>
        )}

        {/* Next Button */}
        {result !== null && (
          <button
            data-testid="quiz-next-btn"
            onClick={nextQuestion}
            className="neo-btn-primary w-full inline-flex items-center justify-center gap-2"
          >
            {currentIndex + 1 >= questions.length ? "See Results" : "Next Question"}
            <ArrowRight size={18} />
          </button>
        )}
      </div>
    </div>
  );
}
