import json
import logging
from dataclasses import asdict
from typing import TYPE_CHECKING, Any, Protocol

from mypy_boto3_s3 import S3Client

from weather_energy_pipeline.models.raw_payload import RawPayload
from weather_energy_pipeline.storage.base import RawStorage

logger = logging.getLogger(__name__)


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
        key = self._build_key(payload)
        body = self._serialize_payload(payload)

        logger.info("Storing payload to s3://%s/%s", self._bucket_name, key)

        self._s3_client.put_object(
            Bucket=self._bucket_name,
            Key=key,
            Body=body,
            ContentType="application/json",
        )

        logger.info("Payload stored successfully (%d bytes)", len(body))

    @staticmethod
    def _build_key(payload: RawPayload) -> str:
        year = f"{payload.data_date.year:04d}"
        month = f"{payload.data_date.month:02d}"
        day = f"{payload.data_date.day:02d}"

        return (
            f"bronze/{payload.dataset_name}/{payload.source_name}/"
            f"year={year}/month={month}/day={day}/payload.json"
        )

    @staticmethod
    def _serialize_payload(payload: RawPayload) -> str:
        document = asdict(payload)
        document["data_date"] = payload.data_date.isoformat()
        document["extracted_at"] = payload.extracted_at.isoformat()
        return json.dumps(document)
