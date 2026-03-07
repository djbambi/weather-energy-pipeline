from abc import ABC, abstractmethod

from weather_energy_pipeline.models.fetch_window import FetchWindow
from weather_energy_pipeline.models.raw_payload import RawPayload


class DataSourceRepository(ABC):
    """Abstract base class for raw data source repositories."""

    @abstractmethod
    def fetch(self, window: FetchWindow) -> RawPayload:
        """Fetch raw source data for the provided time window."""
