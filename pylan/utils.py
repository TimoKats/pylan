from datetime import timedelta


def timedelta_from_str(interval: str) -> timedelta:
    count = int(interval[0])
    interval_type = interval[1:]
    if interval_type == "d":
        return timedelta(days=count)
    elif interval_type == "w":
        return timedelta(weeks=count)
    elif interval_type == "h":
        return timedelta(hours=count)
    elif interval_type == "min":
        return timedelta(minutes=count)
    elif interval_type == "sec":
        return timedelta(seconds=count)
    raise Exception("Inteval type " + interval_type + " not recognized.")
