from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class FetchWindow:
    """
    Represents the time window for which data should be fetched
    from a source system.
    """

    start_date: date
    end_date: date

    def __post_init__(self) -> None:
        if self.end_date < self.start_date:
            raise ValueError("end_date must be greater than or equal to start_date")
