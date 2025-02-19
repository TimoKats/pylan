# import matplotlib.pyplot as plt
from datetime import datetime

from pylan import Item, Operators, Pattern

if __name__ == "__main__":
    inflation = Pattern("monthly", Operators.multiply, 0.92)
    investment_gains = Pattern("10d", Operators.multiply, 1.08)
    investment_adds = Pattern("15d", Operators.add, 200)

    test = Pattern("10d", Operators.add, 1.05)

    savings = Item("Savings", 100)

    savings.add_pattern(inflation)
    savings.add_pattern(investment_gains)
    savings.add_pattern(investment_adds)
    savings.add_pattern(test)

    result = savings.run(datetime(2024, 5, 1), datetime(2024, 7, 1))
    print(">>>", result.final)

    test = savings.until(1000)

    print(">>>>>>> ", test, result.final)

    # x, y = result.plot_axes()

    # plt.plot(x, y)
    # plt.show()
