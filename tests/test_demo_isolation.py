import tempfile
import unittest
from pathlib import Path

from core.maintenance import Routine
from storage.json_repository import JsonRoutineRepository
from utils.data_setup import ensure_local_data_files


class TestDemoIsolation(unittest.TestCase):

    def test_two_sessions_use_separate_data(self):

        with tempfile.TemporaryDirectory() as session_a:
            with tempfile.TemporaryDirectory() as session_b:

                session_a_path = Path(session_a)
                session_b_path = Path(session_b)

                routine_a = (
                    session_a_path
                    / "nushluxe_data_v2.json"
                )

                product_a = (
                    session_a_path
                    / "nushluxe_products.json"
                )

                routine_b = (
                    session_b_path
                    / "nushluxe_data_v2.json"
                )

                product_b = (
                    session_b_path
                    / "nushluxe_products.json"
                )

                ensure_local_data_files(
                    routine_a,
                    product_a
                )

                ensure_local_data_files(
                    routine_b,
                    product_b
                )

                repo_a = JsonRoutineRepository(
                    routine_a
                )

                repo_b = JsonRoutineRepository(
                    routine_b
                )

                starting_count_a = len(
                    repo_a.list_all()
                )

                starting_count_b = len(
                    repo_b.list_all()
                )

                self.assertEqual(
                    starting_count_a,
                    starting_count_b
                )

                new_routine = Routine(
                    service="Session A Test",
                    last_completed=__import__(
                        "datetime"
                    ).date.today(),
                    frequency_weeks=4
                )

                repo_a.add(
                    new_routine
                )

                self.assertEqual(
                    len(repo_a.list_all()),
                    starting_count_a + 1
                )

                self.assertEqual(
                    len(repo_b.list_all()),
                    starting_count_b
                )


if __name__ == "__main__":
    unittest.main()