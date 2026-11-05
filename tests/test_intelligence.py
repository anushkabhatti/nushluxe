import unittest
from datetime import date

from core.maintenance import Routine
from core.products import Product

from intelligence.intelligence_service import (
    ENABLE_AI,
    build_ai_context,
    explain_plan
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


class TestIntelligenceService(unittest.TestCase):

    def setUp(self):

        routine = Routine(
            service="Hair",
            last_completed=date.today(),
            frequency_weeks=8
        )

        product = Product(
            product="Foundation",
            category="Makeup",
            last_restocked=date.today(),
            replenish_every_weeks=1,
            estimated_cost=65
        )

        self.routine_repo = FakeRoutineRepository(
            [routine]
        )

        self.product_repo = FakeProductRepository(
            [product]
        )

        self.context = build_ai_context(
            self.routine_repo,
            self.product_repo
        )

    def test_ai_is_disabled(self):

        self.assertFalse(
            ENABLE_AI
        )

    def test_context_has_required_fields(self):

        required_fields = {
            "today",
            "maintenance",
            "products",
            "summary",
            "budget",
            "constraints",
        }

        self.assertEqual(
            set(self.context.keys()),
            required_fields
        )

    def test_context_contains_data(self):

        self.assertEqual(
            len(self.context["maintenance"]),
            1
        )

        self.assertEqual(
            len(self.context["products"]),
            1
        )

        self.assertEqual(
            self.context["products"][0]["name"],
            "Foundation"
        )

        self.assertEqual(
            self.context["products"][0][
                "estimated_cost"
            ],
            65.0
        )

    def test_explain_plan_works_without_ai(self):

        result = explain_plan(
            self.context
        )

        self.assertIn(
            "AI is currently disabled",
            result
        )


if __name__ == "__main__":
    unittest.main()