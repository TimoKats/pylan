
<div align="center">
  <img src=".github/logo.png" width="60%" alt="pylan-logo" />
</div>

## About

[![Unit tests](https://github.com/TimoKats/pylan/actions/workflows/unit_test.yml/badge.svg)](https://github.com/TimoKats/pylan/actions/workflows/unit_test.yml) 
[![GitHub tag](https://img.shields.io/github/tag/TimoKats/pylan?include_prereleases=&sort=semver&color=blue)](https://github.com/TimoKats/pylan/releases/)
[![License: BSD](https://img.shields.io/badge/License-BSD_1--Clause-blue.svg)](https://opensource.org/licenses/BSD-1-clause)
[![stars - pylan](https://img.shields.io/github/stars/TimoKats/pylan?style=social)](https://github.com/TimoKats/pylan)
[![forks - pylan](https://img.shields.io/github/forks/TimoKats/pylan?style=social)](https://github.com/TimoKats/pylan) 

Pylan is a library that calulates/analyzes the combined impact of recurring events. For example, it can be used to analyze the impact of financial patterns, like investment gains, savings, and inflation.

## Getting started

To get started, you can install the Python library using PyPi with the following command:

```
pip install pylan-lib
```

This code snippet shows some functionalities available when doing simulations. For more information, please see the documentation on [pypi](https://pypi.org/project/pylan-lib/). **Also, I've added some useful examples of pylan in [this slidedeck](https://timokats.xyz/downloads/2025_pylan_presentation.pdf)**

```python
import matplotlib.pyplot as plt

from pylan import Item, Subtract, Add, Multiply

savings = Item(start_value=100)
salary_payments = Add("1m", 2500, offset="24d") # Salary paid every month at the 24th
salary_increase = Multiply("1y", 1.2) # Salary grows each year 20%
mortgage = Subtract("0 0 2 * *", 1500)  # cron support

salary_payments.add_pattern(salary_increase) # Add increase to salary pattern
savings.add_patterns([salary_payments, mortgage])
result = savings.run("2024-1-1", "2028-1-1")

x, y = result.plot_axes()

plt.plot(x, y)
plt.show()
```

<div align="center">
  <img src=".github/example.png" width="100%" alt="pylan-logo" />
</div>

## Roadmap
This version is very basic. I plan to add more things, so I'm looking for suggestions. This is a list of basic ideas that are currently on the roadmap.
- Multivariate operators. E.g. Adding salary that grows over time. Or bonds that pay off over time and at the end.
- Combining items and interact between them. For example, take money out of a savings item and put it in an investment item.
- More built-in timeframes, like quarterly, YTD, YOY, etc.
- ...
