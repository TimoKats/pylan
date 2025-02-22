from datetime import datetime, timedelta
from typing import Any

from croniter import croniter
from dateutil.relativedelta import relativedelta

DATE_FORMAT = "%Y-%m-%d"


def keep_or_convert(date: str | datetime) -> datetime:
    return datetime.strptime(date, DATE_FORMAT) if isinstance(date, str) else date


def valid_dt(date: str | datetime) -> bool:
    try:
        keep_or_convert(date)
        return True
    except ValueError:
        return False


def valid_cron(cron_schedule):
    try:
        croniter(cron_schedule, datetime.now())
        return True
    except (ValueError, AttributeError):
        return False


def cron_schedule(cron_schedule, start: datetime, end: datetime):
    iter = croniter(cron_schedule, start)
    dt_schedule = []
    current = iter.get_next(datetime)
    while current <= end:
        dt_schedule.append(current)
        current = iter.get_next(datetime)
    return dt_schedule


def timedelta_from_str(interval: str) -> timedelta:
    count = int(interval[:-1]) if interval != "month" else 1
    interval_type = interval[-1] if interval != "month" else "month"
    if interval_type == "d":
        return relativedelta(days=count)
    elif interval_type == "w":
        return relativedelta(weeks=count)
    elif interval_type == "h":
        return relativedelta(hours=count)
    elif interval_type == "m":
        return relativedelta(minutes=count)
    elif interval_type == "s":
        return relativedelta(seconds=count)
    elif interval_type == "month":
        return relativedelta(months=1)
    raise Exception("Inteval type " + interval_type + " not recognized.")


def interval_schedule(start: datetime, end: datetime, interval: str) -> list[datetime]:
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
    if valid_cron(schedule):
        return cron_schedule(schedule, start, end)
    elif isinstance(schedule, str):
        return interval_schedule(start, end, schedule)
    elif isinstance(schedule, list) and all(valid_dt(i) for i in schedule):
        return [keep_or_convert(i) for i in schedule]
    elif isinstance(schedule, list) and all(isinstance(i, str) for i in schedule):
        return alt_interval_schedule(start, end, schedule)
    raise Exception("Schedule format " + str(schedule) + " invalid.")
