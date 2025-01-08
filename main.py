import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from utils.geocoding import validate_address, geocode_address
from utils.district_data import get_district_info, get_council_member, get_district_boundaries
from utils.mapping import create_district_map

# Page configuration
st.set_page_config(
    page_title="Chattanooga Voting Information",
    page_icon="🗳️",
    layout="wide"
)

# Custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header
st.title("🗳️ Chattanooga Voting Information")
st.markdown("""
Find your voting district, polling place, and election information. 
This tool uses official City of Chattanooga district boundaries and polling location data.
""")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Find Your Voting Information")
    address = st.text_input(
        "Enter your street address and ZIP code",
        placeholder="123 Main St 37402",
        help="Enter your complete street address including ZIP code to find your district and polling place."
    )

    if address:
        # Validate address
        if validate_address(address):
            # Get coordinates
            coords = geocode_address(address)

            if coords:
                lat, lon = coords
                # Get district information
                district_info = get_district_info(lat, lon)

                if district_info["district_number"] != "District not found":
                    # Create and display map
                    m = create_district_map(lat, lon, district_info)
                    st_folium(m, width=700)

                    # Display district information
                    st.subheader("Your District Information")
                    st.write(f"District: {district_info['district_number']}")
                    if district_info.get('district_description'):
                        st.write(f"Area: {district_info['district_description']}")
                    st.write(f"Precinct: {district_info['precinct']}")

                    # Council member information
                    try:
                        council_member = get_council_member(district_info['district_number'])
                        st.subheader("Your Council Member")
                        st.write(f"Name: {council_member['name']}")
                        st.write(f"Email: {council_member['email']}")
                        st.write(f"Phone: {council_member['phone']}")

                        # Polling place information
                        if district_info['polling_place'] != "Not found":
                            st.subheader("Your Polling Place")
                            st.write("Here's your assigned polling location:")
                            st.markdown(f"""
                            **Location Name:** {district_info['polling_place']}  
                            **Address:** {district_info['polling_address']}  
                            **Precinct:** {district_info['precinct']}  
                            **Hours:** 7:00 AM - 7:00 PM on Election Day

                            *This location was determined based on your provided address.*

                            If you need to verify this information or find alternative polling locations,
                            please contact the Hamilton County Election Commission at (423) 493-5100.
                            """)
                        else:
                            st.warning("""
                            We couldn't determine your exact polling place. 
                            Please contact the Hamilton County Election Commission:
                            - Phone: (423) 493-5100
                            - Email: vote@hamiltontn.gov
                            - Address: 700 River Terminal Road, Chattanooga, TN 37406
                            """)
                    except Exception as e:
                        st.error("Error retrieving council member information. Please try again later.")
                else:
                    st.error("""
                    Unable to determine your district. This may mean your address is outside the Chattanooga city limits. 
                    Please verify your address or contact the Election Commission for assistance.
                    """)
            else:
                st.error("Unable to locate your address. Please check the format and try again.")
        else:
            st.error("Please enter a valid street address and ZIP code (e.g., '123 Main St 37402')")

with col2:
    st.subheader("Important Dates")
    st.markdown("""
    - **Next Election Date:** November 5, 2024
    - **Registration Deadline:** October 7, 2024
    - **Early Voting Period:** October 16-31, 2024
    """)

    st.subheader("Election Office Contact")
    st.markdown("""
    Hamilton County Election Commission  
    700 River Terminal Road  
    Chattanooga, TN 37406  
    Phone: (423) 493-5100  
    Email: vote@hamiltontn.gov
    """)

    st.subheader("Voter ID Requirements")
    st.markdown("""
    You must present a valid photo ID to vote in person. Acceptable IDs include:
    - Valid Tennessee driver's license
    - Valid photo ID issued by Tennessee
    - Valid U.S. passport
    - Valid U.S. military photo ID
    - Tennessee handgun carry permit with photo
    """)

# Footer
st.markdown("---")
st.markdown(
    "Data provided by Hamilton County Election Commission and City of Chattanooga. "
    "For official information, please visit the [Election Commission website](https://elect.hamiltontn.gov/)."
)