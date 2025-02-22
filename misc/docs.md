Pylan is a library for simulating numeric patterns over time series.
## Class: Pattern

Class for defining the patterns used in simulation. Can be applied to an item.

```python
>>> Pattern("2d", Operators.add, 10) # adds 10 every day
>>> Pattern("montly", Operators.multiply, 1.06) # 6% inflation every month
>>> Pattern("0 0 2 * *", Operators.add, 10, start_date="2025-1-1") # cron schedule, hardcoded min date
>>> Pattern("2d", Operators.add, 10, offset_start="10d") # starts pattern 10 days later.
```

## Class: Item

An item that you can apply patterns to and simulate over time.

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
>>> gains = Pattern("month", Operators.multiply, 1)
>>> adds = Pattern("2d", Operators.add, 1)
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

#### Item.iterate(self) -> None:

Runs the provided patterns once.

```python
>>> savings = Item(start_value=100)
>>> savings.add_patterns([gains, adds])
>>> savings.iterate()
```

## Class: Result

Outputted by an item run. Result of a simulation between start and end date.

```python
>>> result = savings.run("2024-1-1", "2024-3-1")
>>> x, y = result.plot_axes() # can be used for matplotlib
>>> result.final # last value
>>> result.to_csv("test.csv")
```

#### Result.final(self):

Returns the result on the last day of the simulation.

#### Result.plot_axes(self, categorical_x_axis: bool = False) -> tuple[list, list]:

Returns x, y axes of the simulated run. X axis are dates and Y axis are values.

#### Result.to_csv(self, filename: str, sep: str = ";") -> None:

Exports the result to a csv file. Row oriented.

## Class: Operators

Refers to the supported operations a pattern object can have.

```python
>>> Pattern("0 0 2 * *", Operators.add, 1)
>>> Pattern(["2d", "4d"], Operators.multiply, 0.1)
```

## Class: Granularity

Refers to the minimum step size needed for iterations given a set of patterns.

