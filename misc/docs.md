

Pylan is a Python library that simulates the impact of scheduled events over time. To get started, you can install the Python library using PyPi with the following command:

```
pip install pylan-lib
```

This code snippet shows some basic functionality when doing simulations.

```python
import matplotlib.pyplot as plt

from pylan import AddGrow, Item, Subtract

savings = Item(start_value=100)
dividends = AddGrow("90d", 100, "1y", 1.1) # the dividend will grow with 10% each year
growing_salary = AddGrow("1m", 2500, "1y", 1.2, offset_start="24d") # every month 24th
mortgage = Subtract("0 0 2 * *", 1500)  # cron support

savings.add_patterns([growing_salary, dividends, mortgage])
result = savings.run("2024-1-1", "2028-1-1")

x, y = result.plot_axes()

plt.plot(x, y)
plt.show()
```

There are 2 important classes in this library: Item and Pattern. A pattern is an abstract base class, with multiple implementations. These implementations resemble a time based pattern (e.g. add 10 every month, yearly inflation, etc). Finally, the Item is something that patterns can be added to, like a savings account.

---


## Class: Item

An item that you can apply patterns to and simulate over time. Optionally, you can
set a start value.

```python
>>> savings = Item(start_value=100)
```

#### Item.add_pattern(self, pattern: Pattern) -> None:


Add a pattern object to this item.

```python
>>> test = Add(["2024-1-4", "2024-2-1"], 1)
>>> savings = Item(start_value=100)
>>> savings.add_pattern(test)
```

#### Item.add_patterns(self, patterns: list[Pattern]) -> None:


Adds a list of patterns object to this item.

```python
>>> gains = Multiply("4m", 1)
>>> adds = Multiply("2d", 1)
>>> savings = Item(start_value=100)
>>> savings.add_patterns([gains, adds])
```

#### Item.run(self, start: datetime | str, end: datetime | str) -> list:


Runs the provided patterns between the start and end date. Creates a result
object with all the iterations per day/month/etc.

```python
>>> savings = Item(start_value=100)
>>> savings.add_patterns([gains, adds])
>>> savings.run("2024-1-1", "2025-1-1")
```

#### Item.until(self, stop_value: float) -> timedelta:


Runs the provided patterns until a stop value is reached. Returns the timedelta
needed to reach the stop value. NOTE: Don't use offset with a start date here.

```python
>>> savings = Item(start_value=100)
>>> savings.add_patterns([gains, adds])
>>> savings.until(200)  # returns timedelta
```

## Class: Result

Outputted by an item run. Result of a simulation between start and end date. Has the
schedule and values as attributes (which are both lists).

```python
>>> result = savings.run("2024-1-1", "2024-3-1")
>>> x, y = result.plot_axes() # can be used for matplotlib
>>> result.final # last value
>>> result.to_csv("test.csv")
```

#### Result.final(self):


Returns the result on the last day of the simulation.

```python
>>> result = savings.run("2024-1-1", "2024-3-1")
>>> result.final
```

#### Result.plot_axes(self, categorical_x_axis: bool = False) -> tuple[list, list]:


Returns x, y axes of the simulated run. X axis are dates and Y axis are values.

```python
>>> result = savings.run("2024-1-1", "2024-3-1")
>>> x, y = result.plot_axes() # can be used for matplotlib
```

#### Result.to_csv(self, filename: str, sep: str = ";") -> None:


Exports the result to a csv file. Row oriented.

```python
>>> result = savings.run("2024-1-1", "2024-3-1")
>>> result.to_csv("test.csv")
```

## Class: Pattern


Pattern is an abstract base class with the following implementations:
    - Add(schedule, value to add)
    - Subtract(schedule, value to subtract)
    - Multiply(schedule, value to multiply with)
    - Divide(schedule, value to divide by)
    - AddGrow(schedule for addition, addition value, schedule for multiplication, multiply value)
        - AddGrow adds a value that can be increased over time based on another schedule.

Note, all implementations have the following optional parameters: __start_date__ (str
or datetime with the minimum date for the pattern to start), __end_date__ (str or
datetime, max date for the pattern), __offset_start__ (str, offsets each occurence of
the pattern based on the start date).

```python
>>> dividends = AddGrow("90d", 100, "1y", 1.1)
>>> growing_salary = AddGrow("1m", 2500, "1y", 1.2, offset_start="24d")
>>> mortgage = Subtract("0 0 2 * *", 1500)  # cron support
>>> inflation = Divide(["2025-1-1", "2026-1-1", "2027-1-1"], 1.08)
```

#### Pattern.apply(self) -> None:


Applies the pattern to the item provided as a parameter. Implemented in the
specific classes.

#### Pattern.scheduled(self, current: datetime) -> bool:


Returns true if pattern is scheduled on the provided date.

