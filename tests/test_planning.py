import unittest
from datetime import date

from core.maintenance import Routine
from core.products import Product
from core.planning import (
    get_planning_facts,
    get_planning_summary
)


class FakeRoutineRepository:

    def __init__(self, routines):
        self.routines = routines

    def list_all(self):
        return self.routines


class FakeProductRepository:

    def __init__(self, products):
        self.products = products

    def list_all(self):
        return self.products


class TestPlanning(unittest.TestCase):

    def setUp(self):

        self.routine = Routine(
            service="Hair",
            last_completed=date.today(),
            frequency_weeks=8
        )

        self.product = Product(
            product="Foundation",
            category="Makeup",
            last_restocked=date.today(),
            replenish_every_weeks=1,
            estimated_cost=65
        )

        self.routine_repo = FakeRoutineRepository(
            [self.routine]
        )

        self.product_repo = FakeProductRepository(
            [self.product]
        )

    def test_planning_facts_include_both_types(self):

        facts = get_planning_facts(
            self.routine_repo,
            self.product_repo
        )

        types = {
            item["type"]
            for item in facts
        }

        self.assertIn(
            "maintenance",
            types
        )

        self.assertIn(
            "product",
            types
        )

    def test_planning_facts_are_sorted(self):

        facts = get_planning_facts(
            self.routine_repo,
            self.product_repo
        )

        dates = [
            item["due_date"]
            for item in facts
        ]

        self.assertEqual(
            dates,
            sorted(dates)
        )

    def test_product_cost_is_in_summary(self):

        facts = get_planning_facts(
            self.routine_repo,
            self.product_repo
        )

        summary = get_planning_summary(
            facts
        )

        self.assertEqual(
            summary["products_needing_attention"],
            1
        )

        self.assertEqual(
            summary["total_estimated_cost"],
            65.0
        )

    def test_summary_has_required_fields(self):

        facts = get_planning_facts(
            self.routine_repo,
            self.product_repo
        )

        summary = get_planning_summary(
            facts
        )

        self.assertIn(
            "upcoming_maintenance",
            summary
        )

        self.assertIn(
            "products_needing_attention",
            summary
        )

        self.assertIn(
            "overdue_items",
            summary
        )

        self.assertIn(
            "total_estimated_cost",
            summary
        )


if __name__ == "__main__":
    unittest.main()