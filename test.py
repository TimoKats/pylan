from pylan import Item, Pattern
from datetime import datetime

if __name__ == "__main__":

	inflation = Pattern("2d", "value", "*", 0.92)
	investment_gains = Pattern("3d", "value", "*", 1.08)
	investment_adds = Pattern("7d", "value", "+", 200)

	savings = Item("Savings", {"value": 100})

	# savings.add_pattern(inflation)
	# savings.add_pattern(investment_gains)
	savings.add_pattern(investment_adds)

	savings.run(datetime.today(), datetime(2025, 3, 2), "1d")

	print(savings.attr)
