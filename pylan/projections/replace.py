from pylan.item import Item
from pylan.projections import Projection


class Replace(Projection):
    def apply(self, item: Item) -> None:
        """@private
        Replaces the projection value with the item value.
        """
        item.value = self.value
