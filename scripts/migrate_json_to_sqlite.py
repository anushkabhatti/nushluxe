import json
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

ROUTINE_JSON = PROJECT_ROOT / "nushluxe_data_v2.json"
PRODUCT_JSON = PROJECT_ROOT / "nushluxe_products.json"

DATABASE_FILE = PROJECT_ROOT / "nushluxe_migration_test.db"


def load_items(file_path, collection_name):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Support both legacy list JSON
    # and newer versioned JSON.
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        return data.get(collection_name, [])

    return []


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS routines (
            id TEXT PRIMARY KEY,
            service TEXT NOT NULL,
            last_completed TEXT NOT NULL,
            frequency_weeks INTEGER NOT NULL,
            created_at TEXT,
            updated_at TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            last_restocked TEXT NOT NULL,
            replenish_every_weeks INTEGER NOT NULL,
            estimated_cost REAL NOT NULL,
            created_at TEXT,
            updated_at TEXT
        )
        """
    )

    connection.commit()


def migrate_routines(connection, routines):
    cursor = connection.cursor()

    for routine in routines:
        cursor.execute(
            """
            INSERT OR REPLACE INTO routines (
                id,
                service,
                last_completed,
                frequency_weeks,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                routine.get("id"),
                routine.get("service"),
                routine.get("last_completed"),
                routine.get("frequency_weeks"),
                routine.get("created_at"),
                routine.get("updated_at"),
            ),
        )

    connection.commit()


def migrate_products(connection, products):
    cursor = connection.cursor()

    for product in products:
        cursor.execute(
            """
            INSERT OR REPLACE INTO products (
                id,
                product,
                category,
                last_restocked,
                replenish_every_weeks,
                estimated_cost,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                product.get("id"),
                product.get("product"),
                product.get("category"),
                product.get("last_restocked"),
                product.get("replenish_every_weeks"),
                float(product.get("estimated_cost", 0)),
                product.get("created_at"),
                product.get("updated_at"),
            ),
        )

    connection.commit()


def count_rows(connection, table_name):
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    return cursor.fetchone()[0]


def main():
    print("Nushluxe JSON → SQLite Migration")
    print("--------------------------------")

    routines = load_items(
        ROUTINE_JSON,
        "routines"
    )

    products = load_items(
        PRODUCT_JSON,
        "products"
    )

    print(
        f"Routines found in JSON: {len(routines)}"
    )

    print(
        f"Products found in JSON: {len(products)}"
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    create_tables(connection)

    migrate_routines(
        connection,
        routines
    )

    migrate_products(
        connection,
        products
    )

    routine_count = count_rows(
        connection,
        "routines"
    )

    product_count = count_rows(
        connection,
        "products"
    )

    connection.close()

    print()
    print("Migration complete.")
    print(
        f"SQLite routines: {routine_count}"
    )
    print(
        f"SQLite products: {product_count}"
    )
    print(
        f"Test database: {DATABASE_FILE.name}"
    )
    print()
    print(
        "Your original JSON files were not changed."
    )


if __name__ == "__main__":
    main()