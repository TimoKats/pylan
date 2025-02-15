from datetime import timedelta
from enum import Enum
from typing import Any


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
    second = "sec"
    minute = "min"
    hour = "h"
    day = "d"
    week = "w"
    year = "y"

    def __lt__(self, granularity):
        return self.timedelta() < granularity.timedelta()

    @staticmethod
    def from_str(value: str):
        for level in Granularity:
            if level.value in value:
                return level
        return Granularity.day  # always ok :)

    def timedelta(self) -> timedelta:
        if self == Granularity.second:
            return timedelta(seconds=1)
        elif self == Granularity.minute:
            return timedelta(minutes=1)
        elif self == Granularity.hour:
            return timedelta(hour=1)
        elif self == Granularity.day:
            return timedelta(days=1)
        elif self == Granularity.week:
            return timedelta(weeks=1)
        return timedelta(year=1)
