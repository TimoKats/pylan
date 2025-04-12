from pylan.item import Item
from pylan.projections import Projection


class Subtract(Projection):
    def apply(self, item: Item) -> None:
        """@private
        Adds the projection value to the item value.
        """
        item.value -= self.value
