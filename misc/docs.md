

Pylan is a Python library that simulates the impact of scheduled events. You can install the Python library using PyPi with the following command:

```
pip install pylan-lib
```

This code snippet shows some basic functionality when doing simulations.

```python
from pylan import Item, Subtract, Add, Multiply

savings = Item(start_value=100)
salary_payments = Add("1m", 2500, offset="24d") # Salary paid every month at the 24th
salary_increase = Multiply("1y", 1.2) # Salary grows each year 20%
mortgage = Subtract("0 0 2 * *", 1500)  # cron support

salary_payments.add_projection(salary_increase) # Add increase to salary projection
savings.add_projections([salary_payments, mortgage])
result = savings.run("2024-1-1", "2028-1-1")

x, y = result.plot_axes()

plt.plot(x, y)
plt.show()

```

There are 2 important classes in this library: Item and Projection. A projection is an abstract base class, with multiple implementations. These implementations resemble a time based projection (e.g. add 10 every month, yearly inflation, etc). The Item is something that projections can be added to, like a savings account.



---
## Class: Granularity


Refers to the minimum step size needed for iterations given a set of projections. Can be
tweaked for Item.run(). Note that the default value here is the minimum granularity
of the added projections. Supports: hour, day, week, month, year

```python
>>> from pylan import Granularity
>>> savings.run("2024-1-1", "2028-1-1", Granularity.day)
>>> savings.run("2024-1-1", "2028-1-1", Granularity.month)
```


---
## Class: Item


An item that you can apply projections to and simulate over time. Optionally, you can
set a start value.

```python
>>> savings = Item(start_value=100)
```

#### Item.add_projection(self, projection: Projection) -> None:


Add a projection object to this item.

```python
>>> test = Add(["2024-1-4", "2024-2-1"], 1)
>>> savings = Item(start_value=100)
>>> savings.add_projection(test)
```

#### Item.add_projections(self, projections: list[Projection]) -> None:


Adds a list of projections object to this item.

```python
>>> gains = Multiply("4m", 1)
>>> adds = Multiply("2d", 1)
>>> savings = Item(start_value=100)
>>> savings.add_projections([gains, adds])
```

#### Item.run(


Runs the provided projections between the start and end date. Creates a result
object with all the iterations per day/month/etc.

```python
>>> savings = Item(start_value=100)
>>> savings.add_projections([gains, adds])
>>> savings.run("2024-1-1", "2025-1-1")
```

#### Item.until(


Runs the provided projections until a stop value is reached. Returns the timedelta
needed to reach the stop value. NOTE: Don't use offset with a start date here.

```python
>>> savings = Item(start_value=100)
>>> savings.add_projections([gains, adds])
>>> savings.until(200)  # returns timedelta
```

#### Item.iterate(


Creates Iterator object for the item. Can be used in a for loop. Returns a tuple
of datetime and item object.

```python
>>> for date, saved in savings.iterate("2024-1-1", "2025-2-2", Granularity.day):
>>>     print(date, saved.value)
```


---
## Class: Result


Outputted by an item run. Result of a simulation between start and end date. Has the
schedule and values as attributes (which are both lists).

```python
>>> result = savings.run("2024-1-1", "2024-3-1")
>>> x, y = result.plot_axes() # can be used for matplotlib
>>> result.final # last value
>>> result.to_csv("test.csv")
```

#### Result.__str__(self) -> str:


String format of result is a column oriented table with dates and values.

#### Result.__repr__(self) -> str:


String format of result is a column oriented table with dates and values.

#### Result.__getitem__(self, key: str | datetime) -> float | int:


Get a result by the date using a dict key.

```python
>>> print(result["2024-5-5"])
```

#### Result.final(self):


Returns the result on the last day of the simulation.

```python
>>> result = savings.run("2024-1-1", "2024-3-1")
>>> result.final
```

#### Result.valid(self):


Returns true if the result has a valid format

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


---
## Class: Projection


Projection is an abstract base class with the following implementations:
- Add(schedule, value)
- Subtract(schedule, value)
- Multiply(schedule, value)
- Divide(schedule, value)
- Replace(schedule, value)

Note, all implementations have the following optional parameters:
- start_date: str or datetime with the minimum date for the projection to start
- end_date: str or datetime, max date for the projection
- offset: str, offsets each occurence of the projection based on the start date

```python
>>> mortgage = Subtract("0 0 2 * *", 1500)  # cron support
>>> inflation = Divide(["2025-1-1", "2026-1-1", "2027-1-1"], 1.08)
```

#### Projection.apply(self) -> None:


Applies the projection to the item provided as a parameter. Implemented in the
specific classes.

#### Projection.add_projection(self, projection: Any) -> None:


Applies the projection to the value of this projection. E.g. You add a salary each month,
over time this salary can grow using another projection.

#### Projection.scheduled(self, current: datetime) -> bool:


Returns true if projection is scheduled on the provided date.


---

## Schedule

Passed to projections as a parameter. Is converted to a list of datetime objects. Accepts multiple formats.

#### Cron schedules
For example, "0 0 2 * *" runs on the second day of each month.

#### Timedelta strings
Combination of a count and timedelta. For example, 2d (every 2 days) 3m (every 3 months). Currently supports: years (y), months (m), weeks (w), days (d).

#### Timedelta lists
Same as timedelta, but then alternates between the schedules. For example, ["2d", "5d"] will be triggered after 2 days, then after 5 days, then after 2 days, etc...

#### Datetime lists
A list of datetime objects or str that resemble datetime objects. For example, ["2024-1-1", "2025-1-1"].

**_NOTE:_**  The date format in pylan is yyyy-mm-dd. Currently this is not configurable.


