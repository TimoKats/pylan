from datetime import datetime
from typing import Any

from pylan.item import Item
from pylan.patterns import Pattern
from pylan.schedule import timedelta_from_schedule


class AddGrow(Pattern):
    def __init__(
        self,
        add_schedule: Any,
        add_value: float | int,
        grow_schedule: Any,
        grow_value: float | int,
        start_date: str | datetime = None,
        offset_start: str = None,
        end_date: str | datetime = None,
        offset_end: str = None,
    ) -> None:
        # for additions
        self.schedule = add_schedule
        self.value = add_value
        self.iterations = 0
        self.dt_schedule = []

        # for growing the additions
        self.grow_schedule = grow_schedule
        self.grow_value = grow_value
        self.grow_dt_schedule = []
        self.grow_iterations = 0

        # basic stuff
        self.start_date = start_date
        self.offset_start = offset_start
        self.end_date = end_date
        self.offset_end = offset_end

    def set_dt_schedule(self, start: datetime, end: datetime) -> None:
        """@private
        Overrules base class by also adding the schedule for the growth component.
        """
        start = self._apply_start_date_settings(start)
        end = self._apply_end_date_settings(end)
        self.dt_schedule = timedelta_from_schedule(self.schedule, start, end)
        self.grow_dt_schedule = timedelta_from_schedule(self.grow_schedule, start, end)

    def apply(self, item: Item) -> None:
        """@private
        Adds the pattern value to the item value.
        """
        item.value += self.value

    def update_value(self, current: datetime) -> None:
        """@private
        Grows the value the amount of times that it was scheduled in the past.
        """
        try:
            while self.grow_dt_schedule[self.grow_iterations] < current:
                self.value *= self.grow_value
                self.grow_iterations += 1
        except IndexError:
            pass

    def scheduled(self, current: datetime) -> bool:
        """@private
        Overrules base class by also adding the schedule for the growth component.
        """
        self.update_value(current)
        if not self.dt_schedule:
            raise Exception("Datetime schedule not set.")
        if self.iterations >= len(self.dt_schedule):
            return False
        if current >= self.dt_schedule[self.iterations]:
            self.iterations += 1
            return True
        return False
