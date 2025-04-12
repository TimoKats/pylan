from pylan.item import Item
from pylan.projections import Projection


class Multiply(Projection):
    def apply(self, item: Item) -> None:
        """@private
        Adds the projection value to the item value.
        """
        item.value *= self.value
