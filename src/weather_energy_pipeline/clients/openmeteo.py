import logging
from typing import Any

import requests

from weather_energy_pipeline.models.fetch_window import FetchWindow

logger = logging.getLogger(__name__)


class OpenMeteoClient:
    """Client for fetching weather data from the Open-Meteo API."""

    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    def __init__(self, session: requests.Session | None = None) -> None:
        self._session = session or requests.Session()

    def fetch_daily(
        self,
        window: FetchWindow,
        latitude: float,
        longitude: float,
    ) -> dict[str, Any]:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": window.start_date.isoformat(),
            "end_date": window.end_date.isoformat(),
            "hourly": "temperature_2m",
        }

        logger.info(
            "Fetching Open-Meteo daily data for %s to %s (lat=%.4f, lon=%.4f)",
            window.start_date,
            window.end_date,
            latitude,
            longitude,
        )

        response = self._session.get(self.BASE_URL, params=params, timeout=10.0)
        response.raise_for_status()

        logger.info("Received response from Open-Meteo API")

        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Expected Open-Meteo response to be a JSON object")

        return payload
