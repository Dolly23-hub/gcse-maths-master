import { useState } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "@/components/Navbar";
import HomePage from "@/pages/HomePage";
import TopicsPage from "@/pages/TopicsPage";
import TopicDetailPage from "@/pages/TopicDetailPage";
import PastPapersPage from "@/pages/PastPapersPage";
import QuizPage from "@/pages/QuizPage";
import FormulaSheetPage from "@/pages/FormulaSheetPage";
import AITutorPage from "@/pages/AITutorPage";
import RevisionPlannerPage from "@/pages/RevisionPlannerPage";
import { Toaster } from "sonner";

function App() {
  return (
    <div className="App min-h-screen bg-white">
      <BrowserRouter>
        <Navbar />
        <main className="pt-20">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/topics" element={<TopicsPage />} />
            <Route path="/topics/:topicId" element={<TopicDetailPage />} />
            <Route path="/past-papers" element={<PastPapersPage />} />
            <Route path="/quiz" element={<QuizPage />} />
            <Route path="/quiz/:topicId" element={<QuizPage />} />
            <Route path="/formulas" element={<FormulaSheetPage />} />
            <Route path="/ai-tutor" element={<AITutorPage />} />
            <Route path="/revision-planner" element={<RevisionPlannerPage />} />
          </Routes>
        </main>
        <Toaster position="bottom-right" richColors />
      </BrowserRouter>
    </div>
  );
}

export default App;
