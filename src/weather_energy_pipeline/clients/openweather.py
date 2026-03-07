from typing import Any

import requests
from requests import Session

from weather_energy_pipeline.config.settings import Settings
from weather_energy_pipeline.models.fetch_window import FetchWindow

type RequestParams = dict[str, str | int | float]


class OpenWeatherApiClient:
    """Client for fetching weather data from the OpenWeather API."""

    def __init__(self, settings: Settings, session: Session | None = None) -> None:
        self._settings = settings
        self._session = session or requests.Session()

    def fetch_day_summary(
        self,
        window: FetchWindow,
        latitude: float,
        longitude: float,
    ) -> dict[str, Any]:
        if window.start_date != window.end_date:
            raise ValueError("OpenWeather day summary requests require a single-day window")

        params: RequestParams = {
            "lat": latitude,
            "lon": longitude,
            "date": window.start_date.isoformat(),
            "appid": self._settings.openweather_api_key,
        }

        response = self._session.get(
            self._settings.openweather_base_url,
            params=params,
            headers={"Accept": "application/json"},
            timeout=self._settings.openweather_timeout_s,
        )
        response.raise_for_status()

        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Expected OpenWeather response payload to be a JSON object")

        return payload
