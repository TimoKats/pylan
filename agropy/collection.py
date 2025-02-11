from agropy.item import Item
from agropy.pattern import Pattern

from datetime import datetime

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

