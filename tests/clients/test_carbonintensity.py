from datetime import date

from weather_energy_pipeline.clients.carbon_intensity import CarbonIntensityClient
from weather_energy_pipeline.models.fetch_window import FetchWindow

window = FetchWindow(
    start_date=date(2026, 3, 2),
    end_date=date(2026, 3, 2),
)
region = 3


def test_build_url_formats_dates_and_region_correctly():
    fetched_url = CarbonIntensityClient._build_url(window, region)
    expected = "https://api.carbonintensity.org.uk/regional/intensity/2026-03-02T00:00Z/2026-03-02T23:30Z/regionid/3"
    assert fetched_url == expected


def test_format_utc_produces_correct_iso_format():
    formatted_date = CarbonIntensityClient.format_utc(date(2026, 3, 2), hour=0, minute=1)
    expected = "2026-03-02T00:01Z"
    assert formatted_date == expected
