# GCSE Maths Master - PRD (Final Version)

## Problem Statement
Build a comprehensive GCSE Maths revision app for UK students covering all exam boards (Edexcel, AQA, OCR) with topic explanations, past papers, quizzes, formulas, and AI-powered tutoring.

## Architecture
- **Frontend**: React + Tailwind CSS + Shadcn UI (Neo-Brutalist Notebook design)
- **Backend**: FastAPI + MongoDB
- **AI Integration**: OpenAI GPT-5.2 via Emergent LLM Key
- **Design**: Colourful Neo-Brutalist theme with bold borders, hard shadows, section-specific accent colours

## User Personas
1. **GCSE Students (14-16)**: Primary users needing clear explanations and practice
2. **Teachers**: Looking for structured resources to share
3. **Parents**: Helping children with revision

## What's Been Implemented (Feb 2026)
### Content
- **33 topics** across 5 categories (Number, Algebra, Ratio & Proportion, Geometry & Measures, Probability & Statistics)
- **84 quiz questions** with instant feedback and explanations
- **21 past papers** across Edexcel (8), AQA (7), OCR (6) with practice questions
- **30 key formulas** with descriptions and usage examples
- Topics include Higher tier content: Surds, Circle Theorems, Vectors, Functions, Algebraic Proof

### Features
- **Topic Detail Pages**: Markdown-rendered explanations, key points, expandable worked examples
- **Past Papers Hub**: Tabbed interface (Edexcel/AQA/OCR), expandable papers with practice questions
- **Interactive Quiz System**: Topic-specific or mixed mode, scoring, explanations, results screen
- **Formula Sheet**: Searchable, expandable formulas grouped by category
- **AI Maths Tutor**: GPT-5.2 powered chat with suggested questions and topic context
- **Exam Countdown**: 2026 GCSE exam dates with days remaining
- **Progress Tracking**: LocalStorage-based topic viewing and quiz score tracking
- **Study Tips**: Revision advice section on homepage
- **Mobile Responsive**: Full mobile navigation with hamburger menu

### Design
- Colourful section backgrounds (blue hero, dark countdown, violet stats, amber features, green categories, pink exam boards, sky study tips, blue CTA)
- Neo-Brutalist cards with bold borders and hard shadows
- Fonts: Space Grotesk (headings), Outfit (body), JetBrains Mono (formulas/code)
- Exam board accent colours: Edexcel (blue), AQA (pink), OCR (orange)

## API Endpoints
- GET /api/stats - Dynamic content counts
- GET /api/topics - All topics
- GET /api/topics/{id} - Topic detail
- GET /api/topics/category/{category} - Topics by category
- GET /api/past-papers/{board} - Papers by exam board
- GET /api/quizzes - All quiz questions
- GET /api/quizzes/{topic_id} - Topic-specific quizzes
- POST /api/quiz/check - Validate quiz answer
- GET /api/formulas - All formulas
- GET /api/formulas/category/{category} - Formulas by category
- POST /api/ai-tutor - AI-powered explanations
- POST /api/seed - Seed database

## Deployment Ready
- All lint checks passing (Python + JavaScript)
- All API endpoints verified
- All pages tested (desktop + mobile)
- Database seeded with comprehensive content
