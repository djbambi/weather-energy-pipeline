import pytest
from pydantic import ValidationError

from weather_energy_pipeline.config.settings import Settings


@pytest.fixture()
def env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    """Provide a monkeypatch with the minimum required env vars pre-set."""
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-api-key")
    return monkeypatch


# ---- construction & defaults ----


def test_settings_loads_with_only_required_fields(env: pytest.MonkeyPatch) -> None:
    settings = Settings()

    assert settings.openweather_api_key == "test-api-key"
    # Verify defaults exist and satisfy their own constraints — don't hardcode values
    assert settings.openweather_timeout_s > 0
    assert settings.retry_initial_wait_seconds >= 0
    assert settings.retry_backoff_multiplier > 0
    assert settings.retry_max_wait_seconds > 0
    assert 0 <= settings.max_retry_attempts <= 10


def test_settings_base_url_points_to_expected_endpoint(env: pytest.MonkeyPatch) -> None:
    """The base URL is a critical contract — assert it explicitly."""
    settings = Settings()

    assert (
        settings.openweather_base_url
        == "https://api.openweathermap.org/data/3.0/onecall/day_summary"
    )


def test_settings_accepts_custom_values(env: pytest.MonkeyPatch) -> None:
    env.setenv("OPENWEATHER_TIMEOUT_S", "30.0")
    env.setenv("MAX_RETRY_ATTEMPTS", "5")

    settings = Settings()

    assert settings.openweather_timeout_s == 30.0
    assert settings.max_retry_attempts == 5


# ---- immutability ----


def test_settings_is_frozen(env: pytest.MonkeyPatch) -> None:
    settings = Settings()

    with pytest.raises(ValidationError):
        settings.openweather_api_key = "changed"  # type: ignore[misc]


# ---- missing / invalid fields ----


def test_settings_raises_when_api_key_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)

    with pytest.raises(ValidationError):
        Settings()


def test_settings_raises_when_api_key_is_empty(env: pytest.MonkeyPatch) -> None:
    env.setenv("OPENWEATHER_API_KEY", "")

    with pytest.raises(ValidationError):
        Settings()


@pytest.mark.parametrize(
    ("env_var", "bad_value"),
    [
        ("OPENWEATHER_TIMEOUT_S", "0"),
        ("OPENWEATHER_TIMEOUT_S", "-1"),
        ("RETRY_BACKOFF_MULTIPLIER", "0"),
        ("RETRY_MAX_WAIT_SECONDS", "0"),
        ("MAX_RETRY_ATTEMPTS", "11"),
    ],
    ids=[
        "timeout_zero",
        "timeout_negative",
        "backoff_zero",
        "max_wait_zero",
        "retry_exceeds_upper_bound",
    ],
)
def test_settings_raises_for_out_of_bounds_value(
    env: pytest.MonkeyPatch, env_var: str, bad_value: str
) -> None:
    env.setenv(env_var, bad_value)

    with pytest.raises(ValidationError):
        Settings()


# ---- extra env vars ----


def test_settings_ignores_extra_env_vars(env: pytest.MonkeyPatch) -> None:
    env.setenv("UNKNOWN_SETTING", "something")

    Settings()  # should not raise
