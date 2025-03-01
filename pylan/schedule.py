from datetime import datetime, timedelta
from typing import Any

from croniter import croniter
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
        croniter(cron_schedule, datetime.now())
        return True
    except (ValueError, AttributeError):
        return False


def cron_schedule(cron_schedule, start: datetime, end: datetime) -> list[datetime]:
    """@private
    Iterates through cron schedule between a start and end date.
    """
    iter = croniter(cron_schedule, start)
    dt_schedule = []
    current = iter.get_next(datetime)
    while current <= end:
        dt_schedule.append(current)
        current = iter.get_next(datetime)
    return dt_schedule


def timedelta_from_str(interval: str) -> timedelta:
    """@private
    Returns a timedelta object based on an interval string (like 2d, 3w, etc)
    """
    try:
        count = int(interval[:-1])  # error handle here for value error.
        interval_type = interval[-1]
    except ValueError:
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


def interval_schedule(start: datetime, end: datetime, interval: str) -> list[datetime]:
    """@private
    Based on the timedelta from string, return a list of datetime objects between start
    and end.
    """
    dt_schedule = []
    interval = timedelta_from_str(interval)
    current = start
    while current <= end:
        dt_schedule.append(current)
        current += interval
    return dt_schedule


def alt_interval_schedule(
    start: datetime, end: datetime, interval: list[str]
) -> list[datetime]:
    """@private
    Based on a list with objects that have a timedelta from string, return a list of
    datetime objects between start and end.
    """
    interval_index = 0
    dt_schedule = []
    current = start
    while current <= end:
        interval_dt = timedelta_from_str(interval[interval_index])
        dt_schedule.append(current)
        current += interval_dt
        interval_index += 1
        if interval_index >= len(interval):
            interval_index = 0
    return dt_schedule


def timedelta_from_schedule(
    schedule: Any, start: datetime = None, end: datetime = None
) -> list[datetime]:  # NOTE: entrypoint of this submodule
    """@private
    Entrypoint of this submodule. Takes a string with some datetime objects and returns
    a list of datetime objects that represent the schedule.
    """
    if valid_cron(schedule):
        return cron_schedule(schedule, start, end)
    elif isinstance(schedule, str):
        return interval_schedule(start, end, schedule)
    elif isinstance(schedule, list) and all(valid_dt(i) for i in schedule):
        return [keep_or_convert(i) for i in schedule]
    elif isinstance(schedule, list) and all(isinstance(i, str) for i in schedule):
        return alt_interval_schedule(start, end, schedule)
    raise Exception("Schedule format " + str(schedule) + " invalid.")
