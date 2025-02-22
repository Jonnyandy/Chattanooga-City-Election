import sys
import traceback
import streamlit as st
from datetime import datetime
import pytz
import re
from utils.district_data import get_district_info, get_council_member
from utils.mapping import create_district_map, create_base_district_map
from utils.geocoding import validate_address, geocode_address
from streamlit_folium import st_folium
from pathlib import Path

print("Imported all required modules")

# Page configuration
try:
    print("Configuring page settings...")
    st.set_page_config(
        page_title="Find Your District | Chattanooga.Vote",
        page_icon="🗳️",
        layout="wide"
    )
    print("Page configuration completed")
except Exception as e:
    print(f"Error in page configuration: {str(e)}")
    print(traceback.format_exc())
    st.error("Error in page configuration. Please try refreshing the page.")

# Basic styling
try:
    print("Applying basic styling...")
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] > div:first-child {
                padding-top: 0;
            }
        </style>
    """, unsafe_allow_html=True)
    print("Basic styling applied")
except Exception as e:
    print(f"Error in styling: {str(e)}")
    print(traceback.format_exc())

# Initialize session state
try:
    print("Initializing session state...")
    if 'search_performed' not in st.session_state:
        st.session_state.search_performed = False
    if 'current_address' not in st.session_state:
        st.session_state.current_address = None
    if 'current_coords' not in st.session_state:
        st.session_state.current_coords = None
    if 'district_info' not in st.session_state:
        st.session_state.district_info = None
    print("Session state initialized")
except Exception as e:
    print(f"Error in session state initialization: {str(e)}")
    print(traceback.format_exc())

# Main content
try:
    st.title("Find Your District")
    st.markdown("Enter your address to find your city council district.")

    print("Creating layout...")
    col1, col2 = st.columns([2, 1])

    with col1:
        # Address form - always visible
        street_address = st.text_input(
            "Street Address",
            placeholder="123 Main St",
            help="Enter your street address",
            key="main_street_address"
        )

        # Validate ZIP code format
        def is_valid_zip(zip_code):
            return bool(re.match(r'^\d{5}$', zip_code))

        zip_code = st.text_input(
            "ZIP Code",
            placeholder="37405",
            help="Enter your 5-digit ZIP code",
            max_chars=5,
            key="main_zip_code"
        )

        # Search button
        if st.button("Find District", key="find_district_main", type="primary"):
            print("Find District button clicked")
            st.info("Search functionality is temporarily disabled for maintenance.")

        # Temporarily disable map display for debugging
        st.info("Map display is temporarily disabled for maintenance.")

except Exception as e:
    print(f"Critical error in main content: {str(e)}")
    print(traceback.format_exc())
    st.error("An unexpected error occurred. Please try again later.")

# Footer
try:
    st.markdown("---")
    st.markdown(
        "Data provided by City of Chattanooga. "
        "For official information, visit the [Election Commission website](https://elect.hamiltontn.gov/).",
        unsafe_allow_html=True
    )
except Exception as e:
    print(f"Error in footer: {str(e)}")
    print(traceback.format_exc())

print("My_Districts.py initialization completed.")