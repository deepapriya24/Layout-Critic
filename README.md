# 

![Backend Tests](https://github.com/YOUR_USERNAME/layout-critic/actions/workflows/tests.yml/badge.svg)

An AI-powered tool that analyzes UI screenshots and returns a scored design critique — contrast, spacing, visual hierarchy, alignment, and color harmony — with flagged problem regions and one-line fix suggestions.

## Why I built this

As a UI/UX designer, I wanted a tool that gives instant, structured feedback on a design the way a senior reviewer would — not just "looks good/bad" but scored, specific, and actionable. This project combines that design background with full-stack engineering: a FastAPI backend, a React frontend, and a scoring pipeline built to plug into any LLM provider.

## Tech stack

- **Frontend:** React (Vite) + Tailwind CSS, animated dark/futuristic UI
- **Backend:** FastAPI (Python), Pydantic for schema validation
- **Testing:** Pytest, mocked scoring calls
- **CI:** GitHub Actions running the test suite on every push

## How scoring works

The backend currently ships with a **mock scoring adapter** (`backend/app/scorer.py`) that returns realistic sample data — no API key required to run the full app end-to-end. The adapter is written so a real LLM provider (OpenAI, Gemini, Anthropic, etc.) can be dropped in by replacing a single function; see the comments at the top of `scorer.py` for exactly where.

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs at `http://localhost:8000` — Swagger docs at `http://localhost:8000/docs`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

### Running tests
```bash
cd backend
pytest -v
```

## Screenshots

_Add screenshots here after running the app locally._

## Project structure

```
layout-critic/
├── frontend/    # React + Tailwind UI
├── backend/     # FastAPI app + tests
└── .github/     # CI workflow
```
