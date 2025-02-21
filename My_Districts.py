import streamlit as st
from datetime import datetime
import pytz
from utils.district_data import get_district_info, get_council_member
from utils.mapping import create_district_map, create_base_district_map
from streamlit_folium import st_folium
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Find Your District | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide"
)

# Basic styling
st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'current_address' not in st.session_state:
    st.session_state.current_address = None
if 'current_coords' not in st.session_state:
    st.session_state.current_coords = None
if 'district_info' not in st.session_state:
    st.session_state.district_info = None

# Main content
st.title("Find Your District")
st.markdown("Enter your address to find your city council district.")

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
        if street_address and zip_code:
            if not is_valid_zip(zip_code):
                st.error("Please enter a valid 5-digit ZIP code")
            else:
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
                    st.error(f"An error occurred: {e}")


        else:
            st.error("Please enter both street address and ZIP code")

    MAP_HEIGHT = 400

    # Basic map display
    if not st.session_state.search_performed:
        m = create_base_district_map()
        st_folium(m, width=None, height=MAP_HEIGHT)

    # Show map if search is performed
    if st.session_state.search_performed and st.session_state.current_coords:
        lat, lon = st.session_state.current_coords
        district_info = st.session_state.district_info

        if district_info and district_info["district_number"] != "District not found":
            m = create_district_map(lat, lon, district_info)
            map_key = f"map_{st.session_state.current_address}"
            st_folium(m, width=None, height=MAP_HEIGHT, key=map_key)

            # Display district information below map
            st.markdown(f"### Your district is District {district_info['district_number']}")

            # Current Council Member
            council_info = get_council_member(district_info["district_number"])
            st.markdown("#### Current Council Member")
            st.markdown(f"**{council_info['name']}**")

# Footer
st.markdown("---")
st.markdown(
    "Data provided by City of Chattanooga. "
    "For official information, visit the [Election Commission website](https://elect.hamiltontn.gov/).",
    unsafe_allow_html=True
)