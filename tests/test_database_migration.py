import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path

from scripts.migrate_json_to_sqlite import (
    create_tables,
    load_items,
    migrate_products,
    migrate_routines,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SAMPLE_ROUTINES = (
    PROJECT_ROOT
    / "sample_data"
    / "sample_routines.json"
)

SAMPLE_PRODUCTS = (
    PROJECT_ROOT
    / "sample_data"
    / "sample_products.json"
)


class TestDatabaseMigration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.temp_dir = tempfile.TemporaryDirectory()

        temp_path = Path(cls.temp_dir.name)

        cls.routine_json = (
            temp_path / "sample_routines.json"
        )

        cls.product_json = (
            temp_path / "sample_products.json"
        )

        cls.database_file = (
            temp_path / "migration_test.db"
        )

        shutil.copy2(
            SAMPLE_ROUTINES,
            cls.routine_json
        )

        shutil.copy2(
            SAMPLE_PRODUCTS,
            cls.product_json
        )

        cls.routines_json = load_items(
            cls.routine_json,
            "routines"
        )

        cls.products_json = load_items(
            cls.product_json,
            "products"
        )

        cls.connection = sqlite3.connect(
            cls.database_file
        )

        create_tables(
            cls.connection
        )

        migrate_routines(
            cls.connection,
            cls.routines_json
        )

        migrate_products(
            cls.connection,
            cls.products_json
        )

    @classmethod
    def tearDownClass(cls):

        cls.connection.close()
        cls.temp_dir.cleanup()

    def test_routine_count_matches(self):

        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM routines"
        )

        sqlite_count = cursor.fetchone()[0]

        self.assertEqual(
            sqlite_count,
            len(self.routines_json)
        )

    def test_product_count_matches(self):

        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM products"
        )

        sqlite_count = cursor.fetchone()[0]

        self.assertEqual(
            sqlite_count,
            len(self.products_json)
        )

    def test_routine_data_matches(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                service,
                last_completed,
                frequency_weeks,
                created_at,
                updated_at
            FROM routines
            ORDER BY id
            """
        )

        sqlite_rows = cursor.fetchall()

        json_rows = sorted(
            [
                (
                    item.get("id"),
                    item.get("service"),
                    item.get("last_completed"),
                    int(item.get("frequency_weeks")),
                    item.get("created_at"),
                    item.get("updated_at"),
                )
                for item in self.routines_json
            ],
            key=lambda row: row[0]
        )

        self.assertEqual(
            sqlite_rows,
            json_rows
        )

    def test_product_data_matches(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                product,
                category,
                last_restocked,
                replenish_every_weeks,
                estimated_cost,
                created_at,
                updated_at
            FROM products
            ORDER BY id
            """
        )

        sqlite_rows = cursor.fetchall()

        json_rows = sorted(
            [
                (
                    item.get("id"),
                    item.get("product"),
                    item.get("category"),
                    item.get("last_restocked"),
                    int(
                        item.get(
                            "replenish_every_weeks"
                        )
                    ),
                    float(
                        item.get(
                            "estimated_cost",
                            0
                        )
                    ),
                    item.get("created_at"),
                    item.get("updated_at"),
                )
                for item in self.products_json
            ],
            key=lambda row: row[0]
        )

        self.assertEqual(
            sqlite_rows,
            json_rows
        )


if __name__ == "__main__":
    unittest.main()