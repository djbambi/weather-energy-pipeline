import logging
from datetime import UTC, date, datetime
from typing import Any

import requests

from weather_energy_pipeline.models.fetch_window import FetchWindow

logger = logging.getLogger(__name__)


class CarbonIntensityClient:
    """Client for fetching energy data from the Carbon-Intensity API."""

    BASE_URL = "https://api.carbonintensity.org.uk/regional/intensity"

    def __init__(self, session: requests.Session | None = None) -> None:
        self._session = session or requests.Session()

    def fetch_daily(
        self,
        window: FetchWindow,
        region: int,
    ) -> dict[str, Any]:
        # offset to 00:01 to avoid the API returning the last slot of the previous day
        start = self.format_utc(window.start_date, hour=0, minute=1)
        end = self.format_utc(window.end_date, hour=23, minute=30)
        full_url = f"{self.BASE_URL}/{start}/{end}/regionid/{region}"

        logger.info(
            "Fetching Carbon Intensity daily data for %s to %s (Region=%d)",
            window.start_date,
            window.end_date,
            region,
        )

        response = self._session.get(full_url, timeout=10.0)
        response.raise_for_status()

        logger.info("Received response from Carbon-Intensity API")

        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Expected Carbon-Intensity response to be a JSON object")

        return payload

    @staticmethod
    def format_utc(date_value: date, hour: int, minute: int = 0) -> str:
        dt = datetime(
            date_value.year,
            date_value.month,
            date_value.day,
            hour,
            minute,
            tzinfo=UTC,
        )
        return dt.strftime("%Y-%m-%dT%H:%MZ")
