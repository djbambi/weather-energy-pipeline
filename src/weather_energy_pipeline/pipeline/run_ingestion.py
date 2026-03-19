import argparse
import json
import logging
from datetime import date

import boto3
from mypy_boto3_s3 import S3Client
from rich.logging import RichHandler

from weather_energy_pipeline.clients.carbon_intensity import CarbonIntensityClient
from weather_energy_pipeline.clients.openmeteo import OpenMeteoClient
from weather_energy_pipeline.clients.openweather import OpenWeatherApiClient
from weather_energy_pipeline.config.dependencies import get_settings
from weather_energy_pipeline.models.fetch_window import FetchWindow
from weather_energy_pipeline.repositories.openmeteo import OpenMeteoRepository
from weather_energy_pipeline.repositories.openweather import OpenWeatherRepository
from weather_energy_pipeline.storage.s3 import Boto3S3ClientAdapter, S3RawStorage


def _parse_args() -> date:
    parser = argparse.ArgumentParser(description="Run the weather/energy ingestion pipeline.")
    parser.add_argument(
        "--date",
        required=True,
        type=date.fromisoformat,
        metavar="YYYY-MM-DD",
        help="The date to fetch data for (e.g. 2026-03-02).",
    )
    return parser.parse_args().date


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s — %(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    target_date = _parse_args()
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
        start_date=target_date,
        end_date=target_date,
    )

    raw_payload = repository.fetch(window)
    storage.store(raw_payload)

    # Open-Meteo (no API key needed)
    openmeteo_client = OpenMeteoClient()
    openmeteo_repo = OpenMeteoRepository(
        client=openmeteo_client,
        latitude=54.9069,
        longitude=-1.3838,
    )

    openmeteo_payload = openmeteo_repo.fetch(window)
    storage.store(openmeteo_payload)

    client = CarbonIntensityClient()
    window = FetchWindow(start_date=date(2026, 3, 18), end_date=date(2026, 3, 18))
    data = client.fetch_daily(window=window, region=3)
    print(json.dumps(data, indent=2)[:3000])


if __name__ == "__main__":
    main()
