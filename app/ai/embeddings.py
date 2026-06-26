from sklearn.metrics.pairwise import cosine_similarity

_model = None
_model_name: str | None = None


def _get_model(model_name: str):
    global _model, _model_name

    if _model is None or _model_name != model_name:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(model_name)
        _model_name = model_name

    return _model


def semantic_rank(job_description, resumes, model_name: str = "all-MiniLM-L6-v2"):
    model = _get_model(model_name)

    resume_names = list(resumes.keys())
    resume_texts = list(resumes.values())

    job_embedding = model.encode([job_description])
    resume_embeddings = model.encode(resume_texts)

    scores = cosine_similarity(job_embedding, resume_embeddings)[0]

    rankings = []

    for name, score in zip(resume_names, scores):
        rankings.append((name, float(score)))

    rankings.sort(key=lambda x: x[1], reverse=True)

    return rankings
