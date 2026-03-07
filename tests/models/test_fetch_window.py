from datetime import date

import pytest

from weather_energy_pipeline.models.fetch_window import FetchWindow


def test_fetch_window_allows_same_start_and_end_date() -> None:
    window = FetchWindow(
        start_date=date(2026, 3, 7),
        end_date=date(2026, 3, 7),
    )

    assert window.start_date == date(2026, 3, 7)
    assert window.end_date == date(2026, 3, 7)


def test_fetch_window_allows_end_date_after_start_date() -> None:
    window = FetchWindow(
        start_date=date(2026, 3, 1),
        end_date=date(2026, 3, 7),
    )

    assert window.start_date == date(2026, 3, 1)
    assert window.end_date == date(2026, 3, 7)


def test_fetch_window_raises_error_when_end_date_is_before_start_date() -> None:
    with pytest.raises(
        ValueError,
        match="end_date must be greater than or equal to start_date",
    ):
        FetchWindow(
            start_date=date(2026, 3, 8),
            end_date=date(2026, 3, 7),
        )
