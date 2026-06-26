from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_resumes(job_description, resumes):

    documents = [job_description] + list(resumes.values())

    vectorizer = TfidfVectorizer()

    matrix = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(
        matrix[0:1],
        matrix[1:]
    )[0]

    results = []

    for filename, score in zip(resumes.keys(), similarities):
        results.append((filename, score))

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results