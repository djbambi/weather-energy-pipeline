from datetime import date

import boto3
from mypy_boto3_s3 import S3Client

from weather_energy_pipeline.clients.openweather import OpenWeatherApiClient
from weather_energy_pipeline.config.dependencies import get_settings
from weather_energy_pipeline.models.fetch_window import FetchWindow
from weather_energy_pipeline.repositories.openweather import OpenWeatherRepository
from weather_energy_pipeline.storage.s3 import Boto3S3ClientAdapter, S3RawStorage


def main() -> None:
    settings = get_settings()

    # API layer
    api_client = OpenWeatherApiClient(settings=settings)

    repository = OpenWeatherRepository(
        client=api_client,
        latitude=54.9069,
        longitude=-1.3838,
    )

    # Storage layer
    raw_s3_client: S3Client = boto3.client("s3")
    s3_client = Boto3S3ClientAdapter(raw_s3_client)

    storage = S3RawStorage(
        bucket_name=settings.bronze_bucket_name,
        s3_client=s3_client,
    )

    window = FetchWindow(
        start_date=date(2026, 3, 7),
        end_date=date(2026, 3, 7),
    )

    raw_payload = repository.fetch(window)

    storage.store(raw_payload)


if __name__ == "__main__":
    main()
