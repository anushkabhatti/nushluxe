def get_planning_facts(
    routine_repository,
    product_repository
):

    facts = []

    # ---------------------------------
    # MAINTENANCE FACTS
    # ---------------------------------

    routines = routine_repository.list_all()

    for routine in routines:

        facts.append(
            {
                "id": routine.id,
                "type": "maintenance",
                "name": routine.service,
                "due_date": routine.next_due.isoformat(),
                "status": routine.status,
                "estimated_cost": 0.0,
                "is_overdue": routine.status == "OVERDUE",
                "is_upcoming": routine.status in (
                    "UPCOMING",
                    "DUE TODAY"
                ),
            }
        )

    # ---------------------------------
    # PRODUCT FACTS
    # ---------------------------------

    products = product_repository.list_all()

    for product in products:

        facts.append(
            {
                "id": product.id,
                "type": "product",
                "name": product.product,
                "due_date": product.next_replenish.isoformat(),
                "status": product.status,
                "estimated_cost": float(
                    product.estimated_cost
                ),
                "is_overdue": product.status == "OVERDUE",
                "is_upcoming": product.status in (
                    "ON_TRACK",
                    "REPLENISH_SOON"
                ),
            }
        )

    facts.sort(
        key=lambda item: item["due_date"]
    )

    return facts


def get_planning_summary(facts):

    upcoming_maintenance = sum(
        1
        for item in facts
        if (
            item["type"] == "maintenance"
            and item["is_upcoming"]
        )
    )

    products_needing_attention = sum(
        1
        for item in facts
        if (
            item["type"] == "product"
            and item["status"] in (
                "REPLENISH_SOON",
                "OVERDUE"
            )
        )
    )

    overdue_items = sum(
        1
        for item in facts
        if item["is_overdue"]
    )

    total_estimated_cost = sum(
        item["estimated_cost"]
        for item in facts
        if (
            item["type"] == "product"
            and item["status"] in (
                "REPLENISH_SOON",
                "OVERDUE"
            )
        )
    )

    return {
        "upcoming_maintenance": upcoming_maintenance,
        "products_needing_attention": products_needing_attention,
        "overdue_items": overdue_items,
        "total_estimated_cost": total_estimated_cost,
    }