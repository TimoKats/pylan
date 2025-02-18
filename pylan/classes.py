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

    def apply(self, item: Any) -> None:  # fix typing
        current_value = item.value
        item.value = self.operator.apply(current_value, self.impact)

    def scheduled(self, current: datetime) -> bool:
        if not self.dt_schedule:
            raise Exception("Datetime schedule not set.")
        if self.iterations >= len(self.dt_schedule):
            return False
        if current == self.dt_schedule[self.iterations]:  # NOTE: check for granularity!
            self.iterations += 1  # NOTE: For example, daily granularity...
            return True  #  ...only requires day to be equal
        return False


class Item:
    def __init__(self, name: str = "", value: int = 0) -> None:
        self.name = name
        self.patterns = []
        self.iterations = 0
        self.value = value
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

    def until(self, stop_value: float) -> timedelta:  # NOTE: not finished!
        if not self.patterns:
            raise Exception("No patterns have been added.")
        [
            pattern.set_dt_schedule(datetime(2025, 1, 1), datetime(2026, 1, 1))
            for pattern in self.patterns
        ]
        delta = timedelta()
        current = datetime(2025, 1, 1)
        while self.value <= stop_value:
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


class Collection:
    def __init__(self, n: int) -> None:
        self.items = [Item() for _ in range(0, n)]
        self.start_dt = datetime.now()
        self.n = n

    def __str__(self) -> str:
        collection_str = ""
        for item in self.items:
            collection_str += str(item) + " "
        return collection_str

    def update(self, loc: int, item: Item) -> None:
        if loc > self.n:
            raise Exception("Location exceeds collection range.")
        self.items[loc] = item

    def add_pattern(self, pattern: Pattern) -> None:
        return
