# start working with set enums or types to pick granularity from.


from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from pylan.utils import timedelta_from_str
from pylan.enums import Ops, Granularity

@dataclass
class Pattern:
	schedule: str
	attribute: str
	operator: str
	impact: Any
	iterations: int = 1  # perhaps keep track of the dates?

	def apply(self, item: Any) -> None:  # fix typing
		if self.operator == "+":
			item.attr[self.attribute] += self.impact
		elif self.operator == "*":
			item.attr[self.attribute] *= self.impact
		else:
			raise Exception("Operator not supported.")

	def scheduled(self, passed_time: timedelta) -> bool:
		dt_schedule = timedelta_from_str(self.schedule)
		if passed_time >= (dt_schedule * self.iterations):
			self.iterations += 1
			return True
		return False


class Item:
	def __init__(self, name: str = ".", attr: dict = {}) -> None:
		self.name = name
		self.start_dt = datetime.today()
		self.patterns = []
		self.iterations = 0
		self.attr = attr

	def __str__(self) -> str:
		if len(self.name) > 1:
			return self.name[:2]
		return self.name

	def add_attribute(self, name: str, value: Any) -> None:
		self.attr[name] = value

	def add_pattern(self, pattern: Pattern) -> None:
		self.patterns.append(pattern)

	def run(self, start: datetime, end: datetime, interval: str) -> list:
		dt_interval = timedelta_from_str(interval)
		current = start
		while current <= end:
			for pattern in self.patterns:
				if pattern.scheduled((current - start)):
					pattern.apply(self)
				current += dt_interval
		return []

	def iterate(self):
		self.iterations += 1
		for pattern in self.patterns:
			pattern.apply(self)


class Collection:
	def __init__(self, n: int) -> None:
		self.items = [ Item() for _ in range(0, n) ]
		self.start_dt = datetime.now()
		self.n = n

	def __str__(self) -> str:
		collection_str = ""
		for item in self.items:
			collection_str += str(item) + " "
		return collection_str

	def update(self, loc: int, item: Item) -> None:
		if loc > self.n:
			raise Exception("Location exceeds collection range.")
		self.items[loc] = item

	def add_pattern(self, pattern: Pattern) -> None:
		return

