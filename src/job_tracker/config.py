from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./job_tracker.db"
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", env_prefix="JOB_TRACKER_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
