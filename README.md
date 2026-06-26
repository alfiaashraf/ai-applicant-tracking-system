# AI Applicant Tracking System

An AI-powered Applicant Tracking System (ATS) that helps recruiters analyze and rank candidates against job descriptions using Natural Language Processing (NLP) and semantic similarity.

## Features

- Upload PDF resumes
- Analyze resume skills
- AI-powered candidate ranking
- Semantic similarity using Sentence Transformers
- TF-IDF based ranking
- FastAPI REST API
- Swagger API documentation
- Health monitoring endpoint

## Tech Stack

### Backend
- FastAPI
- Python
- Pydantic
- Scikit-learn
- Sentence Transformers

### AI / NLP
- TF-IDF
- Cosine Similarity
- Semantic Embeddings
- PDF Parsing

## Project Structure

```text
app/
    ai/
    routers/
    services/
    schemas/
    models/
    database/
```

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /health | Health check |
| POST | /resume/analyze | Analyze a resume |
| POST | /ranking/rank | Rank resumes |

## Current Status

🚧 Under active development

Upcoming features:

- React recruiter dashboard
- PostgreSQL integration
- Authentication
- Resume analytics
- CSV export
- Docker deployment
