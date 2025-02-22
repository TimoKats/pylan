
<div align="center">
  <img src="https://github.com/TimoKats/pylan/blob/main/.github/logo.png" width="60%" alt="pylan-logo" />
</div>

---
[![Tests](https://github.com/TimoKats/pylan/actions/workflows/test.yml/badge.svg)](https://github.com/TimoKats/pylan/actions/workflows/test.yml) 
[![GitHub tag](https://img.shields.io/github/tag/TimoKats/pylan?include_prereleases=&sort=semver&color=cyan)](https://github.com/TimoKats/pylan/releases/)
[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)
[![stars - pylan](https://img.shields.io/github/stars/TimoKats/pylan?style=social)](https://github.com/TimoKats/pylan)
[![forks - pylan](https://img.shields.io/github/forks/TimoKats/pylan?style=social)](https://github.com/TimoKats/pylan) 

Pylan is a Python library for simulating the impact of multiple patterns over time. For example, pylan can be used to simulate the impact of financial patterns, like investment gains, adding savings, and inflation.  

### Getting started

To get started, you can install the Python library using PyPi with the following command:

```
pip install pylan-lib
```

This code snippet shows the different options available when doing simulations.

```
savings = Item(start_value=100)

inflation = Pattern("6w", Operators.divide, 1.08)
salary_adds = Pattern("month", Operators.add, 2000, offset_start="15d")  # every month at the 15th
investment_gains = Pattern("month", Operators.multiply, 1.1)
mortgage = Pattern("0 0 2 * *", Operators.subtract, 1500)  # cron support

savings.add_patterns([salary_adds, inflation, investment_gains, mortgage])

result = savings.run("2024-1-1", "2025-1-1")
x, y = result.plot_axes()

plt.plot(x, y)
plt.show()
```

For more information, please see the documentation on [pypi](https://pypi.org/project/pylan-lib/).

### Roadmap
This version is very basic. I plan to add more things, so I'm looking for suggestions. This is a list of basic ideas that are currently on the roadmap.
- Multivariate operators. E.g. Adding salary that grows over time. Or bonds that pay off over time and at the end.
- Combining items and interact between them. For example, take money out of a savings item and put it in an investment item.
- More built-in timeframes, like quarterly, YTD, YOY, etc.
- ...
