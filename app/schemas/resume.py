from pydantic import BaseModel, Field


class ResumeAnalyzeResponse(BaseModel):
    filename: str
    cleaned_text: str
    skills: list[str]
