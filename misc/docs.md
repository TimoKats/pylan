

Pylan is a Python library that simulates the impact of scheduled events over time. To get started, you can install the Python library using PyPi with the following command:

```
pip install pylan-lib
```

This code snippet shows some basic functionality when doing simulations.

```python
savings = Item(start_value=100)

inflation = Pattern("6w", Operators.divide, 1.08)
salary_adds = Pattern("m", Operators.add, 2000, offset_start="15d")  # every m at the 15th
investment_gains = Pattern("m", Operators.multiply, 1.1)
mortgage = Pattern("0 0 2 * *", Operators.subtract, 1500)  # cron support

savings.add_patterns([salary_adds, inflation, investment_gains, mortgage])

result = savings.run("2024-1-1", "2025-1-1")
x, y = result.plot_axes()

plt.plot(x, y)
plt.show()
```

There are three important classes in this library: Item, Pattern and Operator. In summary, patterns refer to scheduled events that you want to simulate. The all have an operator (like add something, multiply by x, etc.) and you add these patterns to an item (e.g. savings, investments, etc). Below is the documentation of these classes.

---


## Class: Granularity

Refers to the minimum step size needed for iterations given a set of patterns.

## Class: Item

An item that you can apply patterns to and simulate over time. Optionally, you can
set a start value.

```python
>>> savings = Item(start_value=100)
```

#### Item.add_pattern(self, pattern: Pattern) -> None:


Add a pattern object to this item.

```python
>>> test = Pattern(["2024-1-4", "2024-2-1"], Operators.add, 1)
>>> savings = Item(start_value=100)
>>> savings.add_pattern(test)
```

#### Item.add_patterns(self, patterns: list[Pattern]) -> None:


Adds a list of patterns object to this item.

```python
>>> gains = Pattern("m", Operators.multiply, 1)
>>> adds = Pattern("2d", Operators.add, 1)
>>> savings = Item(start_value=100)
>>> savings.add_patterns([gains, adds])
```

#### Item.run(self, start: datetime | str, end: datetime | str) -> list:


Runs the provided patterns between the start and end date. Creates a result
object with all the iterations per day/m/etc.

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

#### Pattern.apply(self) -> None:


Applies the pattern to the item provided as a parameter. Implemented in the
specific classes.

#### Pattern.scheduled(self, current: datetime) -> bool:


Returns true if pattern is scheduled on the provided date.

