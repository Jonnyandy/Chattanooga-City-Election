import streamlit as st
from datetime import datetime, timezone
from streamlit_folium import st_folium
from utils.geocoding import validate_address, geocode_address
from utils.district_data import get_district_info, get_council_member
from utils.mapping import create_district_map, create_base_district_map
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Find Your District | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to ensure the title appears above navigation
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

# Early Voting Information moved to sidebar
with st.sidebar.expander("Early Voting Information", expanded=False):
    st.markdown("**Early Voting Period:** February 12 – February 27, 2025")
    st.markdown("*ALL LOCATIONS CLOSED MONDAY, FEBRUARY 17TH, FOR PRESIDENTS DAY*")
    st.markdown("**Early Voting Locations:**")
    st.markdown("""
    1. **Election Commission**  
       700 River Terminal Rd, Chattanooga, TN 37406  
       *Monday - Friday: 8:00 am – 7:00 pm*  
       *Saturday: 8:00 am – 4:00 pm*  

    2. **Hixson Community Center**  
       5401 School Dr, Hixson, TN 37343  
       *Monday - Friday: 10:00 am – 6:00 pm*  
       *Saturday: 10:00 am – 4:00 pm*

    3. **Chris L. Ramsey Sr. Community Center**  
       1010 N Moore Rd, Chattanooga, TN 37411  
       *Monday - Friday: 10:00 am – 6:00 pm*  
       *Saturday: 10:00 am – 4:00 pm*
    """)

with st.sidebar.expander("Check Registration", expanded=False):
    st.markdown("""
    ### Verify Your Voter Registration

    To check if you're registered to vote in the March 4th, 2025 election, visit the official Tennessee voter lookup tool:

    [Click here to verify your registration ↗](https://tnmap.tn.gov/voterlookup/)

    **Requirements:**
    • Valid TN Photo ID
    • Must be 18+ by election day
    • Chattanooga resident

    **Need to register or update your information?**  
    Visit [GoVoteTN.gov](https://govotetn.gov)
    """)

st.sidebar.markdown("---")
with st.sidebar.expander("❓ Need Help?", expanded=True):
    st.markdown("""
    **Election Commission:**
    📞 (423) 493-5100
    📧 vote@hamiltontn.gov
    """)

with st.sidebar.expander("🤝 Become a Poll Worker", expanded=False):
    st.markdown("""
    Poll officials get a stipend of $135 - $175 per election.  
    Sign up at [elect.hamiltontn.gov/pollworker](http://elect.hamiltontn.gov/pollworker)
    """)
# Add title and attribution to sidebar
st.sidebar.markdown("""
    <div style='text-align: center; padding-top: 0; margin-bottom: 20px;'>
        <h1 style='color: #1B4E5D; margin-bottom: 5px;'>chattanooga.vote</h1>
        <div style='margin: 20px 0;'>
            <div style='text-align: center; margin-bottom: 10px;'>
                <img src='assets/chattanoogashow_jonathanholborn.png' style='max-width: 400px; height: auto;' alt='The Chattanooga Show and Jonathan Holborn'>
            </div>
            <!-- Placeholder for Jonathan Holborn logo -->
            <div style='background-color: #f0f0f0; padding: 20px; margin-bottom: 10px; border-radius: 5px;'>
                [Jonathan Holborn Logo]
            </div>
        </div>
        <p style='font-style: italic; color: #666;'>
            Brought to you by<br>
            The Chattanooga Show<br>
            and Jonathan Holborn
        </p>
    </div>
    <hr>
""", unsafe_allow_html=True)
# Election countdown
election_date = datetime(2025, 3, 4, tzinfo=timezone.utc)
current_time = datetime.now(timezone.utc)
time_until_election = election_date - current_time

days = time_until_election.days
hours = time_until_election.seconds // 3600
minutes = (time_until_election.seconds % 3600) // 60

st.markdown(
    f"""
    <div style="background-color: #1B4E5D; color: white; padding: 10px; text-align: center; border-radius: 5px; margin-bottom: 20px;">
         {days} days until Election Day:
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

    zip_code = st.text_input(
        "ZIP Code",
        placeholder="37405",
        help="Enter your ZIP code",
        max_chars=5,
        key="main_zip_code"
    )

    # Search button
    if st.button("Find District", key="find_district_main", type="primary"):
        if street_address and zip_code:
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

    # Map display
    st.subheader("Chattanooga City Council Districts")
    if not st.session_state.search_performed:
        m = create_base_district_map()
        map_data = st_folium(m, width=None, height=400, key="base_map")

    # Show map if search is performed
    if st.session_state.search_performed and st.session_state.current_coords:
        lat, lon = st.session_state.current_coords
        district_info = st.session_state.district_info

        if district_info and district_info["district_number"] != "District not found":
            m = create_district_map(lat, lon, district_info)
            map_key = f"map_{st.session_state.current_address}"
            map_data = st_folium(m, width=None, height=350, key=map_key)

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

                    # If we have candidate photos
                    photo_path = f"assets/candidate_photos/{candidate.split('[')[0].strip()}.jpg"
                    if Path(photo_path).exists():
                        st.image(photo_path, use_column_width=True)

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