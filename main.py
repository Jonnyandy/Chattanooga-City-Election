import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.geocoding import validate_address, geocode_address
from utils.district_data import get_district_info, get_council_member
from utils.mapping import create_district_map, create_base_district_map
from datetime import datetime, timezone

# Page configuration
st.set_page_config(
    page_title="Chattanooga Voting Information",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header
st.title("🗳️ Chattanooga Voting Information")

# Election Day Countdown
election_date = datetime(2025, 3, 4, 19, 0, 0, tzinfo=timezone.utc)  # 7 PM UTC (2 PM EST)
now = datetime.now(timezone.utc)
time_until_election = election_date - now

if time_until_election.total_seconds() > 0:
    days = time_until_election.days
    hours = time_until_election.seconds // 3600
    minutes = (time_until_election.seconds % 3600) // 60

    st.markdown("""
    <div style='padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem; margin-bottom: 1rem;'>
        <h3 style='text-align: center; margin: 0;'>⏱️ Election Day Countdown</h3>
        <p style='text-align: center; font-size: 1.5rem; margin: 0.5rem 0;'>
            <strong>{} days, {} hours, {} minutes</strong><br>
            <span style='font-size: 1rem;'>until March 4th, 2025 Election Day</span>
        </p>
    </div>
    """.format(days, hours, minutes), unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem; margin-bottom: 1rem;'>
        <h3 style='text-align: center; color: #ff4b4b;'>🗳️ Election Day is Here!</h3>
        <p style='text-align: center;'>Polls are open until 7:00 PM EST</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
Find your voting district by entering your address below. 
This tool uses official City of Chattanooga district boundaries.
""")

# Main content
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("Find Your District")
    address = st.text_input(
        "Enter your street address and ZIP code",
        placeholder="123 Main St 37402",
        help="Enter your complete street address including ZIP code to find your district.",
        key="address_input"
    )

    # Always show the base district map
    if not address:
        st.subheader("Chattanooga City Council Districts")
        m = create_base_district_map()
        map_data = st_folium(m, width=None, height=500)
    else:
        # Process address if entered
        if validate_address(address):
            coords = geocode_address(address)
            if coords:
                lat, lon = coords
                district_info = get_district_info(lat, lon)

                if district_info["district_number"] != "District not found":
                    m = create_district_map(lat, lon, district_info)
                    map_data = st_folium(m, width=None, height=500)

                    # Display district information
                    st.subheader("Your District Information")
                    council_info = get_council_member(district_info["district_number"])

                    info_col1, info_col2 = st.columns(2)
                    with info_col1:
                        st.markdown(f"**District:** {district_info['district_number']}")
                        st.markdown(f"**Current Council Member:** {council_info['name']}")

                        # Add March 4th Election Candidates
                        if district_info.get('candidates'):
                            st.markdown("---")
                            st.markdown("**March 4th, 2025 Election Candidates:**")
                            for candidate in district_info['candidates']:
                                st.markdown(f"• {candidate}")
                        else:
                            st.markdown("---")
                            st.markdown("*No candidate information available for this district*")

                    with info_col2:
                        if district_info.get('district_description'):
                            st.markdown(f"**Area:** {district_info['district_description']}")

                    # Add polling location information
                    st.subheader("Your Polling Location")
                    if district_info["polling_place"] != "Not found":
                        st.markdown(f"""
                        **Location:** {district_info["polling_place"]}  
                        **Address:** {district_info["polling_address"]}  
                        **Precinct:** {district_info["precinct"]}
                        """)
                    else:
                        st.warning("Polling location information not available for this address. Please contact the Election Commission for assistance.")

                else:
                    st.error(
                        "Unable to determine your district. This may mean your address is "
                        "outside the Chattanooga city limits. Please verify your address "
                        "or contact the Election Commission for assistance."
                    )
                    m = create_base_district_map()
                    map_data = st_folium(m, width=None, height=500)
            else:
                st.error("Unable to locate your address. Please check the format and try again.")
                m = create_base_district_map()
                map_data = st_folium(m, width=None, height=500)
        else:
            st.error(
                "Please enter a valid Chattanooga address in the format:\n"
                "'123 Main St 37402'\n\n"
                "Include:\n"
                "- Street number\n"
                "- Street name\n"
                "- ZIP code"
            )
            m = create_base_district_map()
            map_data = st_folium(m, width=None, height=500)

with col2:
    st.subheader("Helpful Information")

    # Early Voting Info in sidebar
    with st.expander("🗳️ Early Voting Details", expanded=True):
        st.markdown("""
        **Early Voting Period:** February 12 – February 27, 2025  
        *ALL LOCATIONS CLOSED MONDAY, FEBRUARY 17TH, FOR PRESIDENTS DAY*

        **Early Voting Locations:**

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

        **Important Notes:**
        - Only eligible voters who reside in the City of Chattanooga may participate
        - PHOTO ID ISSUED BY STATE OF TN OR FEDERAL GOVT REQUIRED TO VOTE
        - Visit [govotetn.gov](http://govotetn.gov) to update your information
        """)

    with st.expander("📮 Valid ZIP Codes", expanded=False):
        st.markdown("""
        Chattanooga ZIP codes include:
        - 37401-37412
        - 37415, 37416
        - 37419, 37421
        - 37450, 37351
        """)

    with st.expander("🤝 Become a Poll Worker", expanded=False):
        st.markdown("""
        Poll officials get a stipend of $135 - $175 per election.  
        Sign up at [elect.hamiltontn.gov/pollworker](http://elect.hamiltontn.gov/pollworker)
        """)

    with st.expander("❓ Need Help?", expanded=False):
        st.markdown("""
        **Contact the Hamilton County Election Commission:**
        - Phone: (423) 493-5100
        - Email: vote@hamiltontn.gov
        """)

# Footer
st.markdown("---")
st.markdown(
    "Data provided by City of Chattanooga. "
    "For official information, visit the [Election Commission website](https://elect.hamiltontn.gov/).",
    unsafe_allow_html=True
)