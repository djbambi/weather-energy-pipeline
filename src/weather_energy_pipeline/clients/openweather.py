import logging
from datetime import date
from typing import Any, Protocol

import requests

from weather_energy_pipeline.config.settings import Settings
from weather_energy_pipeline.models.fetch_window import FetchWindow

type RequestParams = dict[str, str | int | float]
type RequestHeaders = dict[str, str]

logger = logging.getLogger(__name__)


class SupportsResponse(Protocol):
    """Protocol for HTTP responses returned by the injected session."""

    def raise_for_status(self) -> None:
        """Raise an exception for HTTP error responses."""

    def json(self) -> Any:
        """Return the response payload parsed as JSON."""


class SupportsGet(Protocol):
    """Protocol for objects that support HTTP GET requests."""

    def get(
        self,
        url: str,
        params: RequestParams,
        headers: RequestHeaders,
        timeout: float,
    ) -> SupportsResponse:
        """Perform an HTTP GET request."""


class OpenWeatherApiClient:
    """Client for fetching weather data from the OpenWeather API."""

    def __init__(self, settings: Settings, session: SupportsGet | None = None) -> None:
        self._settings = settings
        self._session = session or requests.Session()

    def fetch_day_summary(
        self,
        window: FetchWindow,
        latitude: float,
        longitude: float,
    ) -> dict[str, Any]:
        """
        Fetch OpenWeather day summary data for a single-day window.

        Args:
            window: The date window to fetch. Must represent exactly one day.
            latitude: Latitude for the requested location.
            longitude: Longitude for the requested location.

        Returns:
            The JSON payload returned by the OpenWeather API.

        Raises:
            ValueError: If the supplied window spans more than one day.
            ValueError: If the response payload is not a JSON object.
            requests.HTTPError: If the API returns an HTTP error response.
        """
        self._validate_single_day_window(window)

        params: RequestParams = {
            "lat": latitude,
            "lon": longitude,
            "date": self._to_api_date(window.start_date),
            "appid": self._settings.openweather_api_key,
        }

        headers: RequestHeaders = {
            "Accept": "application/json",
        }

        logger.info(
            "Fetching day summary for %s (lat=%.4f, lon=%.4f)",
            window.start_date,
            latitude,
            longitude,
        )
        logger.debug(
            "Request params: lat=%s, lon=%s, date=%s", latitude, longitude, window.start_date
        )
        response = self._session.get(
            self._settings.openweather_base_url,
            params=params,
            headers=headers,
            timeout=self._settings.openweather_timeout_s,
        )
        response.raise_for_status()
        logger.info("Received response from OpenWeather API")

        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Expected OpenWeather response payload to be a JSON object")

        return payload

    @staticmethod
    def _validate_single_day_window(window: FetchWindow) -> None:
        """Ensure the supplied window represents exactly one day."""
        if window.start_date != window.end_date:
            raise ValueError("OpenWeather day summary requests require a single-day window")

    @staticmethod
    def _to_api_date(value: date) -> str:
        """Convert a date value to the format expected by the API."""
        return value.isoformat()
