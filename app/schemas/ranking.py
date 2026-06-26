from pydantic import BaseModel, Field


class RankingItem(BaseModel):
    filename: str
    score: float = Field(ge=0.0, le=1.0)
    matched_skills: list[str]
    missing_skills: list[str]
    recommendation: str


class RankingResponse(BaseModel):
    rankings: list[RankingItem]
