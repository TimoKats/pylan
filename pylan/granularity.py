from datetime import timedelta
from enum import Enum

from dateutil.relativedelta import relativedelta


class Granularity(Enum):
    """@private
    Refers to the minimum step size needed for iterations given a set of patterns.
    """

    hour = "h"
    day = "d"
    week = "w"
    month = "m"
    year = "y"

    def __lt__(self, granularity):
        return self.rank < granularity.rank

    @staticmethod
    def from_str(value: str):
        for level in Granularity:
            if level.value in value:
                return level
        return Granularity.day  # NOTE: cron, or set of datetimes

    @property
    def rank(self) -> int:
        if self == Granularity.hour:
            return 3
        elif self == Granularity.day:
            return 4
        elif self == Granularity.week:
            return 5
        elif self == Granularity.month:
            return 6
        return 7

    @property
    def timedelta(self) -> timedelta:
        if self == Granularity.hour:
            return relativedelta(hours=1)
        elif self == Granularity.day:
            return relativedelta(days=1)
        elif self == Granularity.week:
            return relativedelta(weeks=1)
        elif self == Granularity.month:
            return relativedelta(months=1)
        raise Exception("Granularity not found.")
