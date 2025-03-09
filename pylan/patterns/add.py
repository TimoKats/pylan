from pylan.item import Item
from pylan.patterns import Pattern


class Add(Pattern):
    def apply(self, item: Item | Pattern) -> None:
        """@private
        Adds the pattern value to the item (or pattern) value.
        """
        item.value += self.value
