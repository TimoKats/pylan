from agropy import Collection, Item, Pattern


if __name__ == "__main__":

	inflation = Pattern("inflation", "x", "value", 0.9)
	savings = Item("Savings", {"value": 100})
	savings.add_pattern(inflation)

	savings.iterate()

	print(savings.attr)
