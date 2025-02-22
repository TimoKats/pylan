from datetime import timedelta
from enum import Enum
from typing import Any

from dateutil.relativedelta import relativedelta


class Operators(Enum):
    add = 1
    subtract = 2
    multiply = 3
    divide = 4
    replace = 5
    quad = 6

    def apply(self, value: float, impact: float) -> Any:
        if self == Operators.add:
            return value + impact
        elif self == Operators.subtract:
            return value - impact
        elif self == Operators.multiply:
            return value * impact
        elif self == Operators.divide:
            return value / impact
        elif self == Operators.replace:
            return impact
        elif self == Operators.quad:
            return value**impact
        raise Exception("Operator has no defined action.")


class Granularity(Enum):
    month = "month"
    second = "s"
    minute = "m"
    hour = "h"
    day = "d"
    week = "w"
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
        if self == Granularity.second:
            return 1
        elif self == Granularity.minute:
            return 2
        elif self == Granularity.hour:
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
        if self == Granularity.second:
            return relativedelta(seconds=1)
        elif self == Granularity.minute:
            return relativedelta(minutes=1)
        elif self == Granularity.hour:
            return relativedelta(hours=1)
        elif self == Granularity.day:
            return relativedelta(days=1)
        elif self == Granularity.week:
            return relativedelta(weeks=1)
        elif self == Granularity.month:
            return relativedelta(months=1)
        raise Exception("Granularity not found.")
