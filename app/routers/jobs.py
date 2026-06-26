import logging

from fastapi import APIRouter, Path

from app.core.exceptions import AppError
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import create_job, get_job, list_jobs

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/jobs",
    tags=["Recruiter Dashboard"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=201,
    summary="Create a job posting",
    response_description="The newly created job posting.",
)
async def create_job_endpoint(data: JobCreate) -> JobResponse:
    try:
        return create_job(data)
    except AppError:
        raise
    except Exception as exc:
        logger.exception("Unexpected error creating job")
        raise AppError(f"Failed to create job: {exc}") from exc


@router.get(
    "",
    response_model=list[JobResponse],
    summary="List job postings",
    response_description="All job postings, newest first.",
)
async def list_jobs_endpoint() -> list[JobResponse]:
    return list_jobs()


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    summary="Get a job posting",
    response_description="Job posting details for the recruiter dashboard.",
)
async def get_job_endpoint(
    job_id: str = Path(..., description="Unique job identifier."),
) -> JobResponse:
    return get_job(job_id)
