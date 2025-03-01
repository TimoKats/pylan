from abc import ABC, abstractmethod
from datetime import datetime

from pylan.schedule import keep_or_convert, timedelta_from_schedule, timedelta_from_str


class Pattern(ABC):
    @abstractmethod
    def apply(self) -> None:
        """@public
        Applies the pattern to the item provided as a parameter. Implemented in the
        specific classes.
        """
        pass

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
