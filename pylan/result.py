from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from pylan.schedule import keep_or_convert


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
        """@public
        String format of result is a column oriented table with dates and values.
        """
        str_result = ""
        for date, value in zip(self.schedule, self.values):
            str_result += str(date) + "\t" + str(value) + "\n"
        return str_result

    def __repr__(self) -> str:
        """@public
        String format of result is a column oriented table with dates and values.
        """
        str_result = ""
        seperator = False
        for index, (date, value) in enumerate(zip(self.schedule, self.values)):
            if index < 5 or index > len(self.values) - 6:
                str_result += str(date) + "\t" + str(value) + "\n"
            elif not seperator:
                str_result += "...\n"
                seperator = True
        return str_result

    def __getitem__(self, key: str | datetime) -> float | int:
        """@public
        Get a result by the date using a dict key.

        >>> print(result["2024-5-5"])
        """
        key = keep_or_convert(key)
        for date, value in zip(self.schedule, self.values):
            if date == key:
                return value
        raise Exception("Date not found in result.")

    @property
    def final(self):
        """@public
        Returns the result on the last day of the simulation.

        >>> result = savings.run("2024-1-1", "2024-3-1")
        >>> result.final
        """
        return self.values[-1:][0]

    @property
    def valid(self):
        """@public
        Returns true if the result has a valid format
        """
        return len(self.schedule) == len(self.values)

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
