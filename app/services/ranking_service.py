import asyncio
import logging
from pathlib import Path

from app.ai.embeddings import semantic_rank
from app.ai.ranker import rank_resumes
from app.ai.skill_extractor import extract_skills
from app.core.config import Settings, get_settings
from app.core.exceptions import EmptyDocumentError, PDFParseError
from app.schemas.ranking import RankingItem, RankingResponse
from app.services.job_service import get_job_description
from app.services.resume_service import extract_resume_text
from app.utils.constants import (
    RECOMMENDATION_MODERATE,
    RECOMMENDATION_STRONG,
    RECOMMENDATION_WEAK,
)

logger = logging.getLogger(__name__)


def _normalize_scores(scores: dict[str, float]) -> dict[str, float]:
    if not scores:
        return {}

    values = list(scores.values())
    min_score = min(values)
    max_score = max(values)

    if max_score == min_score:
        return {name: 1.0 if max_score > 0 else 0.0 for name in scores}

    return {
        name: (score - min_score) / (max_score - min_score)
        for name, score in scores.items()
    }


def _recommendation(score: float, settings: Settings) -> str:
    if score >= settings.strong_score_threshold:
        return RECOMMENDATION_STRONG
    if score >= settings.moderate_score_threshold:
        return RECOMMENDATION_MODERATE
    return RECOMMENDATION_WEAK


def _rank_candidates_sync(
    job_description: str,
    resumes: dict[str, str],
    settings: Settings,
) -> RankingResponse:
    if not job_description.strip():
        raise EmptyDocumentError("Job description cannot be empty.")

    if not resumes:
        raise EmptyDocumentError("At least one resume is required.")

    logger.info("Ranking %d resumes against job description", len(resumes))

    tfidf_results = rank_resumes(job_description, resumes)
    tfidf_scores = _normalize_scores(
        {name: float(score) for name, score in tfidf_results}
    )
    semantic_results = semantic_rank(
        job_description,
        resumes,
        model_name=settings.embedding_model,
    )

    semantic_scores = _normalize_scores(
        {name: float(score) for name, score in semantic_results}
    )

    job_skills = set(extract_skills(job_description))
    rankings: list[RankingItem] = []

    for filename, resume_text in resumes.items():
        tfidf_score = tfidf_scores.get(filename, 0.0)
        semantic_score = semantic_scores.get(filename, 0.0)
        combined_score = (
            settings.tfidf_weight * tfidf_score
            + settings.semantic_weight * semantic_score
        )

        resume_skills = set(extract_skills(resume_text))
        matched_skills = sorted(job_skills & resume_skills)
        missing_skills = sorted(job_skills - resume_skills)

        rankings.append(
            RankingItem(
                filename=filename,
                score=round(combined_score, 4),
                matched_skills=matched_skills,
                missing_skills=missing_skills,
                recommendation=_recommendation(combined_score, settings),
            )
        )

    rankings.sort(key=lambda item: item.score, reverse=True)
    return RankingResponse(rankings=rankings)


async def rank_candidates_for_job(
    job_id: str,
    resume_files: list[tuple[Path, str]],
    settings: Settings | None = None,
) -> RankingResponse:
    job_description = get_job_description(job_id)
    return await rank_candidates(job_description, resume_files, settings)


async def rank_candidates(
    job_description: str,
    resume_files: list[tuple[Path, str]],
    settings: Settings | None = None,
) -> RankingResponse:
    settings = settings or get_settings()
    resumes: dict[str, str] = {}

    for pdf_path, filename in resume_files:
        try:
            resumes[filename] = extract_resume_text(pdf_path)
        except (PDFParseError, EmptyDocumentError):
            raise
        except Exception as exc:
            raise PDFParseError(
                f"Failed to process resume '{filename}': {exc}"
            ) from exc

    return await asyncio.to_thread(
        _rank_candidates_sync,
        job_description,
        resumes,
        settings,
    )
