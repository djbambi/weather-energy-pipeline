from abc import ABC, abstractmethod

from weather_energy_pipeline.models.raw_payload import RawPayload


class RawStorage(ABC):
    """Abstract storage for raw ingestion payloads."""

    @abstractmethod
    def store(self, payload: RawPayload) -> None:
        """Persist the supplied raw payload."""
