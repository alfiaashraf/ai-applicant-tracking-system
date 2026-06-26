import logging
from pathlib import Path

from fastapi import APIRouter, File, Form, UploadFile

from app.core.exceptions import AppError, InvalidFileError
from app.schemas.ranking import RankingResponse
from app.services.ranking_service import rank_candidates_for_job
from app.utils.files import safe_remove, save_upload

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ranking", tags=["Ranking"])


@router.post(
    "/rank",
    response_model=RankingResponse,
    summary="Rank resumes for a job",
    response_description="Ranked candidates with scores, skill gaps, and recommendations.",
)
async def rank_resumes_endpoint(
    job_id: str = Form(
        ...,
        description="ID of an existing job posting created via POST /jobs.",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    ),
    files: list[UploadFile] = File(
        ...,
        description="One or more PDF resumes to rank against the job.",
    ),
) -> RankingResponse:
    if not files:
        raise InvalidFileError("At least one resume file is required.")

    stored_files: list[tuple[Path, str]] = []
    seen_names: dict[str, int] = {}

    try:
        for upload in files:
            stored_path, original_name = await save_upload(upload)
            count = seen_names.get(original_name, 0)
            seen_names[original_name] = count + 1
            display_name = (
                original_name
                if count == 0
                else f"{original_name} ({count + 1})"
            )
            stored_files.append((stored_path, display_name))

        return await rank_candidates_for_job(job_id, stored_files)
    except AppError:
        raise
    except Exception as exc:
        logger.exception("Unexpected error ranking resumes")
        raise AppError(f"Failed to rank resumes: {exc}") from exc
    finally:
        for stored_path, _ in stored_files:
            safe_remove(stored_path)
