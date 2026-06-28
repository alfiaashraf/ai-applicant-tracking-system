import uuid
import logging

from app.database import SessionLocal
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse
from app.core.exceptions import JobNotFoundError

logger = logging.getLogger(__name__)


def _to_response(job: Job) -> JobResponse:
    return JobResponse(
        id=job.id,
        title=job.title,
        description=job.description,
        created_at=job.created_at,
    )


def create_job(data: JobCreate) -> JobResponse:
    db = SessionLocal()

    try:
        job = Job(
            id=str(uuid.uuid4()),
            title=data.title.strip(),
            description=data.description.strip(),
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        logger.info("Created job '%s' (%s)", job.title, job.id)

        return _to_response(job)

    finally:
        db.close()


def list_jobs() -> list[JobResponse]:
    db = SessionLocal()

    try:
        jobs = db.query(Job).order_by(Job.created_at.desc()).all()
        return [_to_response(job) for job in jobs]

    finally:
        db.close()


def get_job(job_id: str) -> JobResponse:
    db = SessionLocal()

    try:
        job = db.query(Job).filter(Job.id == job_id).first()

        if job is None:
            raise JobNotFoundError(f"Job '{job_id}' not found.")

        return _to_response(job)

    finally:
        db.close()


def get_job_description(job_id: str) -> str:
    job = get_job(job_id)
    return f"{job.title}\n\n{job.description}"
