import json
from typing import TYPE_CHECKING, Any, Protocol

from mypy_boto3_s3 import S3Client

from weather_energy_pipeline.models.raw_payload import RawPayload
from weather_energy_pipeline.storage.base import RawStorage

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


class SupportsS3PutObject(Protocol):
    """Protocol for objects that can write an object to S3."""

    def put_object(
        self,
        *,
        Bucket: str,
        Key: str,
        Body: str,
        ContentType: str,
    ) -> Any:
        """Write an object to S3."""


class Boto3S3ClientAdapter:
    """Adapter that makes a boto3 S3 client conform to SupportsS3PutObject."""

    def __init__(self, client: S3Client) -> None:
        self._client = client

    def put_object(
        self,
        *,
        Bucket: str,
        Key: str,
        Body: str,
        ContentType: str,
    ) -> Any:
        return self._client.put_object(
            Bucket=Bucket,
            Key=Key,
            Body=Body,
            ContentType=ContentType,
        )


class S3RawStorage(RawStorage):
    """Store raw ingestion payloads in an S3 Bronze layer."""

    def __init__(self, bucket_name: str, s3_client: SupportsS3PutObject) -> None:
        self._bucket_name = bucket_name
        self._s3_client = s3_client

    def store(self, payload: RawPayload) -> None:
        """Persist the supplied raw payload to S3."""
        key = self._build_key(payload)
        body = self._serialize_payload(payload)

        self._s3_client.put_object(
            Bucket=self._bucket_name,
            Key=key,
            Body=body,
            ContentType="application/json",
        )

    @staticmethod
    def _build_key(payload: RawPayload) -> str:
        extracted_date = payload.extracted_at.date()

        year = f"{extracted_date.year:04d}"
        month = f"{extracted_date.month:02d}"
        day = f"{extracted_date.day:02d}"

        return (
            f"bronze/{payload.dataset_name}/{payload.source_name}/"
            f"year={year}/month={month}/day={day}/payload.json"
        )

    @staticmethod
    def _serialize_payload(payload: RawPayload) -> str:
        document = {
            "dataset_name": payload.dataset_name,
            "source_type": payload.source_type,
            "source_name": payload.source_name,
            "extracted_at": payload.extracted_at.isoformat(),
            "content_type": payload.content_type,
            "payload": payload.payload,
        }
        return json.dumps(document)
