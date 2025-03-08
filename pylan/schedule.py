from datetime import datetime, timedelta
from typing import Any

from cron_converter import Cron
from dateutil.relativedelta import relativedelta

DATE_FORMAT = "%Y-%m-%d"


def keep_or_convert(date: str | datetime) -> datetime:
    """@private
    Accepts datetime or string and returns all as datetime.
    """
    return datetime.strptime(date, DATE_FORMAT) if isinstance(date, str) else date


def valid_dt(date: str | datetime) -> bool:
    """@private
    Returns true if string or datetime is valid datetime.
    """
    try:
        keep_or_convert(date)
        return True
    except ValueError:
        return False


def valid_cron(cron_schedule: str) -> bool:
    """@private
    Returns true if string is a valid cron
    """
    try:
        Cron(cron_schedule)
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def cron_schedule(cron_schedule, start: datetime, end: datetime) -> list[datetime]:
    """@private
    Iterates through cron schedule between a start and end date.
    """
    cron = Cron(cron_schedule)
    schedule = cron.schedule(start)
    dt_schedule = []
    while schedule.next() < end:
        dt_schedule.append(schedule.date)
    return dt_schedule


def timedelta_from_str(interval: str) -> timedelta:
    """@private
    Returns a timedelta object based on an interval string (like 2d, 3w, etc)
    """
    try:
        count = int(interval[:-1])
        interval_type = interval[-1]
    except (ValueError, TypeError):
        raise Exception("Schedule doesn't adhere to format. E.g. 1d, 2y.")
    if interval_type == "y":
        return relativedelta(years=count)
    elif interval_type == "m":
        return relativedelta(months=count)
    elif interval_type == "w":
        return relativedelta(weeks=count)
    elif interval_type == "d":
        return relativedelta(days=count)
    elif interval_type == "h":
        return relativedelta(hours=count)
    raise Exception("Inteval type " + interval_type + " not recognized.")


def interval_schedule(
    start: datetime, end: datetime, interval: str, include_start: bool
) -> list[datetime]:
    """@private
    Based on the timedelta from string, return a list of datetime objects between start
    and end.
    """
    dt_schedule = []
    interval = timedelta_from_str(interval)
    if include_start:
        dt_schedule.append(start)
    while start <= end:
        start += interval
        dt_schedule.append(start)
        if start >= end:
            break
    return dt_schedule


def alt_interval_schedule(
    start: datetime, end: datetime, interval: list[str], include_start: bool
) -> list[datetime]:
    """@private
    Based on a list with objects that have a timedelta from string, return a list of
    datetime objects between start and end.
    """
    interval_index = 0
    dt_schedule = []
    if include_start:
        dt_schedule.append(start)
    while start <= end:
        start += timedelta_from_str(interval[interval_index])
        dt_schedule.append(start)
        interval_index += 1
        if interval_index >= len(interval):
            interval_index = 0
        if start >= end:
            break
    return dt_schedule


def timedelta_from_schedule(
    schedule: Any,
    start: datetime = None,
    end: datetime = None,
    include_start: bool = False,
) -> list[datetime]:
    """@private
    Entrypoint of this submodule. Takes a string with some datetime objects and returns
    a list of datetime objects that represent the schedule.
    """
    if valid_cron(schedule):
        return cron_schedule(schedule, start, end)
    elif isinstance(schedule, str):
        return interval_schedule(start, end, schedule, include_start)
    elif isinstance(schedule, list) and all(valid_dt(i) for i in schedule):
        return [keep_or_convert(i) for i in schedule]
    elif isinstance(schedule, list) and all(isinstance(i, str) for i in schedule):
        return alt_interval_schedule(start, end, schedule, include_start)
    raise Exception("Schedule format " + str(schedule) + " invalid.")
