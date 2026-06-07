from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SUBSMITH_", env_file=".env", extra="ignore")

    whisper_model: str = "small"
    device: str = "cpu"
    compute_type: str = "int8"

    source_language: str | None = None
    target_language: str = "el"

    translation_workers: int = Field(default=8, ge=1, le=64)
    translation_max_retries: int = Field(default=3, ge=0, le=10)

    subtitle_font_size: int = Field(default=24, ge=8, le=96)
    audio_sample_rate: int = 16000

    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
