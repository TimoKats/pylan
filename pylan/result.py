from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Result:
    schedule: Optional[list[datetime]] = field(default_factory=list)
    values: Optional[list[float]] = field(default_factory=list)

    def __str__(self) -> str:
        str_result = ""
        for date, value in zip(self.schedule, self.values):
            str_result += str(date) + "   " + str(value) + "\n"
        return str_result

    @property
    def final(self):
        return self.values[-1:][0]

    def plot_axes(self, categorical_x_axis: bool = False) -> tuple[list, list]:
        if categorical_x_axis:
            return [str(date) for date in self.schedule], self.values
        return self.schedule, self.values

    def add_result(self, date: datetime, value: float) -> None:
        self.schedule.append(date)
        self.values.append(value)

    def to_csv(self, filename: str, sep: str = ";") -> None:
        f = open(filename, "w")
        for date, value in zip(self.schedule, self.values):
            f.write(str(date) + sep + str(value) + "\n")
