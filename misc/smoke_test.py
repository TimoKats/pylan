from pylan import AddGrow, Divide, Item, Subtract

savings = Item(start_value=100)
dividends = AddGrow("90d", 100, "1y", 1.1)
growing_salary = AddGrow("1m", 2500, "1y", 1.2, offset="24d")
mortgage = Subtract("0 0 2 * *", 1500)  # cron support
inflation = Divide(["2025-1-1", "2026-1-1", "2027-1-1"], 1.08)

savings.add_patterns([growing_salary, dividends, mortgage])
result = savings.run("2024-1-1", "2027-1-1")

x, y = result.plot_axes()

print(result["2024-5-5"])
