from datetime import UTC, datetime

from weather_energy_pipeline.clients.openmeteo import OpenMeteoClient
from weather_energy_pipeline.models.fetch_window import FetchWindow
from weather_energy_pipeline.models.raw_payload import RawPayload
from weather_energy_pipeline.repositories.base import DataSourceRepository


class OpenMeteoRepository(DataSourceRepository):
    """Repository for fetching raw weather data from Open-Meteo."""

    def __init__(
        self,
        client: OpenMeteoClient,
        latitude: float,
        longitude: float,
    ) -> None:
        self._client = client
        self._latitude = latitude
        self._longitude = longitude

    def fetch(self, window: FetchWindow) -> RawPayload:
        payload = self._client.fetch_daily(
            window=window,
            latitude=self._latitude,
            longitude=self._longitude,
        )

        return RawPayload(
            dataset_name="weather",
            source_type="api",
            source_name="openmeteo",
            extracted_at=datetime.now(UTC),
            content_type="application/json",
            payload=payload,
        )
