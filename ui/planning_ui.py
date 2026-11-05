import streamlit as st

from html import escape
from textwrap import dedent

from core.planning import (
    get_planning_facts,
    get_planning_summary
)


def render_html(content):
    st.html(
        dedent(content).strip()
    )


def render_planning_summary(
    routine_repository,
    product_repository
):

    facts = get_planning_facts(
        routine_repository,
        product_repository
    )

    summary = get_planning_summary(
        facts
    )

    # ==========================================
    # HEADER
    # ==========================================

    render_html(
        """
        <div class="section-kicker">
            Planning Overview
        </div>

        <div class="section-heading">
            What Needs Your Attention
        </div>

        <div class="section-copy">
            A combined view of your maintenance
            and product replenishment schedule.
        </div>
        """
    )

    # ==========================================
    # SUMMARY METRICS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        render_html(
            f"""
            <div class="metric-box">

                <div class="metric-label">
                    Upcoming Maintenance
                </div>

                <div class="metric-value">
                    {summary["upcoming_maintenance"]}
                </div>

                <div class="metric-subtext">
                    Services ahead
                </div>

            </div>
            """
        )

    with col2:

        render_html(
            f"""
            <div class="metric-box">

                <div class="metric-label">
                    Products to Replenish
                </div>

                <div class="metric-value">
                    {summary["products_needing_attention"]}
                </div>

                <div class="metric-subtext">
                    Soon or overdue
                </div>

            </div>
            """
        )

    with col3:

        render_html(
            f"""
            <div class="metric-box">

                <div class="metric-label">
                    Overdue Items
                </div>

                <div class="metric-value">
                    {summary["overdue_items"]}
                </div>

                <div class="metric-subtext">
                    Need attention
                </div>

            </div>
            """
        )

    with col4:

        render_html(
            f"""
            <div class="metric-box">

                <div class="metric-label">
                    Estimated Product Cost
                </div>

                <div class="metric-value">
                    ${summary["total_estimated_cost"]:,.0f}
                </div>

                <div class="metric-subtext">
                    Replenish soon + overdue
                </div>

            </div>
            """
        )

    # ==========================================
    # NEXT ITEMS
    # ==========================================

    render_html(
        """
        <div class="luxury-rule"></div>

        <div class="section-kicker">
            Next Up
        </div>

        <div class="section-heading">
            Your Upcoming Plan
        </div>
        """
    )

    if not facts:

        st.info(
            "Nothing has been added to your planning system yet."
        )

        return

    for item in facts[:6]:

        safe_name = escape(
            item["name"]
        )

        if item["type"] == "maintenance":

            type_label = "Maintenance"

        else:

            type_label = "Product"

        if item["status"] == "OVERDUE":

            status_label = "Overdue"

        elif item["status"] == "DUE TODAY":

            status_label = "Due Today"

        elif item["status"] == "REPLENISH_SOON":

            status_label = "Replenish Soon"

        elif item["status"] == "ON_TRACK":

            status_label = "On Track"

        else:

            status_label = "Upcoming"

        with st.container(border=True):

            left, middle, right = st.columns(
                [2.3, 1.5, 1.3]
            )

            with left:

                render_html(
                    f"""
                    <div class="tiny-label">
                        {type_label}
                    </div>

                    <div class="routine-name">
                        {safe_name}
                    </div>
                    """
                )

            with middle:

                render_html(
                    f"""
                    <div class="tiny-label">
                        Due
                    </div>

                    <div class="routine-value">
                        {item["due_date"]}
                    </div>
                    """
                )

            with right:

                render_html(
                    f"""
                    <div class="tiny-label">
                        Status
                    </div>

                    <div class="routine-value">
                        {status_label}
                    </div>
                    """
                )