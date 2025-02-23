from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Result:
    """
    Outputted by an item run. Result of a simulation between start and end date. Has the
    schedule and values as attributes (which are both lists).

    >>> result = savings.run("2024-1-1", "2024-3-1")
    >>> x, y = result.plot_axes() # can be used for matplotlib
    >>> result.final # last value
    >>> result.to_csv("test.csv")
    """

    schedule: Optional[list[datetime]] = field(default_factory=list)
    values: Optional[list[float]] = field(default_factory=list)

    def __str__(self) -> str:
        """@private
        String format of result is a column oriented table with dates and values.
        """
        str_result = ""
        for date, value in zip(self.schedule, self.values):
            str_result += str(date) + "   " + str(value) + "\n"
        return str_result

    @property
    def final(self):
        """@public
        Returns the result on the last day of the simulation.

        >>> result = savings.run("2024-1-1", "2024-3-1")
        >>> result.final
        """
        return self.values[-1:][0]

    def plot_axes(self, categorical_x_axis: bool = False) -> tuple[list, list]:
        """@public
        Returns x, y axes of the simulated run. X axis are dates and Y axis are values.

        >>> result = savings.run("2024-1-1", "2024-3-1")
        >>> x, y = result.plot_axes() # can be used for matplotlib
        """
        if categorical_x_axis:
            return [str(date) for date in self.schedule], self.values
        return self.schedule, self.values

    def add_result(self, date: datetime, value: float) -> None:
        """@private

        Adds value/date to the result object.
        """
        self.schedule.append(date)
        self.values.append(value)

    def to_csv(self, filename: str, sep: str = ";") -> None:
        """@public
        Exports the result to a csv file. Row oriented.

        >>> result = savings.run("2024-1-1", "2024-3-1")
        >>> result.to_csv("test.csv")
        """
        f = open(filename, "w")
        for date, value in zip(self.schedule, self.values):
            f.write(str(date) + sep + str(value) + "\n")
