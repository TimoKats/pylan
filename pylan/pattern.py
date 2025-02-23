from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from pylan.enums import Operators
from pylan.schedule import keep_or_convert, timedelta_from_schedule, timedelta_from_str


@dataclass
class Pattern:
    """
    Class for defining the patterns used in simulation. Can be applied to an item. Allows
    the following parameters: schedule, operator, impact (all mandetory), start_date
    offset_start, end_date, offset_end (all optional).

    >>> Pattern("2d", Operators.add, 10) # adds 10 every day
    >>> Pattern(["2d", "3d"], Operators.multiply, 1.06) # irregular patterns through lists
    >>> Pattern("0 0 2 * *", Operators.add, 10, start_date="2025-1-1") # cron schedule, hardcoded min date
    >>> Pattern("2d", Operators.add, 10, offset_start="10d") # starts pattern 10 days later.
    """

    schedule: Any
    operator: Operators
    impact: Any

    start_date: Optional[datetime | str] = None
    end_date: Optional[datetime | str] = None
    offset_start: Optional[str] = None
    offset_end: Optional[str] = None
    iterations: Optional[int] = 0
    dt_schedule: Optional[list] = None

    def set_dt_schedule(self, start: datetime, end: datetime) -> None:
        """@private
        Iterates between start and end date and returns sets the list of datetimes that
        the pattern is scheduled.
        """
        start = self._apply_start_date_settings(start)
        end = self._apply_end_date_settings(end)
        self.dt_schedule = timedelta_from_schedule(self.schedule, start, end)

    def _apply_start_date_settings(self, date: datetime) -> datetime:
        """@private
        Checks if the optional start date variables are set and returns updated value.
        """
        if self.start_date and keep_or_convert(self.start_date) > date:
            date = keep_or_convert(self.start_date)
        elif self.offset_start:
            date += timedelta_from_str(self.offset_start)
        return date

    def _apply_end_date_settings(self, date: datetime) -> datetime:
        """@private
        Checks if the optional end date variables are set and returns updated value.
        """
        if self.end_date and keep_or_convert(self.end_date) < date:
            date = keep_or_convert(self.end_date)
        elif self.offset_end:
            date -= timedelta_from_str(self.offset_end)
        return date

    def apply(self, item: Any) -> None:
        """@public
        Applies the pattern to the item provided as a parameter.
        """
        current_value = item.value
        item.value = self.operator.apply(current_value, self.impact)

    def scheduled(self, current: datetime) -> bool:
        """@public
        Returns true if pattern is scheduled on the provided date.
        """
        if not self.dt_schedule:
            raise Exception("Datetime schedule not set.")
        if self.iterations >= len(self.dt_schedule):
            return False
        if current == self.dt_schedule[self.iterations]:
            self.iterations += 1
            return True
        return False
