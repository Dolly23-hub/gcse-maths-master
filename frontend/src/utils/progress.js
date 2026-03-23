// Local storage progress tracking utility
const STORAGE_KEY = "gcse_maths_progress";

function getProgress() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : { topicsViewed: [], quizResults: {}, lastVisit: null };
  } catch {
    return { topicsViewed: [], quizResults: {}, lastVisit: null };
  }
}

function saveProgress(progress) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  } catch {
    // localStorage might be full or disabled
  }
}

export function markTopicViewed(topicId) {
  const progress = getProgress();
  if (!progress.topicsViewed.includes(topicId)) {
    progress.topicsViewed.push(topicId);
  }
  progress.lastVisit = new Date().toISOString();
  saveProgress(progress);
}

export function saveQuizResult(topicId, score, total) {
  const progress = getProgress();
  const prev = progress.quizResults[topicId];
  // Keep the best score
  if (!prev || score > prev.score) {
    progress.quizResults[topicId] = { score, total, date: new Date().toISOString() };
  }
  progress.lastVisit = new Date().toISOString();
  saveProgress(progress);
}

export function getTopicsViewed() {
  return getProgress().topicsViewed;
}

export function getQuizResults() {
  return getProgress().quizResults;
}

export function getOverallProgress(totalTopics) {
  const progress = getProgress();
  const viewed = progress.topicsViewed.length;
  return totalTopics > 0 ? Math.round((viewed / totalTopics) * 100) : 0;
}

export function getQuizScore(topicId) {
  const progress = getProgress();
  return progress.quizResults[topicId] || null;
}

export function getStudyStreak() {
  const progress = getProgress();
  // Simple: just check if visited today
  if (!progress.lastVisit) return 0;
  const lastVisit = new Date(progress.lastVisit);
  const today = new Date();
  const diffDays = Math.floor((today - lastVisit) / (1000 * 60 * 60 * 24));
  return diffDays <= 1 ? 1 : 0;
}

export function getTotalQuizScore() {
  const results = getQuizResults();
  let totalCorrect = 0;
  let totalQuestions = 0;
  Object.values(results).forEach(r => {
    totalCorrect += r.score;
    totalQuestions += r.total;
  });
  return { correct: totalCorrect, total: totalQuestions };
}
