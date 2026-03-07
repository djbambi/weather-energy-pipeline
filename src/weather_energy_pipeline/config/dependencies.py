from functools import lru_cache

from weather_energy_pipeline.config.settings import Settings


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings()
