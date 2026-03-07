"""Application runtime settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    openweather_api_key: str = Field(
        min_length=1,
        description="API key for the OpenWeather API.",
    )
    openweather_base_url: str = Field(
        default="https://api.openweathermap.org/data/3.0/onecall/day_summary",
        description="Base URL for the OpenWeather day summary endpoint.",
    )
    openweather_timeout_s: float = Field(
        default=10.0,
        gt=0,
        description="HTTP timeout in seconds for OpenWeather requests.",
    )
    retry_initial_wait_seconds: int = Field(default=1, ge=0)
    retry_backoff_multiplier: float = Field(default=2.0, gt=0)
    retry_max_wait_seconds: int = Field(default=60, gt=0)
    max_retry_attempts: int = Field(default=3, ge=0, le=10)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )
