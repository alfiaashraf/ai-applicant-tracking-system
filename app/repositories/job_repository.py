import uuid
from datetime import datetime, timezone
from threading import Lock

from app.models.job import Job

_repository: "InMemoryJobRepository | None" = None


class InMemoryJobRepository:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock = Lock()

    def create(self, title: str, description: str) -> Job:
        job = Job(
            id=str(uuid.uuid4()),
            title=title.strip(),
            description=description.strip(),
            created_at=datetime.now(timezone.utc),
        )

        with self._lock:
            self._jobs[job.id] = job

        return job

    def get_all(self) -> list[Job]:
        with self._lock:
            jobs = list(self._jobs.values())

        return sorted(jobs, key=lambda job: job.created_at, reverse=True)

    def get_by_id(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)


def get_job_repository() -> InMemoryJobRepository:
    global _repository

    if _repository is None:
        _repository = InMemoryJobRepository()

    return _repository
