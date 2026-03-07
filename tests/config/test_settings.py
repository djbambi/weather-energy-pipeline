import pytest
from pydantic import ValidationError

from weather_energy_pipeline.config.settings import Settings


def test_settings_loads_required_and_default_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-api-key")

    settings = Settings()

    assert settings.openweather_api_key == "test-api-key"
    assert settings.openweather_timeout_s == 10.0
    assert (
        settings.openweather_base_url
        == "https://api.openweathermap.org/data/3.0/onecall/day_summary"
    )
    assert settings.retry_initial_wait_seconds == 1
    assert settings.retry_backoff_multiplier == 2.0
    assert settings.retry_max_wait_seconds == 60
    assert settings.max_retry_attempts == 3


def test_settings_raises_validation_error_when_api_key_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)

    with pytest.raises(ValidationError):
        Settings()


def test_settings_raises_validation_error_for_invalid_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-api-key")
    monkeypatch.setenv("OPENWEATHER_TIMEOUT_S", "0")

    with pytest.raises(ValidationError):
        Settings()
