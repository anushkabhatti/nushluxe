from abc import ABC, abstractmethod
from typing import List, Optional

from core.maintenance import Routine
from core.products import Product


class RoutineRepository(ABC):

    @abstractmethod
    def list_all(self) -> List[Routine]:
        pass

    @abstractmethod
    def get_by_id(self, routine_id: str) -> Optional[Routine]:
        pass

    @abstractmethod
    def add(self, routine: Routine) -> Routine:
        pass

    @abstractmethod
    def update(self, routine: Routine) -> Routine:
        pass

    @abstractmethod
    def delete(self, routine_id: str) -> bool:
        pass


class ProductRepository(ABC):

    @abstractmethod
    def list_all(self) -> List[Product]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def add(self, product: Product) -> Product:
        pass

    @abstractmethod
    def update(self, product: Product) -> Product:
        pass

    @abstractmethod
    def delete(self, product_id: str) -> bool:
        pass