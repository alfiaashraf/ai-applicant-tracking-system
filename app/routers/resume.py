import logging
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.core.exceptions import AppError
from app.schemas.resume import ResumeAnalyzeResponse
from app.services.resume_service import analyze_resume
from app.utils.files import safe_remove, save_upload

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post(
    "/analyze",
    response_model=ResumeAnalyzeResponse,
    summary="Analyze a resume",
    response_description="Extracted text and detected skills from the uploaded PDF.",
)
async def analyze_resume_endpoint(
    file: UploadFile = File(..., description="PDF resume to analyze"),
) -> ResumeAnalyzeResponse:
    stored_path: Path | None = None

    try:
        stored_path, original_name = await save_upload(file)
        return await analyze_resume(stored_path, original_name)
    except AppError:
        raise
    except Exception as exc:
        logger.exception("Unexpected error analyzing resume")
        raise AppError(f"Failed to analyze resume: {exc}") from exc
    finally:
        if stored_path is not None:
            safe_remove(stored_path)
