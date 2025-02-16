import unittest
from datetime import datetime

from pylan.utils import timedelta_from_schedule


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
            timedelta_from_schedule(
                "monthly", datetime(2025, 1, 5), datetime(2025, 4, 5)
            ),
        )

    def test_datetime_schedule(self):
        self.assertEqual(
            [datetime(2025, 1, 5), datetime(2025, 4, 5)],
            timedelta_from_schedule([datetime(2025, 1, 5), datetime(2025, 4, 5)]),
        )


if __name__ == "__main__":
    unittest.main()
