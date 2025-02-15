from datetime import datetime

from pylan import Item, Operators, Pattern

if __name__ == "__main__":
    inflation = Pattern("1w", "value", Operators.multiply, 0.92)
    investment_gains = Pattern("7d", "value", Operators.multiply, 1.08)
    investment_adds = Pattern("1d", "value", Operators.add, 200)

    savings = Item("Savings", {"value": 100})

    # savings.add_pattern(inflation)
    savings.add_pattern(investment_gains)
    # savings.add_pattern(investment_adds)

    savings.run(datetime.today(), datetime(2025, 2, 23), "1d")

    print(investment_gains.dt_schedule)
    print(savings.attr)
