# EVIDIQ

### Evidence Intelligence for Hiring Decisions

**Tagline:**
**Don't trust rankings. Trust evidence.**

---

## Overview

EVIDIQ is an AI-powered hiring decision intelligence platform designed to help recruiters make transparent, evidence-backed candidate decisions.

Traditional Applicant Tracking Systems (ATS) prioritize keyword matching and static scoring. While efficient, these approaches often fail to explain decisions, overlook hidden talent, and encourage blind trust in AI-generated rankings.

EVIDIQ approaches hiring differently.

Instead of asking:

> “Who scored highest?”

EVIDIQ asks:

> “How confident are we that this recommendation is correct?”

The platform combines semantic understanding, confidence estimation, explainability, and recruiter feedback to transform candidate ranking into a trustworthy decision-making process.

---

# Problem

Modern hiring systems face a growing trust problem.

Recruiters receive ranked candidate lists but often cannot answer:

* Why was this candidate selected?
* What evidence supports this recommendation?
* How reliable is the AI decision?
* Which strong candidates may have been overlooked?
* Should recruiters trust or challenge this output?

At the same time:

* Resume optimization increasingly influences rankings
* AI-generated resumes reduce differentiation
* Candidate scores lack transparency
* Traditional ATS systems reward wording over capability

As a result, recruiters either trust AI too much or ignore it entirely.

---

# Our Solution

EVIDIQ introduces **Decision Intelligence for Hiring**.

Instead of automating decisions, EVIDIQ supports decisions.

The platform evaluates:

* Candidate evidence
* Semantic fit
* Confidence level
* Explainability
* Recruiter disagreement

Every recommendation becomes inspectable and challengeable.

---

# Core Innovation

## AI Disagreement Engine™

Most systems operate like:

```text
Resume
↓

ATS Score
↓

Decision
```

EVIDIQ operates like:

```text
Resume
↓

AI Evaluation
↓

Evidence Analysis
↓

Confidence Estimation
↓

Recruiter Challenge
↓

Final Decision
```

The recruiter remains in control.

---

# Key Features

## Evidence-Based Candidate Ranking

Evaluates candidates using contextual understanding instead of exact keyword overlap.

Signals include:

* Skills
* Experience
* Projects
* Technical relevance
* Career context

Output:

```text
Fit Score: 88
```

---

## Confidence Engine

Separates candidate capability from AI certainty.

Example:

```text
Fit Score: 91

Confidence: 58
```

Meaning:

Strong candidate.

Insufficient evidence.

---

## Explainable Recommendations

Every ranking includes reasoning.

Example:

```text
Selected Because

+ Strong project alignment

+ Relevant technical stack

− Missing deployment exposure
```

---

## Recruiter Challenge Layer

Recruiters can disagree with AI recommendations.

Example:

```text
Challenge:
Portfolio depth insufficient

↓

AI recalculates ranking
```

This creates human-in-the-loop hiring.

---

## Hidden Talent Discovery

Highlights candidates who may have been overlooked by traditional filtering systems.

Example:

```text
Original Rank: 29

Potential Rank: 7

Reason:
Strong transferable evidence
```

---

# Architecture

```text
Frontend (Next.js)

↓

FastAPI Backend

↓

Resume Parsing

↓

Embedding Generation

↓

Semantic Retrieval

↓

Candidate Scoring

↓

Confidence Engine

↓

Explanation Generator

↓

Decision Dashboard
```

---

# Technology Stack

## Frontend

* Next.js
* Tailwind CSS
* TypeScript
* ShadCN UI

## Backend

* FastAPI
* Python
* Uvicorn
* Pydantic

## AI / ML

* Sentence Transformers
* MiniLM Embeddings
* Scikit-learn
* Groq API

## Storage

* Qdrant
* PostgreSQL

## Parsing

* PyMuPDF
* Pandas

---

# Repository Structure

```bash
evidiq/

backend/
frontend/
data/
tests/
docs/
```

---

# Current Workflow

```text
Upload Resume

↓

Extract Candidate Evidence

↓

Generate Embeddings

↓

Semantic Evaluation

↓

Compute Confidence

↓

Generate Explanation

↓

Challenge Recommendation

↓

Export Results
```

---

# API Endpoints

## Upload Resume

```http
POST /upload
```

Uploads candidate resumes.

---

## Rank Candidates

```http
GET /rank
```

Returns semantic fit score.

Example:

```json
{
"score":0.82
}
```

---

# Why Use EVIDIQ?

Existing hiring platforms answer:

> Who should I hire?

EVIDIQ answers:

> Why should I trust this recommendation?

Business outcomes:

* Higher recruiter trust
* Better decision transparency
* Reduced resume gaming
* Faster candidate review
* Improved candidate discovery

---

# Vision

EVIDIQ does not replace recruiters.

It gives recruiters the confidence to question AI and make better hiring decisions.

The future of hiring is not automated decisions.

The future is trustworthy decisions.

---

# License

MIT License
