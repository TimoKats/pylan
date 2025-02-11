from typing import Any

from agropy.pattern import Pattern

class Item:
	def __init__(self, name: str = ".", attr: dict = {}) -> None:
		self.name = name
		self.patterns = {}
		self.iterations = 0
		self.attr = attr

	def __str__(self) -> str:
		if len(self.name) > 1:
			return self.name[:2]
		return self.name

	def add_attribute(self, name: str, value: Any) -> None:
		self.attr[name] = value

	def add_pattern(self, pattern: Pattern) -> None:
		self.patterns[pattern.name] = pattern

	def iterate(self):
		self.iterations += 1
		for pattern in self.patterns.values():
			pattern.apply(self)


