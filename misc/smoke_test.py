from pylan import Add, Granularity, Item, Multiply, Result, Subtract

savings = Item(start_value=10)
salary_payments = Add("1m", 2500, offset="24d")
salary_increase = Multiply("1y", 1.2)
mortgage = Subtract("0 0 2 * *", 1500)  # cron support
salary_payments.add_projection(salary_increase)
savings.add_projections([salary_payments])

result = Result()
car_bought = False
buy_car = Subtract("", 5000)

for date, saved in savings.iterate("2024-1-1", "2025-1-1", Granularity.day):
    if saved.value > 5000 and not car_bought:
        buy_car.apply(savings)
        car_bought = True
    result.add_result(date=date, value=saved.value)
