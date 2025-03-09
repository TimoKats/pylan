from datetime import datetime, timedelta

from pylan.granularity import Granularity
from pylan.patterns import Pattern
from pylan.result import Result
from pylan.schedule import keep_or_convert


class Item:
    """
    An item that you can apply patterns to and simulate over time. Optionally, you can
    set a start value.

    >>> savings = Item(start_value=100)
    """

    def __init__(self, start_value: int = 0) -> None:
        self.patterns = []
        self.iterations = 0
        self.value = start_value if start_value else 0
        self.start_value = start_value if start_value else 0
        self.granularity = None

    def add_pattern(self, pattern: Pattern) -> None:
        """@public
        Add a pattern object to this item.

        >>> test = Add(["2024-1-4", "2024-2-1"], 1)
        >>> savings = Item(start_value=100)
        >>> savings.add_pattern(test)
        """
        pattern_granularity = Granularity.from_str(pattern.schedule)
        if not self.granularity:
            self.granularity = pattern_granularity
        elif pattern_granularity < self.granularity:
            self.granularity = pattern_granularity
        self.patterns.append(pattern)

    def add_patterns(self, patterns: list[Pattern]) -> None:
        """@public
        Adds a list of patterns object to this item.

        >>> gains = Multiply("4m", 1)
        >>> adds = Multiply("2d", 1)
        >>> savings = Item(start_value=100)
        >>> savings.add_patterns([gains, adds])
        """
        try:
            for pattern in patterns:
                self.add_pattern(pattern)
        except TypeError:
            raise Exception("parameter is not list, use add_pattern instead.")

    def run(self, start: datetime | str, end: datetime | str) -> list:
        """@public
        Runs the provided patterns between the start and end date. Creates a result
        object with all the iterations per day/month/etc.

        >>> savings = Item(start_value=100)
        >>> savings.add_patterns([gains, adds])
        >>> savings.run("2024-1-1", "2025-1-1")
        """
        if not self.patterns:
            raise Exception("No patterns have been added.")
        start = keep_or_convert(start)
        end = keep_or_convert(end)
        [pattern.setup(start, end) for pattern in self.patterns]
        self.value = self.start_value
        result = Result()

        while start <= end:
            for pattern in self.patterns:
                if pattern.scheduled(start):
                    pattern.apply(self)
            result.add_result(start, self.value)
            start += self.granularity.timedelta
        return result

    def until(
        self,
        stop_value: float,
        start: datetime = datetime.today(),
        max_iterations: int = 1000,
    ) -> timedelta:
        """@public
        Runs the provided patterns until a stop value is reached. Returns the timedelta
        needed to reach the stop value. NOTE: Don't use offset with a start date here.

        >>> savings = Item(start_value=100)
        >>> savings.add_patterns([gains, adds])
        >>> savings.until(200)  # returns timedelta
        """
        end = start + self.granularity.timedelta
        self.value = self.start_value
        delta = timedelta()
        iterations = 0
        if not self.patterns:
            raise Exception("No patterns have been added.")
        while self.value <= stop_value:
            [pattern.setup(start, end, iterative=True) for pattern in self.patterns]
            for pattern in self.patterns:
                if pattern.scheduled(end):
                    pattern.apply(self)
            end += self.granularity.timedelta
            delta += self.granularity.timedelta
            iterations += 1
            if iterations > max_iterations:
                raise Exception("Max iterations (" + str(max_iterations) + ") reached.")
        return delta
