from pylan import Item, Pattern, Operators
from datetime import datetime

if __name__ == "__main__":

	inflation = Pattern("2d", "value", Operators.add, 0.92)
	investment_gains = Pattern("3d", "value", Operators.multiply, 1.08)
	investment_adds = Pattern("7d", "value", Operators.add, 200)  # NOTE: create list of dates based on schedule, that's better!

	savings = Item("Savings", {"value": 100})

	savings.add_pattern(inflation)
	savings.add_pattern(investment_gains)
	savings.add_pattern(investment_adds)

	savings.run(datetime.today(), datetime(2025, 3, 2), "2d")

	print(savings.attr)
