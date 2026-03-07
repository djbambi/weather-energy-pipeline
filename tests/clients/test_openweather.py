from datetime import date
from typing import Any

import pytest

from weather_energy_pipeline.clients.openweather import OpenWeatherApiClient
from weather_energy_pipeline.config.settings import Settings
from weather_energy_pipeline.models.fetch_window import FetchWindow


class DummyResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return self._payload


class DummySession:
    def __init__(self) -> None:
        self.called_with: dict[str, Any] | None = None

    def get(
        self,
        url: str,
        params: dict[str, Any],
        headers: dict[str, str],
        timeout: float,
    ) -> DummyResponse:
        self.called_with = {
            "url": url,
            "params": params,
            "headers": headers,
            "timeout": timeout,
        }
        return DummyResponse({"ok": True})


@pytest.fixture()
def settings(monkeypatch: pytest.MonkeyPatch) -> Settings:
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-api-key")
    return Settings()


def test_fetch_day_summary_builds_expected_request(settings: Settings) -> None:
    session = DummySession()
    client = OpenWeatherApiClient(settings=settings, session=session)

    window = FetchWindow(
        start_date=date(2026, 3, 7),
        end_date=date(2026, 3, 7),
    )

    payload = client.fetch_day_summary(
        window=window,
        latitude=54.9069,
        longitude=-1.3838,
    )

    assert payload == {"ok": True}
    assert session.called_with is not None
    assert session.called_with["url"] == settings.openweather_base_url
    assert session.called_with["params"] == {
        "lat": 54.9069,
        "lon": -1.3838,
        "date": "2026-03-07",
        "appid": "test-api-key",
    }
    assert session.called_with["headers"] == {
        "Accept": "application/json",
    }
    assert session.called_with["timeout"] == settings.openweather_timeout_s


def test_fetch_day_summary_raises_for_multi_day_window(settings: Settings) -> None:
    session = DummySession()
    client = OpenWeatherApiClient(settings=settings, session=session)

    window = FetchWindow(
        start_date=date(2026, 3, 7),
        end_date=date(2026, 3, 8),
    )

    with pytest.raises(
        ValueError,
        match="OpenWeather day summary requests require a single-day window",
    ):
        client.fetch_day_summary(
            window=window,
            latitude=54.9069,
            longitude=-1.3838,
        )
