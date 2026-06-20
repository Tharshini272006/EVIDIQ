# EVIDIQ — Copilot Instructions

## What this project is
EVIDIQ is a hiring decision-intelligence backend + frontend. It separates
"how good is this candidate" (Fit Score) from "how sure are we" (Confidence),
explains every score with concrete evidence, and lets a recruiter challenge a
ranking and see it recompute. It is NOT a generic ATS keyword matcher.

## Hard rules
- Never invent a metric that has no underlying signal. If a score can't be
  traced to an actual computed value (cosine similarity, word count, regex
  match, explicit rule), do not output it. No fake "bias score," no
  unvalidated "future fit" predictions, no decorative numbers.
- Every score must be explainable: if you add a number, also add the code
  path that shows which inputs produced it.
- Match existing patterns: backend uses FastAPI routers under `backend/api/`,
  business logic under `backend/services/<domain>/`, plain functions over
  classes unless state is genuinely needed.
- Imports are absolute from repo root: `from backend.services.x.y import z`.
  Run with `uvicorn backend.main:app --reload` from repo root, never from
  inside `backend/`.
- Frontend is Next.js (App Router) + TypeScript, no Tailwind/ShadCN currently
  installed — use plain CSS modules / globals.css patterns already in
  `frontend/app/globals.css` unless told otherwise.
- No placeholder/stub functions that silently return empty or null in a way
  that looks like a finished feature (e.g. a component that returns `null`
  but is wired up like it works). If something is a stub, name it clearly
  and leave a TODO comment.
- Always handle: empty resume folder, unparseable PDF/DOCX, missing job
  description file, zero candidates, malformed upload. Fail with clear
  HTTPException messages, not silent empty returns, unless empty-is-valid
  is the actual correct behavior (document why if so).
- Never commit secrets, personal files, or real resume/PII data into
  `data/resumes/` — that folder is sample-data-only and gitignored except
  for `sample_resume.pdf`.

## Current real architecture (don't contradict this)
backend/
  api/          -> route handlers only, no business logic
  services/
    parser/         -> resume_parser.py (PDF via PyMuPDF/fitz, DOCX via raw zip/XML)
    embeddings/      -> generate_embeddings.py (sentence-transformers, all-MiniLM-L6-v2)
    ranking/         -> rank_engine.py (orchestrates parse -> embed -> score -> sort)
    scoring/         -> candidate_score.py (cosine similarity via sklearn)
    confidence/      -> confidence_engine.py (in progress)
    reasoning/       -> explanation_engine.py (in progress)

## When generating code
- Add type hints on every function signature.
- Add a docstring explaining the actual logic, not a restatement of the
  function name.
- Prefer small, testable pure functions over large multi-responsibility ones.
- If you're not sure whether a feature already exists elsewhere in the repo,
  say so instead of duplicating logic.
