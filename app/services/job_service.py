import logging

from app.core.exceptions import JobNotFoundError
from app.models.job import Job
from app.repositories.job_repository import InMemoryJobRepository, get_job_repository
from app.schemas.job import JobCreate, JobResponse

logger = logging.getLogger(__name__)


def _to_response(job: Job) -> JobResponse:
    return JobResponse(
        id=job.id,
        title=job.title,
        description=job.description,
        created_at=job.created_at,
    )


def create_job(
    data: JobCreate,
    repository: InMemoryJobRepository | None = None,
) -> JobResponse:
    repository = repository or get_job_repository()
    job = repository.create(title=data.title, description=data.description)
    logger.info("Created job '%s' (%s)", job.title, job.id)
    return _to_response(job)


def list_jobs(
    repository: InMemoryJobRepository | None = None,
) -> list[JobResponse]:
    repository = repository or get_job_repository()
    return [_to_response(job) for job in repository.get_all()]


def get_job(
    job_id: str,
    repository: InMemoryJobRepository | None = None,
) -> JobResponse:
    repository = repository or get_job_repository()
    job = repository.get_by_id(job_id)

    if job is None:
        raise JobNotFoundError(f"Job '{job_id}' not found.")

    return _to_response(job)


def get_job_description(
    job_id: str,
    repository: InMemoryJobRepository | None = None,
) -> str:
    job = get_job(job_id, repository)
    return f"{job.title}\n\n{job.description}"
