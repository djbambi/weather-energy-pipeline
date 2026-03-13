from datetime import date, datetime

from weather_energy_pipeline.models.fetch_window import FetchWindow
from weather_energy_pipeline.repositories.openmeteo import OpenMeteoRepository


class DummyClient:
    """Records calls and returns a canned payload."""

    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.called_with: dict | None = None

    def fetch_daily(self, *, window: FetchWindow, latitude: float, longitude: float) -> dict:
        self.called_with = {
            "window": window,
            "latitude": latitude,
            "longitude": longitude,
        }
        return self.payload


SAMPLE_PAYLOAD = {"hourly": {"temperature_2m": [1.0, 2.0]}}

WINDOW = FetchWindow(start_date=date(2025, 6, 1), end_date=date(2025, 6, 2))


def test_fetch_returns_raw_payload_with_correct_metadata():
    client = DummyClient(payload=SAMPLE_PAYLOAD)
    repo = OpenMeteoRepository(client=client, latitude=51.5, longitude=-0.1)

    result = repo.fetch(WINDOW)

    assert result.dataset_name == "weather"
    assert result.source_type == "api"
    assert result.source_name == "openmeteo"
    assert result.content_type == "application/json"
    assert result.payload == SAMPLE_PAYLOAD
    assert isinstance(result.extracted_at, datetime)
    assert result.data_date == WINDOW.start_date


def test_fetch_passes_window_and_coordinates_to_client():
    client = DummyClient(payload=SAMPLE_PAYLOAD)
    repo = OpenMeteoRepository(client=client, latitude=40.7, longitude=-74.0)

    repo.fetch(WINDOW)

    assert client.called_with == {
        "window": WINDOW,
        "latitude": 40.7,
        "longitude": -74.0,
    }
