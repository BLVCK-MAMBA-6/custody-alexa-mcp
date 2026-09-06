"""Environment-backed configuration for Custody."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or ``.env``."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"
    database_url: str | None = None


settings = Settings()
