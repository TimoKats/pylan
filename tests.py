import unittest
from datetime import datetime

from pylan import Item, Operators, Pattern
from pylan.schedule import timedelta_from_schedule


class TestTimeDelta(unittest.TestCase):
    def test_single_interval(self):
        self.assertEqual(
            [
                datetime(2025, 1, 1, 0, 0),
                datetime(2025, 1, 3, 0, 0),
                datetime(2025, 1, 5, 0, 0),
            ],
            timedelta_from_schedule("2d", datetime(2025, 1, 1), datetime(2025, 1, 5)),
        )

    def test_alternate_interval(self):
        self.assertEqual(
            [
                datetime(2025, 1, 5, 0, 0),
                datetime(2025, 1, 7, 0, 0),
                datetime(2025, 1, 10, 0, 0),
            ],
            timedelta_from_schedule(
                ["2d", "3d"], datetime(2025, 1, 5), datetime(2025, 1, 10)
            ),
        )

    def test_monthly_schedule(self):
        self.assertEqual(
            [
                datetime(2025, 1, 5, 0, 0),
                datetime(2025, 2, 5, 0, 0),
                datetime(2025, 3, 5, 0, 0),
                datetime(2025, 4, 5, 0, 0),
            ],
            timedelta_from_schedule("month", datetime(2025, 1, 5), datetime(2025, 4, 5)),
        )

    def test_datetime_schedule(self):
        self.assertEqual(
            [datetime(2025, 1, 5), datetime(2025, 4, 5)],
            timedelta_from_schedule([datetime(2025, 1, 5), datetime(2025, 4, 5)]),
        )

    def test_datetime_schedule_in_str(self):
        self.assertEqual(
            timedelta_from_schedule(["2025-1-5", "2025-4-5"]),
            timedelta_from_schedule([datetime(2025, 1, 5), datetime(2025, 4, 5)]),
        )

    def test_cron_schedule(self):
        self.assertEqual(
            timedelta_from_schedule(
                "0 0 2 * *", datetime(2024, 1, 1), datetime(2024, 3, 1)
            ),
            timedelta_from_schedule([datetime(2024, 1, 2), datetime(2024, 2, 2)]),
        )


class TestPatterns(unittest.TestCase):
    def test_basic_addition(self):
        adds = Pattern("1d", Operators.add, 10)
        start = Item(start_value=100)
        start.add_pattern(adds)
        self.assertEqual(
            start.run(datetime(2024, 5, 1), datetime(2024, 5, 10)).final, 200
        )

    def test_basic_multiplication(self):
        adds = Pattern("1d", Operators.add, 10)
        multiplies = Pattern("3d", Operators.multiply, 2)
        start = Item(start_value=100)
        start.add_pattern(adds)
        start.add_pattern(multiplies)
        self.assertEqual(
            start.run(datetime(2024, 5, 1), datetime(2024, 5, 10)).final, 2180
        )

    def test_pattern_manipulation(self):
        adds = Pattern("1d", Operators.add, 10, start_date="2024-5-3")
        start = Item(start_value=100)
        start.add_patterns([adds])
        self.assertEqual(
            start.run(datetime(2024, 5, 1), datetime(2024, 5, 10)).final, 180
        )

    def test_offset_start(self):
        test = Pattern("month", Operators.add, 1, offset_start="month")
        savings = Item(start_value=100)
        savings.add_pattern(test)
        savings.run("2024-1-1", "2024-2-1")
        self.assertEqual(1, len(savings.patterns[0].dt_schedule))


class TestItems(unittest.TestCase):
    def test_add_pattern(self):
        adds = Pattern("1d", Operators.add, 10)
        start = Item(start_value=100)
        start.add_pattern(adds)
        self.assertEqual(len(start.patterns), 1)

    def test_add_patterns(self):
        adds = Pattern("1d", Operators.add, 10)
        test = Pattern("2d", Operators.add, 10)
        start = Item(start_value=100)
        start.add_patterns([adds, test])
        self.assertEqual(len(start.patterns), 2)


if __name__ == "__main__":
    unittest.main()
