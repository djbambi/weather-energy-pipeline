from datetime import date

from rich import print as rprint

from weather_energy_pipeline.clients.openweather import OpenWeatherApiClient
from weather_energy_pipeline.config.dependencies import get_settings
from weather_energy_pipeline.models.fetch_window import FetchWindow


def main() -> None:
    settings = get_settings()
    client = OpenWeatherApiClient(settings=settings)

    window = FetchWindow(
        start_date=date(2026, 3, 6),
        end_date=date(2026, 3, 6),
    )

    payload = client.fetch_day_summary(
        window=window,
        latitude=54.9069,
        longitude=-1.3838,
    )

    rprint("Top-level keys:", list(payload.keys()))
    rprint("Payload preview:", payload)


if __name__ == "__main__":
    main()
