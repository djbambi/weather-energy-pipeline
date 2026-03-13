from datetime import UTC, date, datetime

from weather_energy_pipeline.models.raw_payload import RawPayload
from weather_energy_pipeline.storage.s3 import S3RawStorage


class DummyS3Client:
    def __init__(self) -> None:
        self.called_with: dict[str, object] | None = None

    def put_object(
        self,
        *,
        Bucket: str,
        Key: str,
        Body: str,
        ContentType: str,
    ) -> dict[str, object]:
        self.called_with = {
            "Bucket": Bucket,
            "Key": Key,
            "Body": Body,
            "ContentType": ContentType,
        }
        return {}


def test_store_writes_payload_to_expected_s3_key() -> None:
    s3_client = DummyS3Client()
    storage = S3RawStorage(
        bucket_name="weather-energy-bronze-dev",
        s3_client=s3_client,
    )

    payload = RawPayload(
        dataset_name="weather",
        source_type="api",
        source_name="openweather",
        data_date=date(2026, 3, 6),
        extracted_at=datetime(2026, 3, 6, 10, 30, 0, tzinfo=UTC),
        content_type="application/json",
        payload={"temperature": 12.3},
    )

    storage.store(payload)

    assert s3_client.called_with is not None
    assert s3_client.called_with["Bucket"] == "weather-energy-bronze-dev"
    assert (
        s3_client.called_with["Key"]
        == "bronze/weather/openweather/year=2026/month=03/day=06/payload.json"
    )
    assert s3_client.called_with["ContentType"] == "application/json"


def test_store_serializes_expected_fields() -> None:
    s3_client = DummyS3Client()
    storage = S3RawStorage(
        bucket_name="weather-energy-bronze-dev",
        s3_client=s3_client,
    )

    payload = RawPayload(
        dataset_name="weather",
        source_type="api",
        source_name="openweather",
        data_date=date(2026, 3, 6),
        extracted_at=datetime(2026, 3, 6, 10, 30, 0, tzinfo=UTC),
        content_type="application/json",
        payload={"temperature": 12.3},
    )

    storage.store(payload)

    assert s3_client.called_with is not None
    body = s3_client.called_with["Body"]

    assert isinstance(body, str)
    assert '"dataset_name": "weather"' in body
    assert '"source_name": "openweather"' in body
    assert '"content_type": "application/json"' in body


def test_build_key_zero_padded_month_and_day() -> None:
    payload = RawPayload(
        dataset_name="weather",
        source_type="api",
        source_name="openweather",
        data_date=date(2026, 1, 5),
        extracted_at=datetime(2026, 1, 5),
        content_type="application/json",
        payload={"test": "data"},
    )

    key = S3RawStorage._build_key(payload)

    assert "year=2026" in key
    assert "month=01" in key
    assert "day=05" in key
