import logging
from datetime import UTC, datetime

from weather_energy_pipeline.clients.carbon_intensity import CarbonIntensityClient
from weather_energy_pipeline.models.fetch_window import FetchWindow
from weather_energy_pipeline.models.raw_payload import RawPayload
from weather_energy_pipeline.repositories.base import DataSourceRepository

logger = logging.getLogger(__name__)


class CarbonIntensityRepository(DataSourceRepository):
    """Repository for fetching raw energy data from Carbon Intensity."""

    def __init__(
        self,
        client: CarbonIntensityClient,
        region: int,
    ) -> None:
        self._client = client
        self._region = region

    def fetch(self, window: FetchWindow) -> RawPayload:
        logger.info(
            "Fetching carbon intensity data for %s to %s (region %d)",
            window.start_date,
            window.end_date,
            self._region,
        )

        payload = self._client.fetch_daily(
            window=window,
            region=self._region,
        )

        return RawPayload(
            dataset_name="energy",
            source_type="api",
            source_name="carbon_intensity",
            data_date=window.start_date,
            extracted_at=datetime.now(UTC),
            content_type="application/json",
            payload=payload,
        )
