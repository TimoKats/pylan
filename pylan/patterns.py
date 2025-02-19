from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Optional

from pylan.enums import Granularity, Operators
from pylan.result import Result
from pylan.utils import timedelta_from_schedule


@dataclass
class Pattern:
    schedule: str
    operator: Operators
    impact: Any

    iterations: Optional[int] = 1
    dt_schedule: Optional[list] = None

    def set_dt_schedule(self, start: datetime, end: datetime) -> None:
        self.dt_schedule = timedelta_from_schedule(self.schedule, start, end)

    def apply(self, item: Any) -> None:
        current_value = item.value
        item.value = self.operator.apply(current_value, self.impact)

    def scheduled(self, current: datetime) -> bool:
        if not self.dt_schedule:
            raise Exception("Datetime schedule not set.")
        if self.iterations >= len(self.dt_schedule):
            return False
        if current == self.dt_schedule[self.iterations]:
            self.iterations += 1
            return True
        return False


class Item:
    def __init__(self, name: str = "", value: int = 0) -> None:
        self.name = name
        self.patterns = []
        self.iterations = 0
        self.value = value  # NOTE: rename the parameter to start_value
        self.init_value = value  # to deal with multiple runs
        self.granularity = None

    def __str__(self) -> str:
        if len(self.name) > 1:
            return self.name[:2]
        return self.name

    def add_pattern(self, pattern: Pattern) -> None:
        pattern_granularity = Granularity.from_str(pattern.schedule)
        if not self.granularity:
            self.granularity = pattern_granularity
        elif pattern_granularity < self.granularity:
            self.granularity = pattern_granularity
        self.patterns.append(pattern)

    def run(self, start: datetime, end: datetime) -> list:
        self.value = self.init_value
        if not self.patterns:
            raise Exception("No patterns have been added.")
        [pattern.set_dt_schedule(start, end) for pattern in self.patterns]
        result = Result()
        current = start
        while current <= end:
            for pattern in self.patterns:
                if pattern.scheduled(current):
                    pattern.apply(self)
            current += self.granularity.timedelta
            result.add_result(current, self.value)
        return result

    def until(self, stop_value: float) -> timedelta:
        self.value = self.init_value
        start = datetime(2025, 1, 1)
        delta = timedelta()
        current = start
        if not self.patterns:
            raise Exception("No patterns have been added.")
        while self.value <= stop_value:
            [pattern.set_dt_schedule(start, current) for pattern in self.patterns]
            for pattern in self.patterns:
                if pattern.scheduled(current):
                    pattern.apply(self)
            current += self.granularity.timedelta
            delta += self.granularity.timedelta
        return delta

    def iterate(self):
        self.iterations += 1
        for pattern in self.patterns:
            pattern.apply(self)
