from datetime import datetime, timedelta
from typing import Any

from pylan.granularity import Granularity
from pylan.projections import Projection
from pylan.result import Result
from pylan.schedule import keep_or_convert


class ItemIterator:
    def __init__(
        self, item: Any, start: datetime, end: datetime, granularity: Granularity
    ) -> None:
        """@private
        Iterator class for the item object. See the docstring of Item.iterate() for more
        information.
        """
        self.item = item
        self.start = start
        self.current = start
        self.end = end
        self.granularity = granularity
        [projection.setup(start, end) for projection in item.projections]

    def __iter__(self) -> Any:
        """@private
        Iter function, gets called in for loops.
        """
        return self

    def __next__(self) -> Any:
        """@private
        Every iteration, the current time is increased and projections are applied.
        """
        if self.current > self.end:
            raise StopIteration
        for projection in self.item.projections:
            if projection.scheduled(self.current):
                projection.apply(self.item)
        self.current += self.granularity.timedelta
        return self.current, self.item


class Item:
    """@public
    An item that you can apply projections to and simulate over time. Optionally, you can
    set a start value.

    >>> savings = Item(start_value=100)
    """

    def __init__(self, start_value: int = 0) -> None:
        self.projections = []
        self.iterations = 0
        self.value = start_value if start_value else 0
        self.start_value = start_value if start_value else 0
        self.granularity = None

    def add_projection(self, projection: Projection) -> None:
        """@public
        Add a projection object to this item.

        >>> test = Add(["2024-1-4", "2024-2-1"], 1)
        >>> savings = Item(start_value=100)
        >>> savings.add_projection(test)
        """
        projection_granularity = Granularity.from_str(projection.schedule)
        if not self.granularity:
            self.granularity = projection_granularity
        elif projection_granularity < self.granularity:
            self.granularity = projection_granularity
        self.projections.append(projection)

    def add_projections(self, projections: list[Projection]) -> None:
        """@public
        Adds a list of projections object to this item.

        >>> gains = Multiply("4m", 1)
        >>> adds = Multiply("2d", 1)
        >>> savings = Item(start_value=100)
        >>> savings.add_projections([gains, adds])
        """
        try:
            for projection in projections:
                self.add_projection(projection)
        except TypeError:
            raise Exception("parameter is not list, use add_projection instead.")

    def run(
        self, start: datetime | str, end: datetime | str, granularity: Granularity = None
    ) -> list:
        """@public
        Runs the provided projections between the start and end date. Creates a result
        object with all the iterations per day/month/etc.

        >>> savings = Item(start_value=100)
        >>> savings.add_projections([gains, adds])
        >>> savings.run("2024-1-1", "2025-1-1")
        """
        if not granularity:
            granularity = self.granularity
        if not self.projections:
            raise Exception("No projections have been added.")
        start = keep_or_convert(start)
        end = keep_or_convert(end)
        [projection.setup(start, end) for projection in self.projections]
        self.value = self.start_value
        result = Result()

        current = start
        while current <= end:
            for projection in self.projections:
                if projection.scheduled(current):
                    projection.apply(self)
            result.add_result(current, self.value)
            current += granularity.timedelta
        return result

    def until(
        self,
        stop_value: float,
        start: datetime = datetime.today(),
        max_iterations: int = 1000,
    ) -> timedelta:
        """@public
        Runs the provided projections until a stop value is reached. Returns the timedelta
        needed to reach the stop value. NOTE: Don't use offset with a start date here.

        >>> savings = Item(start_value=100)
        >>> savings.add_projections([gains, adds])
        >>> savings.until(200)  # returns timedelta
        """
        current = start + self.granularity.timedelta
        self.value = self.start_value
        delta = timedelta()
        iterations = 0
        if not self.projections:
            raise Exception("No projections have been added.")

        while self.value <= stop_value:
            [projection.setup(start, current, iterative=True) for projection in self.projections]
            for projection in self.projections:
                if projection.scheduled(current):
                    projection.apply(self)
            current += self.granularity.timedelta
            delta += self.granularity.timedelta
            iterations += 1
            if iterations > max_iterations:
                raise Exception("Max iterations (" + str(max_iterations) + ") reached.")
        return delta

    def iterate(
        self, start: datetime | str, end: datetime | str, granularity: Granularity
    ) -> ItemIterator:
        """@public
        Creates Iterator object for the item. Can be used in a for loop. Returns a tuple
        of datetime and item object.

        >>> for date, saved in savings.iterate("2024-1-1", "2025-2-2", Granularity.day):
        >>>     print(date, saved.value)
        """
        start = keep_or_convert(start)
        end = keep_or_convert(end)
        return ItemIterator(self, start, end, granularity)
