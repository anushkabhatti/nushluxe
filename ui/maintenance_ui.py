import streamlit as st

from datetime import date
from html import escape
from textwrap import dedent

from core.maintenance import Routine
from utils.dates import get_days_text


def render_html(content):
    st.html(
        dedent(content).strip()
    )


def render_maintenance(repository):

    maintenance_schedule = repository.list_all()

    maintenance_schedule.sort(
        key=lambda routine: routine.next_due
    )

    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None

    schedule_tab, add_tab = st.tabs(
        [
            "Schedule",
            "Add Routine"
        ]
    )

    # =====================================================
    # SCHEDULE
    # =====================================================

    with schedule_tab:

        render_html(
            """
            <div class="section-kicker">
                Maintenance
            </div>

            <div class="section-heading">
                Your Schedule
            </div>

            <div class="section-copy">
                A chronological view of your recurring
                beauty and wellness maintenance.
            </div>
            """
        )

        if not maintenance_schedule:

            st.info(
                "Your maintenance schedule is empty."
            )

        else:

            for routine in maintenance_schedule:

                safe_service = escape(
                    routine.service.title()
                )

                days_text = get_days_text(
                    routine.next_due
                )

                if routine.status == "OVERDUE":

                    status_html = """
                    <span class="status-pill status-overdue">
                        Overdue
                    </span>
                    """

                elif routine.status == "DUE TODAY":

                    status_html = """
                    <span class="status-pill status-due">
                        Due Today
                    </span>
                    """

                else:

                    status_html = """
                    <span class="status-pill status-upcoming">
                        Upcoming
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
                                {safe_service}
                            </div>

                            <div class="routine-frequency">
                                Every {routine.frequency_weeks} week(s)
                            </div>
                            """
                        )

                    with col2:

                        render_html(
                            f"""
                            <div class="tiny-label">
                                Next Due
                            </div>

                            <div class="routine-value">
                                {
                                    routine.next_due.strftime(
                                        "%B %d, %Y"
                                    )
                                }
                            </div>

                            <div class="routine-secondary">
                                {days_text}
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
                            key=f"edit_{routine.id}",
                            use_container_width=True
                        ):

                            st.session_state.edit_id = (
                                routine.id
                            )

                            st.rerun()

                        if st.button(
                            "Delete",
                            key=f"delete_{routine.id}",
                            use_container_width=True
                        ):

                            repository.delete(
                                routine.id
                            )

                            if (
                                st.session_state.edit_id
                                == routine.id
                            ):

                                st.session_state.edit_id = (
                                    None
                                )

                            st.rerun()

    # =====================================================
    # EDIT
    # =====================================================

    if st.session_state.edit_id is not None:

        routine_to_edit = repository.get_by_id(
            st.session_state.edit_id
        )

        if routine_to_edit is None:

            st.session_state.edit_id = None

        else:

            safe_edit_service = escape(
                routine_to_edit.service.title()
            )

            render_html(
                f"""
                <div class="luxury-rule"></div>

                <div class="section-kicker">
                    Modify
                </div>

                <div class="section-heading">
                    Edit {safe_edit_service}
                </div>

                <div class="section-copy">
                    Update the details of this routine
                    and Nushluxe will recalculate its schedule.
                </div>
                """
            )

            with st.form(
                "edit_routine_form"
            ):

                edited_service = st.text_input(
                    "Service",
                    value=(
                        routine_to_edit.service.title()
                    )
                )

                edited_date = st.date_input(
                    "Last completed",
                    value=(
                        routine_to_edit.last_completed
                    ),
                    max_value=date.today()
                )

                edited_frequency = st.number_input(
                    "Frequency in weeks",
                    min_value=1,
                    value=int(
                        routine_to_edit.frequency_weeks
                    ),
                    step=1
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

                if not edited_service.strip():

                    st.error(
                        "Please enter a service name."
                    )

                else:

                    routine_to_edit.update(
                        service=edited_service,
                        last_completed=edited_date,
                        frequency_weeks=int(
                            edited_frequency
                        )
                    )

                    repository.update(
                        routine_to_edit
                    )

                    st.session_state.edit_id = None

                    st.rerun()

            if cancel_edit:

                st.session_state.edit_id = None

                st.rerun()

    # =====================================================
    # ADD
    # =====================================================

    with add_tab:

        render_html(
            """
            <div class="section-kicker">
                New Ritual
            </div>

            <div class="section-heading">
                Add to Nushluxe
            </div>

            <div class="section-copy">
                Tell Nushluxe when you last completed a
                service and how often you repeat it.
                Your next maintenance date will be
                calculated automatically.
            </div>
            """
        )

        with st.form(
            "add_routine_form",
            clear_on_submit=True
        ):

            service = st.text_input(
                "Service",
                placeholder=(
                    "Hair, facial, manicure, brows..."
                )
            )

            last_completed = st.date_input(
                "Last completed",
                max_value=date.today()
            )

            frequency_weeks = st.number_input(
                "Repeat every",
                min_value=1,
                step=1,
                value=4,
                help="Number of weeks"
            )

            submitted = (
                st.form_submit_button(
                    "Add to Nushluxe",
                    use_container_width=True
                )
            )

        if submitted:

            if not service.strip():

                st.error(
                    "Please enter a service name."
                )

            else:

                new_routine = Routine(
                    service=service.strip().title(),
                    last_completed=last_completed,
                    frequency_weeks=int(
                        frequency_weeks
                    )
                )

                repository.add(
                    new_routine
                )

                st.rerun()