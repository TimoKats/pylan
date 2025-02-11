from dataclasses import dataclass
from typing import Any

@dataclass
class Pattern:
	name: str
	schedule: str
	attribute: str
	impact: Any

	def apply(self, item: Any) -> None:  # fix typing
		item.attr[self.attribute] += self.impact  # this will depend on data type etc.
