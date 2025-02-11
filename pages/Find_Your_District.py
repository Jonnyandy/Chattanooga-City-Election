import streamlit as st
import folium
from datetime import datetime, timezone
from streamlit_folium import st_folium
from utils.geocoding import validate_address, geocode_address
from utils.district_data import get_district_info, get_council_member, get_district_candidates
from utils.mapping import create_district_map, create_base_district_map
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Find Your District | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("Quick Links")
st.sidebar.markdown("---")

# Early Voting Information moved to sidebar
with st.sidebar.expander("Early Voting Information", expanded=False):
    st.markdown("**Early Voting Period:** February 12 – February 27, 2025")
    # Rest of the file content remains the same
