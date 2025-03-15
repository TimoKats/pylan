from pylan.item import Item
from pylan.patterns import Pattern


class Replace(Pattern):
    def apply(self, item: Item) -> None:
        """@private
        Replaces the pattern value with the item value.
        """
        item.value = self.value
