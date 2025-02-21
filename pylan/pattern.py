from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from pylan.enums import Operators
from pylan.utils import keep_or_convert, timedelta_from_schedule


@dataclass
class Pattern:
    schedule: str
    operator: Operators
    impact: Any

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    iterations: Optional[int] = 0
    dt_schedule: Optional[list] = None

    def set_dt_schedule(self, start: datetime, end: datetime) -> None:
        if self.start_date and keep_or_convert(self.start_date) > start:
            start = keep_or_convert(self.start_date)
        if self.end_date and keep_or_convert(self.end_date) < end:
            end = keep_or_convert(self.end_date)
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
