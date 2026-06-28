# AI Applicant Tracking System (ATS)

An AI-powered Applicant Tracking System built with **FastAPI**, **React**, and **Natural Language Processing (NLP)** to help recruiters analyze and rank candidates against a job description.

The system combines **TF-IDF keyword matching** with **Sentence Transformer semantic embeddings** to produce more meaningful candidate rankings than keyword matching alone.

---

## Features

### Recruiter Dashboard
- Create and manage multiple job postings
- Select an existing job for candidate evaluation
- Upload one or more PDF resumes
- View ranked candidates in an interactive dashboard

### AI Resume Analysis
- PDF text extraction
- Skill extraction
- TF-IDF similarity scoring
- Semantic similarity using Sentence Transformers
- Combined AI ranking score
- Match percentage
- Matched skills
- Missing skills
- AI recommendation (Strong / Moderate / Weak)

### Candidate Dashboard
- Candidate ranking cards
- Search candidates
- Filter by recommendation
- Sort by score
- Export rankings as CSV
- Top candidate highlight
- Average score statistics

---

# Tech Stack

## Frontend

- React
- Axios
- Tailwind CSS
- Vite

## Backend

- FastAPI
- Python
- Pydantic
- SQLAlchemy
- PostgreSQL
- Uvicorn

## AI / NLP

- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity
- Sentence Transformers
- all-MiniLM-L6-v2

## Deployment

- Frontend: Vercel
- Backend: Render
- Database: PostgreSQL (Render)

---

# System Architecture

```
                React Frontend
                       │
                     Axios
                       │
                FastAPI REST API
                       │
        ┌──────────────┴──────────────┐
        │                             │
  Resume Processing             Job Management
        │                             │
        │                       PostgreSQL
        │
 PDF Extraction
        │
 Skill Extraction
        │
TF-IDF + Semantic Embeddings
        │
 Candidate Ranking
        │
  JSON Response
```

---

# Project Structure

```
frontend/
    src/
        components/
        services/

app/
    ai/
    core/
    database/
    models/
    repositories/
    routers/
    schemas/
    services/
    utils/

requirements.txt
```

---

# API Endpoints

## Health

| Method | Endpoint |
|---------|----------|
| GET | `/health` |

---

## Jobs

| Method | Endpoint |
|---------|----------|
| POST | `/jobs` |
| GET | `/jobs` |
| GET | `/jobs/{id}` |

---

## Resume

| Method | Endpoint |
|---------|----------|
| POST | `/resume/analyze` |

---

## Ranking

| Method | Endpoint |
|---------|----------|
| POST | `/ranking/rank` |

---

# Running Locally

## Backend

```bash
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Runs on:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Runs on:

```
http://localhost:5173
```

---

# Deployment

Frontend is deployed on **Vercel**.

Backend is deployed on **Render**.

The backend uses a managed PostgreSQL database hosted on Render.

---

# AI Ranking Strategy

Each candidate is evaluated using two independent techniques.

### 1. TF-IDF Similarity

Measures keyword overlap between the job description and resume.

---

### 2. Semantic Similarity

Uses the Sentence Transformer model:

```
all-MiniLM-L6-v2
```

to compare the meaning of the resume against the job description.

---

The final candidate score is computed as a weighted combination of the two similarity scores before generating recruiter recommendations.

---

# Future Improvements

- Authentication & recruiter accounts
- Resume history
- Interview scheduling
- Email notifications
- OCR support for scanned resumes
- Docker deployment
- Kubernetes deployment
- Resume feedback generation using an LLM
- Advanced recruiter analytics

---

# Screenshots

## Recruiter Dashboard

*(Add screenshot here)*

---

## Candidate Rankings

*(Add screenshot here)*

---

## Swagger Documentation

*(Add screenshot here)*

---

# Author

**Alfia Mohammad Ashraf**

Built as a full-stack AI project to explore NLP, semantic search, FastAPI, PostgreSQL, React, and modern recruiter workflows.
