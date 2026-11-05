import unittest
from datetime import date

from utils.dates import calculate_next_due_date, get_days_text


class TestDateFunctions(unittest.TestCase):

    def test_calculate_next_due_date(self):
        result = calculate_next_due_date(
            date(2026, 10, 1),
            9
        )

        self.assertEqual(
            result,
            date(2026, 12, 3)
        )

    def test_due_today_text(self):
        today = date.today()

        self.assertEqual(
            get_days_text(today),
            "Due today"
        )


if __name__ == "__main__":
    unittest.main()
