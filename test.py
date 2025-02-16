from datetime import datetime

from pylan import Item, Operators, Pattern

if __name__ == "__main__":
    inflation = Pattern("1d", Operators.multiply, 0.92)
    investment_gains = Pattern("10d", Operators.multiply, 1.08)
    investment_adds = Pattern("3d", Operators.add, 200)

    savings = Item("Savings", 100)

    savings.add_pattern(inflation)
    savings.add_pattern(investment_gains)
    savings.add_pattern(investment_adds)

    savings.run(datetime(2024, 5, 1), datetime(2024, 7, 1), "1d")
    print(savings.value)
