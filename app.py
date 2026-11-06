import streamlit as st
import tempfile
import shutil

from datetime import date
from pathlib import Path
from textwrap import dedent

from storage.json_repository import (
    JsonRoutineRepository,
    JsonProductRepository
)

from ui.maintenance_ui import render_maintenance
from ui.products_ui import render_products
from ui.planning_ui import render_planning_summary

from utils.data_setup import ensure_local_data_files


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NUSHLUXE",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# FILE LOCATIONS + SESSION DATA
# =========================================================

APP_FOLDER = Path(__file__).resolve().parent


def reset_demo_data_files(
    routine_data_file,
    product_data_file
):

    sample_folder = (
        APP_FOLDER / "sample_data"
    )

    sample_routines = (
        sample_folder
        / "sample_routines.json"
    )

    sample_products = (
        sample_folder
        / "sample_products.json"
    )

    routine_data_file = Path(
        routine_data_file
    )

    product_data_file = Path(
        product_data_file
    )

    routine_data_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    product_data_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy2(
        sample_routines,
        routine_data_file
    )

    shutil.copy2(
        sample_products,
        product_data_file
    )


if "demo_data_folder" not in st.session_state:

    st.session_state.demo_data_folder = (
        tempfile.mkdtemp(
            prefix="nushluxe_demo_"
        )
    )


SESSION_DATA_FOLDER = Path(
    st.session_state.demo_data_folder
)


ROUTINE_DATA_FILE = (
    SESSION_DATA_FOLDER
    / "nushluxe_data_v2.json"
)

PRODUCT_DATA_FILE = (
    SESSION_DATA_FOLDER
    / "nushluxe_products.json"
)


ensure_local_data_files(
    ROUTINE_DATA_FILE,
    PRODUCT_DATA_FILE
)


routine_repository = JsonRoutineRepository(
    ROUTINE_DATA_FILE
)

product_repository = JsonProductRepository(
    PRODUCT_DATA_FILE
)


# =========================================================
# HTML HELPER
# =========================================================

def render_html(content):
    st.html(
        dedent(content).strip()
    )


