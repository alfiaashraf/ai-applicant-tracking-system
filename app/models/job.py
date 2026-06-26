from dataclasses import dataclass
from datetime import datetime


@dataclass
class Job:
    id: str
    title: str
    description: str
    created_at: datetime
