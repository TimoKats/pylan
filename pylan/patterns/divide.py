from pylan.item import Item
from pylan.patterns import Pattern


class Divide(Pattern):
    def apply(self, item: Item) -> None:
        """@private
        Adds the pattern value to the item value.
        """
        item.value /= self.value
