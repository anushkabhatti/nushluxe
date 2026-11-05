from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from uuid import uuid4


REPLENISH_SOON_DAYS = 7


@dataclass
class Product:
    product: str
    category: str
    last_restocked: date
    replenish_every_weeks: int
    estimated_cost: float = 0.0

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    created_at: str = field(
        default_factory=lambda:
        datetime.now().isoformat(timespec="seconds")
    )

    updated_at: str = field(
        default_factory=lambda:
        datetime.now().isoformat(timespec="seconds")
    )

    @property
    def next_replenish(self):
        return self.last_restocked + timedelta(
            weeks=self.replenish_every_weeks
        )

    @property
    def status(self):
        today = date.today()

        days_until_replenish = (
            self.next_replenish - today
        ).days

        if days_until_replenish < 0:
            return "OVERDUE"

        elif days_until_replenish <= REPLENISH_SOON_DAYS:
            return "REPLENISH_SOON"

        else:
            return "ON_TRACK"

    def update(
        self,
        product=None,
        category=None,
        last_restocked=None,
        replenish_every_weeks=None,
        estimated_cost=None
    ):

        if product is not None:
            self.product = product.strip().title()

        if category is not None:
            self.category = category.strip().title()

        if last_restocked is not None:
            self.last_restocked = last_restocked

        if replenish_every_weeks is not None:
            self.replenish_every_weeks = (
                replenish_every_weeks
            )

        if estimated_cost is not None:
            self.estimated_cost = float(
                estimated_cost
            )

        self.updated_at = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.title(),
            "category": self.category.title(),
            "last_restocked":
                self.last_restocked.isoformat(),
            "replenish_every_weeks":
                self.replenish_every_weeks,
            "next_replenish":
                self.next_replenish.isoformat(),
            "estimated_cost":
                float(self.estimated_cost),
            "status":
                self.status,
            "created_at":
                self.created_at,
            "updated_at":
                self.updated_at,
        }


def get_product_dashboard_metrics(products):

    total_products = len(products)

    replenish_soon = sum(
        1
        for product in products
        if product.status == "REPLENISH_SOON"
    )

    overdue = sum(
        1
        for product in products
        if product.status == "OVERDUE"
    )

    on_track = sum(
        1
        for product in products
        if product.status == "ON_TRACK"
    )

    attention_products = [
        product
        for product in products
        if product.status in (
            "OVERDUE",
            "REPLENISH_SOON"
        )
    ]

    attention_cost = sum(
        product.estimated_cost
        for product in attention_products
    )

    return {
        "total_products": total_products,
        "replenish_soon": replenish_soon,
        "overdue": overdue,
        "on_track": on_track,
        "attention_cost": attention_cost,
    }