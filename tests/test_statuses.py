import unittest
from datetime import date, timedelta

from utils.dates import get_status


class TestStatusFunctions(unittest.TestCase):

    def test_overdue(self):
        yesterday = date.today() - timedelta(days=1)

        self.assertEqual(
            get_status(yesterday),
            "OVERDUE"
        )

    def test_due_today(self):
        self.assertEqual(
            get_status(date.today()),
            "DUE TODAY"
        )

    def test_upcoming(self):
        tomorrow = date.today() + timedelta(days=1)

        self.assertEqual(
            get_status(tomorrow),
            "UPCOMING"
        )


if __name__ == "__main__":
    unittest.main()
