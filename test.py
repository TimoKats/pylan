from agropy import Field, Crop


if __name__ == "__main__":
	potato = Crop("Potato", 1, 2)
	pumpkin = Crop("Pumkin", 4, 2)

	field = Field(10, 10)
	field.plant(0, 1, potato)
	field.plant(2, 3, pumpkin)

	print(field)
