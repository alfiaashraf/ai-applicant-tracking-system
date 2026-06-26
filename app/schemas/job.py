from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Short job title shown in the recruiter dashboard.",
        examples=["Python Backend Developer"],
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Full job description used for candidate ranking.",
        examples=[
            "We are looking for a Python Backend Developer with FastAPI and SQL experience."
        ],
    )


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="Unique job identifier.")
    title: str = Field(description="Job title.")
    description: str = Field(description="Full job description.")
    created_at: datetime = Field(description="UTC timestamp when the job was created.")
