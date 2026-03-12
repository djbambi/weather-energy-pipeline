from datetime import date
from typing import Any

from weather_energy_pipeline.clients.openmeteo import OpenMeteoClient
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
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> DummyResponse:
        self.called_with = {
            "url": url,
            "params": params,
            "timeout": timeout,
        }
        return DummyResponse({"daily": {"temperature_2m": [8.5]}})


def test_fetch_daily_builds_expected_request() -> None:
    session = DummySession()
    client = OpenMeteoClient(session=session)

    window = FetchWindow(start_date=date(2026, 3, 10), end_date=date(2026, 3, 10))
    payload = client.fetch_daily(window, latitude=54.9069, longitude=-1.3838)

    assert payload == {"daily": {"temperature_2m": [8.5]}}
    assert session.called_with is not None
    assert session.called_with["url"] == OpenMeteoClient.BASE_URL
    assert session.called_with["params"] == {
        "latitude": 54.9069,
        "longitude": -1.3838,
        "start_date": "2026-03-10",
        "end_date": "2026-03-10",
        "hourly": "temperature_2m",
    }
    assert session.called_with["timeout"] == 10.0


def test_fetch_daily_raises_for_non_dict_response() -> None:
    class ListResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> list[str]:
            return ["not", "a", "dict"]

    class ListSession:
        def get(self, *args: Any, **kwargs: Any) -> ListResponse:
            return ListResponse()

    client = OpenMeteoClient(session=ListSession())
    window = FetchWindow(start_date=date(2026, 3, 10), end_date=date(2026, 3, 10))

    import pytest

    with pytest.raises(ValueError, match="Expected Open-Meteo response to be a JSON object"):
        client.fetch_daily(window, latitude=54.9069, longitude=-1.3838)
