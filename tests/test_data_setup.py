import tempfile
import unittest
from pathlib import Path

from utils.data_setup import (
    ensure_local_data_files,
    get_sample_files,
    reset_demo_data_files
)


class TestDataSetup(unittest.TestCase):

    def test_creates_missing_local_files(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_path = Path(temp_dir)

            routine_file = (
                temp_path
                / "nushluxe_data_v2.json"
            )

            product_file = (
                temp_path
                / "nushluxe_products.json"
            )

            self.assertFalse(
                routine_file.exists()
            )

            self.assertFalse(
                product_file.exists()
            )

            ensure_local_data_files(
                routine_file,
                product_file
            )

            self.assertTrue(
                routine_file.exists()
            )

            self.assertTrue(
                product_file.exists()
            )

    def test_existing_files_are_not_overwritten(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_path = Path(temp_dir)

            routine_file = (
                temp_path
                / "nushluxe_data_v2.json"
            )

            product_file = (
                temp_path
                / "nushluxe_products.json"
            )

            routine_file.write_text(
                "existing routine data"
            )

            product_file.write_text(
                "existing product data"
            )

            ensure_local_data_files(
                routine_file,
                product_file
            )

            self.assertEqual(
                routine_file.read_text(),
                "existing routine data"
            )

            self.assertEqual(
                product_file.read_text(),
                "existing product data"
            )

    def test_reset_restores_sample_data(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_path = Path(temp_dir)

            routine_file = (
                temp_path
                / "nushluxe_data_v2.json"
            )

            product_file = (
                temp_path
                / "nushluxe_products.json"
            )

            ensure_local_data_files(
                routine_file,
                product_file
            )

            routine_file.write_text(
                "changed routine data"
            )

            product_file.write_text(
                "changed product data"
            )

            reset_demo_data_files(
                routine_file,
                product_file
            )

            (
                sample_routines,
                sample_products
            ) = get_sample_files()

            self.assertEqual(
                routine_file.read_text(),
                sample_routines.read_text()
            )

            self.assertEqual(
                product_file.read_text(),
                sample_products.read_text()
            )


if __name__ == "__main__":
    unittest.main()