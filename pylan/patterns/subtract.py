from datetime import datetime
from typing import Any

from pylan.item import Item
from pylan.patterns import Pattern


class Subtract(Pattern):
    def __init__(
        self,
        schedule: Any,
        value: float | int,
        start_date: str | datetime = None,
        offset: str = None,
        end_date: str | datetime = None,
    ) -> None:
        self.schedule = schedule
        self.value = value
        self.iterations = 0
        self.dt_schedule = []

        self.start_date = start_date
        self.offset = offset
        self.end_date = end_date

    def apply(self, item: Item) -> None:
        """@private
        Adds the pattern value to the item value.
        """
        item.value -= self.value
