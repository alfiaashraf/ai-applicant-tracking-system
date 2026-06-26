from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AI Applicant Tracking System"
    app_version: str = "1.0.0"
    upload_dir: str = "uploads"
    max_upload_size_mb: int = 10
    allowed_extensions: frozenset[str] = frozenset({".pdf"})
    embedding_model: str = "all-MiniLM-L6-v2"
    tfidf_weight: float = 0.4
    semantic_weight: float = 0.6
    strong_score_threshold: float = 0.7
    moderate_score_threshold: float = 0.4
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
