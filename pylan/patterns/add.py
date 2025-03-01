from datetime import datetime
from typing import Any

from pylan.item import Item
from pylan.patterns import Pattern


class Add(Pattern):
    def __init__(
        self,
        schedule: Any,
        value: float | int,
        start_date: str | datetime = None,
        offset_start: str = None,
        end_date: str | datetime = None,
        offset_end: str = None,
    ) -> None:
        self.schedule = schedule
        self.value = value
        self.iterations = 0
        self.dt_schedule = []

        self.start_date = start_date
        self.offset_start = offset_start
        self.end_date = end_date
        self.offset_end = offset_end

    def apply(self, item: Item) -> None:
        """@private
        Adds the pattern value to the item value.
        """
        item.value += self.value
