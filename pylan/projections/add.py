from pylan.item import Item
from pylan.projections import Projection


class Add(Projection):
    def apply(self, item: Item | Projection) -> None:
        """@private
        Adds the projection value to the item (or projection) value.
        """
        item.value += self.value