# =========================================================
# DESIGN
# =========================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=Inter:wght@300;400;500;600&display=swap');

    .stApp {
        background: #FFFFFF;
        color: #0A0A0A;
    }

    .block-container {
        max-width: 1220px;
        padding-top: 1.5rem;
        padding-bottom: 5rem;
    }

    html,
    body,
    [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .brand-eyebrow {
        text-align: center;
        font-size: 0.67rem;
        letter-spacing: 0.34em;
        text-transform: uppercase;
        color: #8A8A8A;
        margin-top: 1rem;
        margin-bottom: 1.2rem;
    }

    .nushluxe-logo {
        font-family: 'Bodoni Moda', 'Times New Roman', serif;
        text-align: center;
        font-size: clamp(4rem, 8vw, 7rem);
        line-height: 0.9;
        letter-spacing: -0.035em;
        font-weight: 400;
        color: #000000;
        margin: 0;
    }

    .brand-tagline {
        text-align: center;
        font-size: 0.78rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #5F5F5F;
        margin-top: 1.8rem;
    }

    .hero-copy {
        max-width: 620px;
        text-align: center;
        margin: 2.2rem auto 3rem auto;
        font-size: 1.05rem;
        font-weight: 300;
        line-height: 1.8;
        color: #666666;
    }

    .luxury-rule {
        height: 1px;
        background: #EAEAEA;
        width: 100%;
        margin: 2rem 0;
    }

    .section-kicker {
        font-size: 0.68rem;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: #969696;
        margin-bottom: 0.6rem;
    }

    .section-heading {
        font-family: 'Bodoni Moda', 'Times New Roman', serif;
        font-size: 2.6rem;
        font-weight: 400;
        letter-spacing: -0.02em;
        color: #111111;
        margin-bottom: 0.4rem;
    }

    .section-copy {
        color: #777777;
        font-size: 0.94rem;
        font-weight: 300;
        margin-bottom: 1.8rem;
    }

    .metric-box {
        min-height: 125px;
        border-top: 1px solid #111111;
        border-bottom: 1px solid #EAEAEA;
        padding: 1.2rem 0.2rem;
        margin-bottom: 1.6rem;
    }

    .metric-label {
        font-size: 0.63rem;
        letter-spacing: 0.21em;
        color: #8B8B8B;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .metric-value {
        font-family: 'Bodoni Moda', 'Times New Roman', serif;
        font-size: 2.5rem;
        line-height: 1;
        color: #111111;
    }

    .metric-subtext {
        color: #9A9A9A;
        font-size: 0.78rem;
        margin-top: 0.55rem;
    }

    .routine-name {
        font-family: 'Bodoni Moda', 'Times New Roman', serif;
        font-size: 2rem;
        font-weight: 400;
        letter-spacing: -0.025em;
        color: #111111;
        line-height: 1;
        margin-bottom: 0.55rem;
    }

    .routine-frequency {
        color: #8A8A8A;
        font-size: 0.78rem;
        letter-spacing: 0.04em;
    }

    .tiny-label {
        color: #A0A0A0;
        font-size: 0.62rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin-bottom: 0.55rem;
    }

    .routine-value {
        color: #111111;
        font-size: 0.95rem;
        font-weight: 400;
    }

    .routine-secondary {
        color: #989898;
        font-size: 0.75rem;
        margin-top: 0.35rem;
    }

    .status-pill {
        display: inline-block;
        padding: 0.42rem 0.72rem;
        font-size: 0.63rem;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        border-radius: 100px;
    }

    .status-upcoming {
        background: #F5F5F5;
        border: 1px solid #E5E5E5;
        color: #222222;
    }

    .status-due {
        background: #F7EFF0;
        border: 1px solid #EADBDD;
        color: #4C3E41;
    }

    .status-overdue {
        background: #111111;
        border: 1px solid #111111;
        color: #FFFFFF;
    }

    .blush-strip {
        background: #FAF5F5;
        border: 1px solid #F3EAEA;
        padding: 1.8rem 2rem;
        margin: 2rem 0 2.5rem 0;
    }

    .blush-label {
        color: #8A7377;
        font-size: 0.65rem;
        letter-spacing: 0.23em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .blush-heading {
        font-family: 'Bodoni Moda', 'Times New Roman', serif;
        font-size: 1.8rem;
        color: #201A1B;
        margin-bottom: 0.3rem;
    }

    .blush-copy {
        color: #806F72;
        font-size: 0.9rem;
        font-weight: 300;
    }

    div[data-testid="stForm"] {
        background: #FFFFFF;
        border: 1px solid #E7E7E7;
        border-radius: 0px;
        padding: 2rem;
        box-shadow: none;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input {
        background: #FFFFFF !important;
        border: 1px solid #D8D8D8 !important;
        border-radius: 0px !important;
        color: #111111 !important;
        min-height: 46px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #111111 !important;
        border-radius: 0px !important;
        min-height: 43px;
        font-size: 0.72rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase;
        font-weight: 500 !important;
        box-shadow: none !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #111111 !important;
    }

    button[data-baseweb="tab"] {
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #8A8A8A;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #111111;
    }

    div[data-testid="stAlert"] {
        border-radius: 0px !important;
    }

    @media (max-width: 700px) {

        .nushluxe-logo {
            font-size: 4rem;
        }

        .section-heading {
            font-size: 2rem;
        }

        .block-container {
            padding-left: 1.2rem;
            padding-right: 1.2rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DEMO CONTROLS
# =========================================================

st.warning(
    "Demo version — your session uses temporary data. "
    "Refreshing the page starts a new blank session. "
    "Don't enter personal information."
)


reset_column, feedback_column = st.columns(2)


with reset_column:

    if st.button(
        "Reset demo data",
        key="reset_demo_data"
    ):

        reset_demo_data_files(
            ROUTINE_DATA_FILE,
            PRODUCT_DATA_FILE
        )

        st.rerun()


with feedback_column:

    st.link_button(
        "Share feedback",
        "https://forms.gle/SGgN5J7HYzJqoTuPA"
    )


# =========================================================
# BRAND
# =========================================================

render_html(
    """
    <div class="brand-eyebrow">
        Personal Maintenance Intelligence
    </div>

    <div class="nushluxe-logo">
        NUSHLUXE
    </div>

    <div class="brand-tagline">
        Beauty & Wellness Maintenance OS
    </div>

    <div class="hero-copy">
        A refined system for organizing your recurring
        maintenance and the products that support it.
    </div>

    <div class="luxury-rule"></div>
    """
)


# =========================================================
# MAINTENANCE DASHBOARD DATA
# =========================================================

maintenance_schedule = (
    routine_repository.list_all()
)

maintenance_schedule.sort(
    key=lambda routine: routine.next_due
)

total_routines = len(
    maintenance_schedule
)

overdue_count = sum(
    1
    for routine in maintenance_schedule
    if routine.status == "OVERDUE"
)

upcoming_count = sum(
    1
    for routine in maintenance_schedule
    if routine.status == "UPCOMING"
)

future_or_today = [
    routine
    for routine in maintenance_schedule
    if routine.next_due >= date.today()
]

if future_or_today:

    nearest_routine = min(
        future_or_today,
        key=lambda routine: routine.next_due
    )

    nearest_text = (
        nearest_routine.next_due.strftime(
            "%b %d"
        )
    )

else:

    nearest_text = "—"


# =========================================================
# METRICS
# =========================================================

metric1, metric2, metric3, metric4 = (
    st.columns(4)
)

with metric1:

    render_html(
        f"""
        <div class="metric-box">

            <div class="metric-label">
                Total Rituals
            </div>

            <div class="metric-value">
                {total_routines}
            </div>

            <div class="metric-subtext">
                In your maintenance system
            </div>

        </div>
        """
    )


with metric2:

    render_html(
        f"""
        <div class="metric-box">

            <div class="metric-label">
                Upcoming
            </div>

            <div class="metric-value">
                {upcoming_count}
            </div>

            <div class="metric-subtext">
                Currently on schedule
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
                {overdue_count}
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
                Next Due
            </div>

            <div class="metric-value">
                {nearest_text}
            </div>

            <div class="metric-subtext">
                Closest maintenance date
            </div>

        </div>
        """
    )


# =========================================================
# NUSHLUXE MESSAGE
# =========================================================

render_html(
    """
    <div class="blush-strip">

        <div class="blush-label">
            Nushluxe Intelligence
        </div>

        <div class="blush-heading">
            Your maintenance, made visible.
        </div>

        <div class="blush-copy">
            Your services and products are becoming
            one structured personal maintenance system.
        </div>

    </div>
    """
)


# =========================================================
# MAIN MODULE NAVIGATION
# =========================================================

render_planning_summary(
    routine_repository,
    product_repository
)

st.markdown("---")

maintenance_section, products_section = st.tabs(
    [
        "Maintenance",
        "Products"
    ]
)


with maintenance_section:

    render_maintenance(
        routine_repository
    )


with products_section:

    render_products(
        product_repository
    )


# =========================================================
# FOOTER
# =========================================================

render_html(
    """
    <div class="luxury-rule"></div>

    <div style="
        text-align:center;
        font-size:0.62rem;
        letter-spacing:0.2em;
        text-transform:uppercase;
        color:#AAAAAA;
        padding-top:1rem;
        padding-bottom:2rem;
    ">
        NUSHLUXE · PERSONAL MAINTENANCE INTELLIGENCE
    </div>
    """
)