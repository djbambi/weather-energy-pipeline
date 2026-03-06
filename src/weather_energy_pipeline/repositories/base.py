from abc import ABC, abstractmethod

from weather_energy_pipeline.models.raw_payload import RawPayload


class DataSourceRepository(ABC):
    """Abstract base class for raw data source repositories."""

    @abstractmethod
    def fetch(self) -> RawPayload:
        """Fetch raw data from the source and return it as a RawPayload."""
