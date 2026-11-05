import json
import sqlite3
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

ROUTINE_JSON = PROJECT_ROOT / "nushluxe_data_v2.json"
PRODUCT_JSON = PROJECT_ROOT / "nushluxe_products.json"

DATABASE_FILE = PROJECT_ROOT / "nushluxe_migration_test.db"


def load_json_items(file_path, collection_name):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, list):
        return data

    return data.get(collection_name, [])


class TestDatabaseMigration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.connection = sqlite3.connect(
            DATABASE_FILE
        )

        cls.routines_json = load_json_items(
            ROUTINE_JSON,
            "routines"
        )

        cls.products_json = load_json_items(
            PRODUCT_JSON,
            "products"
        )

    @classmethod
    def tearDownClass(cls):

        cls.connection.close()

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