from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    # -------------------------
    # OpenWeather API
    # -------------------------

    openweather_api_key: str = Field(
        min_length=1,
        description="API key for the OpenWeather API",
    )

    openweather_timeout_s: float = Field(default=10.0, gt=0)

    openweather_base_url: str = Field(
        default="https://api.openweathermap.org/data/3.0/onecall/day_summary",
    )

    retry_initial_wait_seconds: int = Field(default=1, ge=0)
    max_retry_attempts: int = Field(default=3, ge=0, le=10)
    retry_backoff_multiplier: float = Field(default=2.0, gt=0)
    retry_max_wait_seconds: int = Field(default=60, gt=0)

    # -------------------------
    # S3 Bronze Storage
    # -------------------------

    bronze_bucket_name: str = Field(
        min_length=3,
        max_length=63,
        pattern=r"^[a-z0-9][a-z0-9\-]{1,61}[a-z0-9]$",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
        frozen=True,
    )
