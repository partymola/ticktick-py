"""
Useful time conversion methods.
"""

import pytz

from ticktick.helpers.constants import DATE_FORMAT
import datetime


def convert_local_time_to_utc(original_time, time_zone: str):
    """
    Converts the datetime object to UTC time. Utilizes the time_zone string for proper conversion.

    Arguments:
        original_time (datetime): Datetime object
        time_zone: Time zone of `original_time`

    Returns:
        datetime: Datetime object with the converted UTC time - with no timezone information attached.

    ??? info "Import Help"
        ```python
        from ticktick.helpers.time_methods import convert_local_time_to_utc
        ```

    ??? Example
        ```python
        pst = datetime(2020, 12, 11, 23, 59)
        converted = convert_local_time_to_utc(pst, 'US/Pacific')
        ```

        ??? success "Result"
            A datetime object that is the UTC equivalent of the original date.

            ```python
            datetime(2020, 12, 12, 7, 59)
            ```
    """

    utc = pytz.utc
    # If the input is already timezone-aware, convert directly to UTC. The
    # original code path round-trips the datetime through strftime/strptime,
    # which silently strips any existing tzinfo and then re-localises the
    # naive wall clock as the supplied time_zone - double-shifting tz-aware
    # inputs (e.g. '20:45+01:00' returned '18:45' UTC instead of '19:45').
    if original_time.tzinfo is not None:
        return original_time.astimezone(utc).replace(tzinfo=None)
    time_zone = pytz.timezone(time_zone)
    original_time = original_time.strftime(DATE_FORMAT)
    time_object = datetime.datetime.strptime(original_time, DATE_FORMAT)
    time_zone_dt = time_zone.localize(time_object)
    return time_zone_dt.astimezone(utc).replace(tzinfo=None)


def convert_date_to_tick_tick_format(datetime_obj, tz: str):
    """
    Parses ISO 8601 Format to Tick Tick Date Format

    It first converts the datetime object to UTC time based off the passed time zone, and then
    returns a string with the TickTick required date format.

    !!! info Required Format
        ISO 8601 Format Example: 2020-12-23T01:56:07+00:00

        TickTick Required Format: 2020-12-23T01:56:07+0000 -> Where the last colon is removed for timezone

    Arguments:
        datetime_obj (datetime): Datetime object to be parsed.
        tz: Time zone string.

    Returns:
        str: The TickTick accepted date string.

    ??? info "Import Help"
        ```python
        from ticktick.helpers.time_methods import convert_iso_to_tick_tick_format
        ```

    ??? example
        ```python
        date = datetime(2022, 12, 31, 14, 30, 45)
        converted_date = convert_iso_to_tick_tick_format(date, 'US/Pacific')
        ```

        ??? success "Result"
            The proper format for a date string to be used with TickTick dates.

            ```python
            '2022-12-31T22:30:45+0000'
            ```
    """
    date = convert_local_time_to_utc(datetime_obj, tz)
    date = date.replace(tzinfo=datetime.timezone.utc).isoformat()
    date = date[::-1].replace(":", "", 1)[::-1]
    return date
