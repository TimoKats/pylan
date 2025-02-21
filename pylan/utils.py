from datetime import datetime, timedelta
from typing import Any

DATE_FORMAT = "%Y-%m-%d"


def timedelta_from_str(interval: str) -> timedelta:
    count = int(interval[:-1])
    interval_type = interval[-1]
    if interval_type == "d":
        return timedelta(days=count)
    elif interval_type == "w":
        return timedelta(weeks=count)
    elif interval_type == "h":
        return timedelta(hours=count)
    elif interval_type == "m":
        return timedelta(minutes=count)  # NOTE: use relative timedelta and add months
    elif interval_type == "s":
        return timedelta(seconds=count)
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


def monthly_schedule(start: datetime, end: datetime) -> list[datetime]:
    dt_schedule = []
    current_month = start.month
    current_year = start.year
    current = start
    while current <= end:
        current = datetime(current_year, current_month, start.day)
        dt_schedule.append(current)
        current_month += 1
        if current_month == 13:
            current_year += 1
            current_month = 1
    return dt_schedule[:-1]


def timedelta_from_schedule(
    schedule: Any, start: datetime = None, end: datetime = None
) -> list[datetime]:
    if schedule == "monthly":
        return monthly_schedule(start, end)
    elif isinstance(schedule, str):
        return interval_schedule(start, end, schedule)
    elif isinstance(schedule, list) and all(isinstance(item, str) for item in schedule):
        return alt_interval_schedule(start, end, schedule)
    elif isinstance(schedule, list) and all(
        isinstance(item, datetime) for item in schedule
    ):
        return schedule
    raise Exception("Schedule format invalid.")


def keep_or_convert(date: str | datetime) -> datetime:
    return datetime.strptime(date, DATE_FORMAT) if isinstance(date, str) else date
