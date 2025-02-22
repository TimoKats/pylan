from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Result:
    """
    Outputted by an item run. Result of a simulation between start and end date.

    >>> result = savings.run("2024-1-1", "2024-3-1")
    >>> x, y = result.plot_axes() # can be used for matplotlib
    >>> result.final # last value
    >>> result.to_csv("test.csv")
    """

    schedule: Optional[list[datetime]] = field(default_factory=list)
    values: Optional[list[float]] = field(default_factory=list)

    def __str__(self) -> str:
        str_result = ""
        for date, value in zip(self.schedule, self.values):
            str_result += str(date) + "   " + str(value) + "\n"
        return str_result

    @property
    def final(self):
        """Returns the result on the last day of the simulation."""
        return self.values[-1:][0]

    def plot_axes(self, categorical_x_axis: bool = False) -> tuple[list, list]:
        """Returns x, y axes of the simulated run. X axis are dates and Y axis are values."""
        if categorical_x_axis:
            return [str(date) for date in self.schedule], self.values
        return self.schedule, self.values

    def add_result(self, date: datetime, value: float) -> None:
        """@private test test"""
        self.schedule.append(date)
        self.values.append(value)

    def to_csv(self, filename: str, sep: str = ";") -> None:
        """Exports the result to a csv file. Row oriented."""
        f = open(filename, "w")
        for date, value in zip(self.schedule, self.values):
            f.write(str(date) + sep + str(value) + "\n")
