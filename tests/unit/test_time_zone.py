"""Testing module for local timezone to UTC conversion"""

from datetime import datetime, timedelta, timezone
import pytz
from ticktick.helpers.time_methods import convert_local_time_to_utc, convert_date_to_tick_tick_format


def test_pacific_time():
    pst = datetime(2020, 12, 14, 1, 19, 0)
    expected_utc = datetime(2020, 12, 14, 9, 19, 0)
    assert convert_local_time_to_utc(pst, 'America/Los_Angeles') == expected_utc


def test_pacific_time_2():
    pst = datetime(2020, 12, 14, 1, 19, 0)
    expected_utc = datetime(2020, 12, 14, 9, 19, 0)
    assert convert_local_time_to_utc(pst, 'US/Pacific') == expected_utc


def test_pacific_time_midnight():
    pst = datetime(2020, 12, 14)
    expected_utc = datetime(2020, 12, 14, 8)
    assert convert_local_time_to_utc(pst, 'US/Pacific') == expected_utc


def test_pacific_time_11_59():
    pst = datetime(2020, 12, 11, 23, 59)
    expected_utc = datetime(2020, 12, 12, 7, 59)
    assert convert_local_time_to_utc(pst, 'US/Pacific') == expected_utc


def test_tokyo_time():
    tokyo = datetime(2020, 12, 14, 18, 38)
    expected_utc = datetime(2020, 12, 14, 9, 38)
    assert convert_local_time_to_utc(tokyo, 'Asia/Tokyo') == expected_utc


def test_convert_iso_to_tick_tick():
    date = datetime(2022, 12, 31, 14, 30, 45)
    expected = '2022-12-31T22:30:45+0000'
    assert convert_date_to_tick_tick_format(date, 'US/Pacific') == expected


def test_convert_iso_to_tick_tick_2():
    date = datetime(2022, 12, 31)
    expected = '2022-12-31T08:00:00+0000'
    assert convert_date_to_tick_tick_format(date, 'US/Pacific') == expected


# --- Tests for timezone-aware inputs (regression tests for the double-shift bug) ---

def test_tz_aware_utc_input_preserved():
    """A datetime already in UTC must round-trip unchanged regardless of time_zone arg."""
    aware = datetime(2026, 4, 26, 19, 45, tzinfo=timezone.utc)
    expected = datetime(2026, 4, 26, 19, 45)
    assert convert_local_time_to_utc(aware, 'Europe/London') == expected
    assert convert_local_time_to_utc(aware, 'US/Pacific') == expected


def test_tz_aware_bst_input_converts_to_utc():
    """A tz-aware datetime in BST (+01:00) should convert to the correct UTC wall time."""
    bst = datetime(2026, 4, 26, 20, 45, tzinfo=timezone(timedelta(hours=1)))
    expected = datetime(2026, 4, 26, 19, 45)
    assert convert_local_time_to_utc(bst, 'Europe/London') == expected


def test_tz_aware_pytz_zone_input():
    """A tz-aware datetime using a pytz zone should convert correctly."""
    pacific = pytz.timezone('US/Pacific').localize(datetime(2020, 12, 14, 1, 19))
    expected = datetime(2020, 12, 14, 9, 19)
    assert convert_local_time_to_utc(pacific, 'US/Pacific') == expected


def test_tz_aware_ignores_time_zone_arg():
    """The time_zone argument must be ignored when the input already carries tzinfo."""
    aware = datetime(2020, 6, 1, 12, 0, tzinfo=timezone(timedelta(hours=9)))  # JST
    expected = datetime(2020, 6, 1, 3, 0)
    # Pass a deliberately mismatched tz to prove it's ignored.
    assert convert_local_time_to_utc(aware, 'US/Pacific') == expected


def test_convert_iso_to_tick_tick_tz_aware():
    """convert_date_to_tick_tick_format should also preserve tz-aware wall time."""
    aware = datetime(2026, 4, 26, 20, 45, tzinfo=timezone(timedelta(hours=1)))
    expected = '2026-04-26T19:45:00+0000'
    assert convert_date_to_tick_tick_format(aware, 'Europe/London') == expected

