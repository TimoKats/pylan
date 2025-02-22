from datetime import datetime, timedelta

from pylan.enums import Granularity
from pylan.pattern import Pattern
from pylan.result import Result
from pylan.schedule import keep_or_convert


class Item:
    def __init__(self, name: str = "", start_value: int = 0) -> None:
        self.name = name
        self.patterns = []
        self.iterations = 0
        self.value = start_value
        self.start_value = start_value  # to deal with multiple runs
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

    def add_patterns(self, patterns: list[Pattern]) -> None:
        try:
            for pattern in patterns:
                self.add_pattern(pattern)
        except TypeError:
            raise Exception("parameter is not list, use add_pattern instead.")

    def run(self, start: datetime | str, end: datetime | str) -> list:
        # all the setup
        if not self.patterns:
            raise Exception("No patterns have been added.")
        start = keep_or_convert(start)
        end = keep_or_convert(end)
        [pattern.set_dt_schedule(start, end) for pattern in self.patterns]
        self.value = self.start_value
        result = Result()
        # run between start and end date
        while start <= end:
            for pattern in self.patterns:
                if pattern.scheduled(start):
                    pattern.apply(self)
            result.add_result(start, self.value)
            start += self.granularity.timedelta
        return result

    def until(self, stop_value: float) -> timedelta:
        self.value = self.start_value
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
