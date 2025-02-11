from typing import Optional

from agropy.crop import Crop

class Field:

	def __init__(
		self,
		n_rows: int,
		n_cols: int,
		row_spacing: Optional[float] = 2,
		crop_spacing: Optional[float] = 1,
	) -> None:
		self.field = [[ Crop() for _ in range(0, n_cols) ] for _ in range(0, n_rows)]
		self.n_rows = n_rows
		self.n_cols = n_cols
		self.planting_pattern = "square"  # make enum for this
		self.unit = "m"  # make enum for this
		return


	def __str__(self):
		field_str = ""
		for rows in self.field:
			for crop in rows:
				field_str += str(crop) + " "
			field_str += "\n"
		return field_str


	def plant(self, row: int, col: int, crop: Crop) -> None:
		if row > self.n_rows or col > self.n_cols:
			raise Exception("Location exceeds field range.")
		self.field[row][col] = crop

