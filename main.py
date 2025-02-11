import streamlit as st

# Redirect to Find Your District page
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide"
)

# Use JavaScript to redirect to the Find Your District page
components.html(
    """
    <script>
        window.location.href = "1_Find_Your_District";
    </script>
    """,
    height=0
)