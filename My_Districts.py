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
        # Address form
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
            if street_address and zip_code:
                if not is_valid_zip(zip_code):
                    st.error("Please enter a valid 5-digit ZIP code")
                else:
                    print("Processing address search...")
                    address = f"{street_address}, {zip_code}"

                    try:
                        if validate_address(address):
                            coords = geocode_address(address)

                            if coords:
                                st.session_state.search_performed = True
                                st.session_state.current_address = address
                                st.session_state.current_coords = coords
                                lat, lon = coords
                                st.session_state.district_info = get_district_info(lat, lon)
                            else:
                                st.error("Unable to locate this address. Please check the format and try again.")
                        else:
                            st.error("Please enter a valid Chattanooga address with ZIP code")
                    except Exception as e:
                        print(f"Error during address processing: {str(e)}")
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.error("Please enter both street address and ZIP code")

        MAP_HEIGHT = 400

        print("Initializing map display...")
        # Show base map if no search performed
        if not st.session_state.search_performed:
            try:
                m = create_base_district_map()
                st_folium(m, width=None, height=MAP_HEIGHT)
            except Exception as e:
                print(f"Error creating base map: {str(e)}")
                st.error("Unable to load the district map at this time.")

        # Show detailed map if search is performed
        if st.session_state.search_performed and st.session_state.current_coords:
            try:
                lat, lon = st.session_state.current_coords
                district_info = st.session_state.district_info

                if district_info and district_info["district_number"] != "District not found":
                    m = create_district_map(lat, lon, district_info)
                    map_key = f"map_{st.session_state.current_address}"
                    st_folium(m, width=None, height=MAP_HEIGHT, key=map_key)

                    # Display district information
                    st.markdown(f"### Your district is District {district_info['district_number']}")

                    # Current Council Member
                    council_info = get_council_member(district_info["district_number"])
                    st.markdown("#### Current Council Member")
                    st.markdown(f"**{council_info['name']}**")
            except Exception as e:
                print(f"Error displaying search results: {str(e)}")
                st.error("Unable to display district information at this time.")

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