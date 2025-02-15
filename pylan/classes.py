# start working with set enums or types to pick granularity from.


from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from pylan.enums import Granularity, Operators
from pylan.utils import timedelta_from_str


@dataclass
class Pattern:
    schedule: str
    attribute: str
    operator: Operators
    impact: Any

    iterations: Optional[int] = 1
    dt_schedule: Optional[list] = None

    def set_dt_schedule(self, start: datetime, end: datetime) -> None:
        interval = timedelta_from_str(self.schedule)
        self.dt_schedule = []
        current = start
        while current <= end:
            self.dt_schedule.append(current)
            current += interval

    def apply(self, item: Any) -> None:  # fix typing
        current_value = item.attr[self.attribute]
        item.attr[self.attribute] = self.operator.apply(current_value, self.impact)

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
    def __init__(self, name: str = ".", attr: dict = {}) -> None:
        self.name = name
        self.start_dt = datetime.today()
        self.patterns = []
        self.iterations = 0
        self.attr = attr
        self.granularity = None

    def __str__(self) -> str:
        if len(self.name) > 1:
            return self.name[:2]
        return self.name

    def add_attribute(self, name: str, value: Any) -> None:
        self.attr[name] = value

    def add_pattern(self, pattern: Pattern) -> None:
        pattern_granularity = Granularity.from_str(pattern.schedule)
        if not self.granularity:
            self.granularity = pattern_granularity
        elif pattern_granularity < self.granularity:
            self.granularity = pattern_granularity
        self.patterns.append(pattern)

    def run(self, start: datetime, end: datetime, interval: str) -> list:
        if not self.patterns:
            raise Exception("No patterns have been added.")
        [pattern.set_dt_schedule(start, end) for pattern in self.patterns]
        current = start
        while current <= end:
            for pattern in self.patterns:
                if pattern.scheduled(current):
                    pattern.apply(self)
            current += self.granularity.timedelta()
        return []

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
