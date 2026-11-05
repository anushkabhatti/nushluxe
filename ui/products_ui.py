import streamlit as st

from datetime import date
from html import escape
from textwrap import dedent

from core.products import (
    Product,
    get_product_dashboard_metrics
)


def render_html(content):
    st.html(
        dedent(content).strip()
    )


def render_products(repository):

    products = repository.list_all()

    products.sort(
        key=lambda product: product.next_replenish
    )

    metrics = get_product_dashboard_metrics(
        products
    )

    if "edit_product_id" not in st.session_state:
        st.session_state.edit_product_id = None

    products_tab, add_product_tab = st.tabs(
        [
            "Products",
            "Add Product"
        ]
    )

    # =====================================================
    # PRODUCTS LIST
    # =====================================================

    with products_tab:

        render_html(
            """
            <div class="section-kicker">
                Products
            </div>

            <div class="section-heading">
                Your Beauty & Wellness Bag
            </div>

            <div class="section-copy">
                Track the products you replenish regularly,
                what needs attention next, and the estimated
                cost of upcoming replenishment.
            </div>
            """
        )

        # =================================================
        # PRODUCT DASHBOARD METRICS
        # =================================================

        metric1, metric2, metric3, metric4 = (
            st.columns(4)
        )

        with metric1:

            render_html(
                f"""
                <div class="metric-box">

                    <div class="metric-label">
                        Total Products
                    </div>

                    <div class="metric-value">
                        {metrics["total_products"]}
                    </div>

                    <div class="metric-subtext">
                        In your product system
                    </div>

                </div>
                """
            )

        with metric2:

            render_html(
                f"""
                <div class="metric-box">

                    <div class="metric-label">
                        Replenish Soon
                    </div>

                    <div class="metric-value">
                        {metrics["replenish_soon"]}
                    </div>

                    <div class="metric-subtext">
                        Due within 7 days
                    </div>

                </div>
                """
            )

        with metric3:

            render_html(
                f"""
                <div class="metric-box">

                    <div class="metric-label">
                        Overdue
                    </div>

                    <div class="metric-value">
                        {metrics["overdue"]}
                    </div>

                    <div class="metric-subtext">
                        Needs attention
                    </div>

                </div>
                """
            )

        with metric4:

            render_html(
                f"""
                <div class="metric-box">

                    <div class="metric-label">
                        Upcoming Cost
                    </div>

                    <div class="metric-value">
                        ${metrics["attention_cost"]:,.0f}
                    </div>

                    <div class="metric-subtext">
                        Overdue + replenish soon
                    </div>

                </div>
                """
            )

        # =================================================
        # PRODUCT CARDS
        # =================================================

        if not products:

            st.info(
                "You have not added any products yet."
            )

        else:

            for product in products:

                safe_product = escape(
                    product.product.title()
                )

                safe_category = escape(
                    product.category.title()
                )

                if product.status == "OVERDUE":

                    status_html = """
                    <span class="status-pill status-overdue">
                        Overdue
                    </span>
                    """

                elif product.status == "REPLENISH_SOON":

                    status_html = """
                    <span class="status-pill status-due">
                        Replenish Soon
                    </span>
                    """

                else:

                    status_html = """
                    <span class="status-pill status-upcoming">
                        On Track
                    </span>
                    """

                with st.container(border=True):

                    col1, col2, col3, col4 = (
                        st.columns(
                            [2.5, 1.7, 1.4, 1.1]
                        )
                    )

                    with col1:

                        render_html(
                            f"""
                            <div class="routine-name">
                                {safe_product}
                            </div>

                            <div class="routine-frequency">
                                {safe_category}
                                · Every
                                {product.replenish_every_weeks}
                                week(s)
                            </div>
                            """
                        )

                    with col2:

                        render_html(
                            f"""
                            <div class="tiny-label">
                                Next Replenishment
                            </div>

                            <div class="routine-value">
                                {
                                    product.next_replenish.strftime(
                                        "%B %d, %Y"
                                    )
                                }
                            </div>

                            <div class="routine-secondary">
                                Estimated cost:
                                ${product.estimated_cost:,.2f}
                            </div>
                            """
                        )

                    with col3:

                        render_html(
                            f"""
                            <div class="tiny-label">
                                Status
                            </div>

                            {status_html}
                            """
                        )

                    with col4:

                        render_html(
                            """
                            <div class="tiny-label">
                                Manage
                            </div>
                            """
                        )

                        if st.button(
                            "Edit",
                            key=f"edit_product_{product.id}",
                            use_container_width=True
                        ):

                            st.session_state.edit_product_id = (
                                product.id
                            )

                            st.rerun()

                        if st.button(
                            "Delete",
                            key=f"delete_product_{product.id}",
                            use_container_width=True
                        ):

                            repository.delete(
                                product.id
                            )

                            if (
                                st.session_state.edit_product_id
                                == product.id
                            ):

                                st.session_state.edit_product_id = (
                                    None
                                )

                            st.rerun()

    # =====================================================
    # EDIT PRODUCT
    # =====================================================

    if st.session_state.edit_product_id is not None:

        product_to_edit = repository.get_by_id(
            st.session_state.edit_product_id
        )

        if product_to_edit is None:

            st.session_state.edit_product_id = None

        else:

            safe_edit_product = escape(
                product_to_edit.product.title()
            )

            render_html(
                f"""
                <div class="luxury-rule"></div>

                <div class="section-kicker">
                    Modify Product
                </div>

                <div class="section-heading">
                    Edit {safe_edit_product}
                </div>

                <div class="section-copy">
                    Update this product and Nushluxe
                    will recalculate its replenishment date.
                </div>
                """
            )

            with st.form(
                "edit_product_form"
            ):

                edited_product = st.text_input(
                    "Product",
                    value=product_to_edit.product.title()
                )

                edited_category = st.text_input(
                    "Category",
                    value=product_to_edit.category.title()
                )

                edited_date = st.date_input(
                    "Last restocked",
                    value=product_to_edit.last_restocked,
                    max_value=date.today()
                )

                edited_frequency = st.number_input(
                    "Replenish every",
                    min_value=1,
                    value=int(
                        product_to_edit.replenish_every_weeks
                    ),
                    step=1,
                    help="Number of weeks"
                )

                edited_cost = st.number_input(
                    "Estimated cost",
                    min_value=0.0,
                    value=float(
                        product_to_edit.estimated_cost
                    ),
                    step=1.0,
                    format="%.2f"
                )

                edit_col1, edit_col2 = (
                    st.columns(2)
                )

                with edit_col1:

                    save_edit = (
                        st.form_submit_button(
                            "Save Changes",
                            use_container_width=True
                        )
                    )

                with edit_col2:

                    cancel_edit = (
                        st.form_submit_button(
                            "Cancel",
                            use_container_width=True
                        )
                    )

            if save_edit:

                if not edited_product.strip():

                    st.error(
                        "Please enter a product name."
                    )

                elif not edited_category.strip():

                    st.error(
                        "Please enter a category."
                    )

                else:

                    product_to_edit.update(
                        product=edited_product,
                        category=edited_category,
                        last_restocked=edited_date,
                        replenish_every_weeks=int(
                            edited_frequency
                        ),
                        estimated_cost=float(
                            edited_cost
                        )
                    )

                    repository.update(
                        product_to_edit
                    )

                    st.session_state.edit_product_id = None

                    st.rerun()

            if cancel_edit:

                st.session_state.edit_product_id = None

                st.rerun()

    # =====================================================
    # ADD PRODUCT
    # =====================================================

    with add_product_tab:

        render_html(
            """
            <div class="section-kicker">
                New Product
            </div>

            <div class="section-heading">
                Add to Your Bag
            </div>

            <div class="section-copy">
                Tell Nushluxe what you use, when you
                last restocked it, and how often you
                normally replenish it.
            </div>
            """
        )

        with st.form(
            "add_product_form",
            clear_on_submit=True
        ):

            product_name = st.text_input(
                "Product",
                placeholder=(
                    "Foundation, serum, shampoo..."
                )
            )

            category = st.text_input(
                "Category",
                placeholder=(
                    "Makeup, skincare, haircare..."
                )
            )

            last_restocked = st.date_input(
                "Last restocked",
                max_value=date.today()
            )

            replenish_every_weeks = st.number_input(
                "Replenish every",
                min_value=1,
                step=1,
                value=8,
                help="Number of weeks"
            )

            estimated_cost = st.number_input(
                "Estimated cost",
                min_value=0.0,
                step=1.0,
                value=0.0,
                format="%.2f"
            )

            submitted = (
                st.form_submit_button(
                    "Add Product",
                    use_container_width=True
                )
            )

        if submitted:

            if not product_name.strip():

                st.error(
                    "Please enter a product name."
                )

            elif not category.strip():

                st.error(
                    "Please enter a category."
                )

            else:

                new_product = Product(
                    product=product_name.strip().title(),
                    category=category.strip().title(),
                    last_restocked=last_restocked,
                    replenish_every_weeks=int(
                        replenish_every_weeks
                    ),
                    estimated_cost=float(
                        estimated_cost
                    )
                )

                repository.add(
                    new_product
                )

                st.rerun()