from datetime import date

from core.planning import (
    get_planning_facts,
    get_planning_summary
)


# Real AI stays OFF during foundation development.
ENABLE_AI = False


def build_ai_context(
    routine_repository,
    product_repository
):
    """
    Build deterministic, structured facts that can
    eventually be sent to an AI model.

    Python calculates facts first.
    AI will only interpret them later.
    """

    facts = get_planning_facts(
        routine_repository,
        product_repository
    )

    summary = get_planning_summary(
        facts
    )

    maintenance = [
        item
        for item in facts
        if item["type"] == "maintenance"
    ]

    products = [
        item
        for item in facts
        if item["type"] == "product"
    ]

    context = {
        "today": date.today().isoformat(),
        "maintenance": maintenance,
        "products": products,
        "summary": summary,
        "budget": None,
        "constraints": [],
    }

    return context


def explain_plan(context):
    """
    Placeholder for future AI integration.

    No external API is called during the
    foundation roadmap.
    """

    if not ENABLE_AI:
        return (
            "AI is currently disabled. "
            "Nushluxe planning facts are ready "
            "for future AI interpretation."
        )

    raise NotImplementedError(
        "Real AI integration has not been enabled yet."
    )