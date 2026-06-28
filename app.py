import streamlit as st
from streamlit_option_menu import option_menu
from utils.styles import apply_styles

st.set_page_config(
    page_title="Traffic Sign Recognition AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_styles(st)

# Session state for navigation
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home"

pages = ["Home", "About", "Detection", "Analytics", "Contact"]

selected = option_menu(
    menu_title=None,
    options=pages,
    icons=["house", "info-circle", "camera", "bar-chart", "person"],
    orientation="horizontal",
    default_index=pages.index(st.session_state.selected_page)
)

st.session_state.selected_page = selected

if selected == "Home":
    from sections.home import show
    show()

elif selected == "About":
    from sections.about import show
    show()

elif selected == "Detection":
    from sections.detection import show
    show()

elif selected == "Analytics":
    from sections.analytics import show
    show()

elif selected == "Contact":
    from sections.contact import show
    show()