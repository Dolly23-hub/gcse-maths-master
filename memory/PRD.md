# GCSE Maths Master - PRD

## Problem Statement
Build a comprehensive GCSE Maths revision app for UK students covering all exam boards (Edexcel, AQA, OCR) with topic explanations, past papers, quizzes, formulas, and AI-powered tutoring.

## Architecture
- **Frontend**: React + Tailwind CSS + Shadcn UI (Neo-Brutalist design)
- **Backend**: FastAPI + MongoDB
- **AI Integration**: OpenAI GPT-5.2 via Emergent LLM Key
- **Design**: Neo-Brutalist Notebook theme with bold borders, hard shadows

## User Personas
1. **GCSE Students (14-16)**: Primary users needing clear explanations and practice
2. **Teachers**: Looking for structured resources to share
3. **Parents**: Helping children with revision

## What's Been Implemented (Feb 2026)
- Homepage with hero, stats, features, category cards, exam board cards
- Topics page: 19 topics across 5 categories with search/filter
- Topic detail pages with markdown explanations, key points, worked examples
- Past Papers Hub: Tabbed interface (Edexcel/AQA/OCR) with expandable practice questions
- Interactive Quiz system with scoring, explanations, mixed/topic-specific modes
- Formula Sheet: 20+ formulas grouped by category with examples
- AI Tutor: Real-time GPT-5.2 powered chat with suggested questions
- Responsive mobile navigation
- Seeded database with rich content

## Prioritized Backlog
### P0 (Critical)
- All core features implemented and tested

### P1 (High Priority)
- More quiz questions per topic
- More past paper years and questions
- Progress tracking with local storage
- Exam countdown timer

### P2 (Nice to Have)
- Topic bookmarking
- Study planner/calendar
- Flashcard mode for formulas
- Dark mode toggle
- Share results on social media

## Next Tasks
1. Add more content (quiz questions, past paper questions)
2. Implement local storage progress tracking
3. Add exam countdown feature
4. Expand Higher tier content
