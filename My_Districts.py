import streamlit as st
from datetime import datetime, timezone
from streamlit_folium import st_folium
from utils.geocoding import validate_address, geocode_address
from utils.district_data import get_district_info, get_council_member
from utils.mapping import create_district_map, create_base_district_map
from pathlib import Path
import re
import pytz

# Page configuration remains unchanged
st.set_page_config(
    page_title="Find Your District | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide",
    
)

# CSS remains unchanged through line 123
st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0;
        }
       
        div[data-testid="stSidebarUserContent"] {
            padding-top: 0;            
        } 
        div[data-testid="stSidebarNav"] {
            margin-top: 20px;
        }
        .sidebar-content {
            margin-top: 0;
            padding-top: 0;
        }
        button[kind="header"] {
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)


# Set sidebar title for the district finder
st.sidebar.title("Find Your District")

# Initialize session state variables
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'current_address' not in st.session_state:
    st.session_state.current_address = None
if 'current_coords' not in st.session_state:
    st.session_state.current_coords = None
if 'district_info' not in st.session_state:
    st.session_state.district_info = None


# Add title and attribution to sidebar

st.sidebar.markdown("""
<hr>
    <div style='text-align: center; padding-top: 0; margin-bottom: 10px;'>
        <h1 style='color: #1B4E5D; margin-bottom: 5px;'>chattanooga.vote</h1>
    </div>
    
""", unsafe_allow_html=True)
st.sidebar.image('assets/chattanoogashow_jonathanholborn.png', width=320)
# Add attribution to sidebar
st.sidebar.markdown("""
    
    <div style='text-align: center; padding-top: 0; margin-bottom: 10px;'>
    <p style='font-style: italic; color: #666;'>
        Brought to you by<br>
        <a href="https://www.instagram.com/chattanoogashow/" target="_blank">The Chattanooga Show</a><br>
        &
        <a href="https://jonathanholborn.com" target="_blank">Jonathan Holborn</a>
    </p>
    </div>
""", unsafe_allow_html=True)


# Election countdown with local timezone
election_date = datetime(2025, 3, 4, tzinfo=pytz.timezone('America/New_York'))
current_time = datetime.now(pytz.timezone('America/New_York'))
time_until_election = election_date - current_time

days = time_until_election.days
hours = time_until_election.seconds // 3600
minutes = (time_until_election.seconds % 3600) // 60

st.markdown(
    f"""
    <div style="background-color: #1B4E5D; color: white; padding: 10px; text-align: center; border-radius: 5px; margin-bottom: 20px;">
         {days} days until Election Day: March 4th, 2025
    </div>
    """,
    unsafe_allow_html=True
)

# Main content area
st.title("Chattanooga Council Elections")

st.markdown("""
Find your city council district by entering your address below. 
This tool uses official City of Chattanooga district boundaries.
""")

# Main content
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

                if validate_address(address):
                    coords = geocode_address(address)

                    if coords:
                        st.session_state.search_performed = True
                        st.session_state.current_address = address
                        st.session_state.current_coords = coords
                        lat, lon = coords
                        district_info = get_district_info(lat, lon)
                        st.session_state.district_info = district_info
                    else:
                        st.error("Unable to locate this address. Please check the format and try again.")
                else:
                    st.error("Please enter a valid Chattanooga address with ZIP code")
        else:
            st.error("Please enter both street address and ZIP code")

    # Map display with consistent height
    MAP_HEIGHT = 400  # Consistent height for all maps

    st.subheader("Chattanooga City Council Districts")
    if not st.session_state.search_performed:
        m = create_base_district_map()
        map_data = st_folium(m, width=None, height=MAP_HEIGHT, key="base_map")

    # Show map if search is performed
    if st.session_state.search_performed and st.session_state.current_coords:
        lat, lon = st.session_state.current_coords
        district_info = st.session_state.district_info

        if district_info and district_info["district_number"] != "District not found":
            m = create_district_map(lat, lon, district_info)
            map_key = f"map_{st.session_state.current_address}"
            map_data = st_folium(m, width=None, height=MAP_HEIGHT, key=map_key)

            # Display district information below map
            st.subheader("District Information")
            st.markdown(f"### Your district is District {district_info['district_number']}")

            # Current Council Member
            council_info = get_council_member(district_info["district_number"])
            st.markdown("#### Current Council Member")
            st.markdown(f"**{council_info['name']}**")

            # Election Information
            st.markdown("---")
            st.markdown("### March 4th, 2025 Election Candidates")

            for candidate in district_info.get('candidates', []):
                with st.container():
                    st.markdown('<div class="candidate-info">', unsafe_allow_html=True)

                    # Handle candidate name and website if present
                    if "[" in candidate:
                        name = candidate.split("[")[0].strip()
                        website = candidate.split("(")[1].split(")")[0]
                        st.markdown(f'<div class="candidate-name">{name}</div>', unsafe_allow_html=True)
                        st.markdown(f'[Campaign Website]({website})', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="candidate-name">{candidate}</div>', unsafe_allow_html=True)

                    # Safe image loading with error handling
                    try:
                        photo_path = Path(f"assets/candidate_photos/{candidate.split('[')[0].strip()}.jpg")
                        if photo_path.exists():
                            st.image(str(photo_path), use_column_width=True)
                    except Exception as e:
                        st.warning("Unable to load candidate photo")

                    st.markdown('</div>', unsafe_allow_html=True)

            # Polling Location Information
            if district_info["polling_place"] != "Not found":
                st.markdown("---")
                st.markdown("### 🏢 Your Polling Location")
                st.markdown(f"""
                **Location:** {district_info["polling_place"]}  
                **Address:** {district_info["polling_address"]}  
                **Precinct:** {district_info["precinct"]}
                """)

# Footer
st.markdown("---")
st.markdown(
    "Data provided by City of Chattanooga. "
    "For official information, visit the [Election Commission website](https://elect.hamiltontn.gov/).",
    unsafe_allow_html=True
)