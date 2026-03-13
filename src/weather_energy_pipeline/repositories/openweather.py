import logging
from datetime import UTC, datetime

from weather_energy_pipeline.clients.openweather import OpenWeatherApiClient
from weather_energy_pipeline.models.fetch_window import FetchWindow
from weather_energy_pipeline.models.raw_payload import RawPayload
from weather_energy_pipeline.repositories.base import DataSourceRepository

logger = logging.getLogger(__name__)


class OpenWeatherRepository(DataSourceRepository):
    """Repository for fetching raw weather data from OpenWeather."""

    def __init__(
        self,
        client: OpenWeatherApiClient,
        latitude: float,
        longitude: float,
    ) -> None:
        self._client = client
        self._latitude = latitude
        self._longitude = longitude

    def fetch(self, window: FetchWindow) -> RawPayload:
        """Fetch raw OpenWeather data for the supplied window."""
        logger.info(
            "Fetching openweather data for %s → %s (%.2f, %.2f)",
            window.start_date,
            window.end_date,
            self._latitude,
            self._longitude,
        )
        payload = self._client.fetch_day_summary(
            window=window,
            latitude=self._latitude,
            longitude=self._longitude,
        )

        return RawPayload(
            dataset_name="weather",
            source_type="api",
            source_name="openweather",
            data_date=window.start_date,
            extracted_at=datetime.now(UTC),
            content_type="application/json",
            payload=payload,
        )
