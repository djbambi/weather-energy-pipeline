from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class RawPayload:
    """
    Container representing raw data fetched from a source system.

    This object is produced by ingestion repositories and represents the
    Bronze-layer payload before any transformation or validation occurs.
    """

    dataset_name: str
    source_type: str
    source_name: str
    extracted_at: datetime
    content_type: str
    payload: Any
