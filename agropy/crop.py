
class Crop:
	def __init__(self, name: str = ".", width: float = 1, length: float = 1) -> None:
		self.name = name
		return

	def __str__(self):
		if len(self.name) > 1:
			return self.name[:2]
		return self.name + " "