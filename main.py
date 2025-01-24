import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.geocoding import validate_address, geocode_address
from utils.district_data import get_district_info, get_council_member
from utils.mapping import create_district_map, create_base_district_map
from utils.voter_verification import verify_voter_registration
from datetime import datetime, timezone, timedelta

# Page configuration
st.set_page_config(
    page_title="Chattanooga Voting Information",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS
with open('styles/custom.css') as f:
    css = f.read()

st.markdown(f"""
    <style>
        {css}
    </style>
""", unsafe_allow_html=True)

# Election Day Countdown
election_date = datetime(2025, 3, 4, 14, 0, 0, tzinfo=timezone(timedelta(hours=-5)))  # 2 PM Eastern
now = datetime.now(timezone(timedelta(hours=-5)))  # Eastern time
time_until_election = election_date - now

if time_until_election.total_seconds() > 0:
    days = time_until_election.days
    countdown_text = f"⏱️ {days} days until Election Day"
else:
    countdown_text = "🗳️ Election Day - Polls open until 7:00 PM EST"

# Header with countdown
st.markdown(f'<div class="header-countdown">{countdown_text}</div>', unsafe_allow_html=True)
st.title("🗳️ Chattanooga.Vote")

st.markdown("""
Find your city council district by entering your address below. 
This tool uses official City of Chattanooga district boundaries.
""")

# Main content
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("Find Your District")
    
    col_addr, col_zip = st.columns([2, 1])
    with col_addr:
        street_address = st.text_input(
            "Street Address",
            placeholder="123 Main St",
            help="Enter your street address",
            key="street_input"
        )
    with col_zip:
        zip_code = st.text_input(
            "ZIP Code",
            placeholder="37402",
            help="Enter your ZIP code (5 digits)",
            key="zip_input",
            max_chars=5
        )
    
    # Validate inputs
    is_valid_street = bool(street_address.strip())
    is_valid_zip = zip_code.isdigit() and len(zip_code) == 5
    
    search_button = st.button(
        "Find District",
        type="primary",
        disabled=not (is_valid_street and is_valid_zip)
    )
    address = f"{street_address} {zip_code}" if search_button else ""

    # Always show the base district map
    if not address or not search_button:
        st.subheader("Chattanooga City Council Districts")
        m = create_base_district_map()
        map_data = st_folium(m, width=None, height=500, returned_objects=[])
    else:
        # Process address if entered
        if validate_address(address):
            coords = geocode_address(address)
            if coords:
                lat, lon = coords
                district_info = get_district_info(lat, lon)

                if district_info["district_number"] != "District not found":
                    m = create_district_map(lat, lon, district_info)
                    map_data = st_folium(m, width=None, height=500, returned_objects=[])

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
                    map_data = st_folium(m, width=None, height=500, returned_objects=[])
            else:
                st.error("Unable to locate your address. Please check the format and try again.")
                m = create_base_district_map()
                map_data = st_folium(m, width=None, height=500, returned_objects=[])
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
            map_data = st_folium(m, width=None, height=500, returned_objects=[])

with col2:
    st.subheader("Helpful Information")

    # Add Voter Registration Check
    with st.expander("✓ Check Voter Registration", expanded=False):
        st.markdown("""
        Verify your voter registration status for the March 4th, 2025 election.
        """)

        with st.form("voter_check_form"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            dob = st.date_input(
                "Date of Birth",
                min_value=datetime(1900, 1, 1),
                max_value=datetime.now(),
                help="Select your date of birth"
            )

            submitted = st.form_submit_button("Check Registration")

            if submitted:
                if all([first_name, last_name, dob]):
                    result = verify_voter_registration(
                        first_name=first_name,
                        last_name=last_name,
                        date_of_birth=dob.strftime("%Y-%m-%d")
                    )

                    if result["status"] == "success":
                        if result["registered"] == "active":
                            st.success(result["message"])
                            st.markdown(f"""
                            **Additional Information:**
                            - {result['precinct']}
                            - {result['district']}
                            - {result['additional_info']}
                            """)
                        else:
                            st.warning("""
                            We couldn't find your voter registration.
                            Register to vote at [GoVoteTN.gov](https://govotetn.gov)
                            """)
                    else:
                        st.error(result["message"])
                else:
                    st.error("Please fill in all required fields")

        st.markdown("""
        **Need to register or update your information?**  
        Visit [GoVoteTN.gov](https://govotetn.gov)
        """)

    with st.expander("🗳️ Early Voting Details", expanded=False):
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

    with st.expander("📋 View Sample Ballot", expanded=False):
        st.markdown("""
        Preview the March 4th, 2025 City Council Election ballot below.
        """)
        with open("attached_assets/cha-sample-ballot-2025.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()
        st.download_button(
            label="📥 Download Sample Ballot PDF",
            data=PDFbyte,
            file_name="chattanooga-sample-ballot-2025.pdf",
            mime="application/pdf"
        )
        st.markdown("""
        *Note: This is a sample ballot for reference. Your actual ballot may vary based on your district.*
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