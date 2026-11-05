import json
from datetime import date
from pathlib import Path
from typing import List, Optional

from core.maintenance import Routine
from core.products import Product
from storage.repositories import RoutineRepository, ProductRepository


SCHEMA_VERSION = 1


def _read_json(file_path: Path):
    if not file_path.exists():
        return None

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return None


def _write_json(file_path: Path, data):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


class JsonRoutineRepository(RoutineRepository):

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def _load_items(self) -> List[dict]:
        data = _read_json(self.file_path)

        if data is None:
            return []

        # Legacy format:
        # [
        #   {...},
        #   {...}
        # ]
        if isinstance(data, list):
            return data

        # New versioned format:
        # {
        #   "schema_version": 1,
        #   "routines": [...]
        # }
        if isinstance(data, dict):
            return data.get("routines", [])

        return []

    def _save_items(self, routines: List[Routine]):
        data = {
            "schema_version": SCHEMA_VERSION,
            "routines": [
                routine.to_dict()
                for routine in routines
            ],
        }

        _write_json(self.file_path, data)

    def _dict_to_routine(self, item: dict) -> Routine:
        routine_kwargs = {
            "service": item["service"],
            "last_completed": date.fromisoformat(
                item["last_completed"]
            ),
            "frequency_weeks": int(
                item["frequency_weeks"]
            ),
        }

        if item.get("id"):
            routine_kwargs["id"] = item["id"]

        if item.get("created_at"):
            routine_kwargs["created_at"] = item["created_at"]

        if item.get("updated_at"):
            routine_kwargs["updated_at"] = item["updated_at"]

        return Routine(**routine_kwargs)

    def list_all(self) -> List[Routine]:
        routines = []

        for item in self._load_items():
            try:
                routines.append(
                    self._dict_to_routine(item)
                )

            except (
                KeyError,
                TypeError,
                ValueError
            ):
                continue

        return routines

    def get_by_id(
        self,
        routine_id: str
    ) -> Optional[Routine]:

        for routine in self.list_all():
            if routine.id == routine_id:
                return routine

        return None

    def add(self, routine: Routine) -> Routine:
        routines = self.list_all()
        routines.append(routine)

        self._save_items(routines)

        return routine

    def update(self, routine: Routine) -> Routine:
        routines = self.list_all()

        updated = False

        for index, existing in enumerate(routines):
            if existing.id == routine.id:
                routines[index] = routine
                updated = True
                break

        if not updated:
            raise ValueError(
                f"Routine with id {routine.id} was not found."
            )

        self._save_items(routines)

        return routine

    def delete(self, routine_id: str) -> bool:
        routines = self.list_all()

        remaining = [
            routine
            for routine in routines
            if routine.id != routine_id
        ]

        if len(remaining) == len(routines):
            return False

        self._save_items(remaining)

        return True

    def migrate_legacy_file(self):
        routines = self.list_all()
        self._save_items(routines)

        return len(routines)


class JsonProductRepository(ProductRepository):

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def _load_items(self) -> List[dict]:
        data = _read_json(self.file_path)

        if data is None:
            return []

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return data.get("products", [])

        return []

    def _save_items(self, products: List[Product]):
        data = {
            "schema_version": SCHEMA_VERSION,
            "products": [
                product.to_dict()
                for product in products
            ],
        }

        _write_json(self.file_path, data)

    def _dict_to_product(self, item: dict) -> Product:
        product_kwargs = {
            "product": item["product"],
            "category": item["category"],
            "last_restocked": date.fromisoformat(
                item["last_restocked"]
            ),
            "replenish_every_weeks": int(
                item["replenish_every_weeks"]
            ),
            "estimated_cost": float(
                item.get("estimated_cost", 0)
            ),
        }

        if item.get("id"):
            product_kwargs["id"] = item["id"]

        if item.get("created_at"):
            product_kwargs["created_at"] = item["created_at"]

        if item.get("updated_at"):
            product_kwargs["updated_at"] = item["updated_at"]

        return Product(**product_kwargs)

    def list_all(self) -> List[Product]:
        products = []

        for item in self._load_items():
            try:
                products.append(
                    self._dict_to_product(item)
                )

            except (
                KeyError,
                TypeError,
                ValueError
            ):
                continue

        return products

    def get_by_id(
        self,
        product_id: str
    ) -> Optional[Product]:

        for product in self.list_all():
            if product.id == product_id:
                return product

        return None

    def add(self, product: Product) -> Product:
        products = self.list_all()
        products.append(product)

        self._save_items(products)

        return product

    def update(self, product: Product) -> Product:
        products = self.list_all()

        updated = False

        for index, existing in enumerate(products):
            if existing.id == product.id:
                products[index] = product
                updated = True
                break

        if not updated:
            raise ValueError(
                f"Product with id {product.id} was not found."
            )

        self._save_items(products)

        return product

    def delete(self, product_id: str) -> bool:
        products = self.list_all()

        remaining = [
            product
            for product in products
            if product.id != product_id
        ]

        if len(remaining) == len(products):
            return False

        self._save_items(remaining)

        return True

    def migrate_legacy_file(self):
        products = self.list_all()
        self._save_items(products)

        return len(products)