from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pylan.schedule import keep_or_convert, timedelta_from_schedule, timedelta_from_str


class Pattern(ABC):
    """@public
    Pattern is an abstract base class with the following implementations:
    - Add(schedule, value)
    - Subtract(schedule, value)
    - Multiply(schedule, value)
    - Divide(schedule, value)

    Note, all implementations have the following optional parameters:
    - __start_date__: str or datetime with the minimum date for the pattern to start
    - __end_date__: str or datetime, max date for the pattern
    - __offset__: str, offsets each occurence of the pattern based on the start date

    >>> mortgage = Subtract("0 0 2 * *", 1500)  # cron support
    >>> inflation = Divide(["2025-1-1", "2026-1-1", "2027-1-1"], 1.08)
    """

    @abstractmethod
    def apply(self) -> None:
        """@public
        Applies the pattern to the item provided as a parameter. Implemented in the
        specific classes.
        """
        pass

    def add_pattern(self, pattern: Any) -> None:
        """@public
        Applies the pattern to the value of this pattern. E.g. You add a salary each month,
        over time this salary can grow using another pattern.
        """
        self.patterns.append(pattern)

    def update_value(self, current: datetime) -> None:
        """@private
        Grows the value the amount of times that it was scheduled in the past.
        """
        for pattern in self.patterns:
            try:
                while pattern.dt_schedule[pattern.iterations] < current:
                    pattern.apply(self)
                    pattern.iterations += 1
            except IndexError:
                pass

    def set_dt_schedule(self, start: datetime, end: datetime) -> None:
        """@private
        Iterates between start and end date and returns sets the list of datetimes that
        the pattern is scheduled.
        """
        self.iterations = 0
        start = self._apply_start_date_settings(start)
        end = self._apply_end_date_settings(end)
        self.dt_schedule = timedelta_from_schedule(self.schedule, start, end)
        [pattern.set_dt_schedule(start, end) for pattern in self.patterns]

    def _apply_start_date_settings(self, date: datetime) -> datetime:
        """@private
        Checks if the optional start date variables are set and returns updated value.
        """
        if self.start_date and keep_or_convert(self.start_date) > date:
            date = keep_or_convert(self.start_date)
        elif self.offset:
            date += timedelta_from_str(self.offset)
        return date

    def _apply_end_date_settings(self, date: datetime) -> datetime:
        """@private
        Checks if the optional end date variables are set and returns updated value.
        """
        if self.end_date and keep_or_convert(self.end_date) < date:
            date = keep_or_convert(self.end_date)
        return date

    def scheduled(self, current: datetime) -> bool:
        """@public
        Returns true if pattern is scheduled on the provided date.
        """
        if self.patterns:
            self.update_value(current)
        if not self.dt_schedule:
            raise Exception("Datetime schedule not set.")
        if self.iterations >= len(self.dt_schedule):
            return False
        if current >= self.dt_schedule[self.iterations]:
            self.iterations += 1
            return True
        return False
