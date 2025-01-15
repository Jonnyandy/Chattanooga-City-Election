import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.geocoding import validate_address, geocode_address
from utils.district_data import get_district_info
from utils.mapping import create_district_map, create_base_district_map

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
Find your voting district by entering your address below. 
This tool uses official City of Chattanooga district boundaries.
""")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Find Your District")
    address = st.text_input(
        "Enter your street address and ZIP code",
        placeholder="123 Main St 37402",
        help="Enter your complete street address including ZIP code to find your district."
    )

    # Always show the base district map
    if not address:
        st.subheader("Chattanooga City Council Districts")
        m = create_base_district_map()
        st_folium(m, width=700, height=500)
    elif address:
        # Process address if entered
        if validate_address(address):
            coords = geocode_address(address)
            if coords:
                lat, lon = coords
                district_info = get_district_info(lat, lon)

                if district_info["district_number"] != "District not found":
                    m = create_district_map(lat, lon, district_info)
                    st_folium(m, width=700, height=500)

                    st.subheader("Your District Information")
                    st.write(f"District: {district_info['district_number']}")
                    if district_info.get('district_description'):
                        st.write(f"Area: {district_info['district_description']}")
                else:
                    st.error("""
                    Unable to determine your district. This may mean your address is outside 
                    the Chattanooga city limits. Please verify your address or contact the 
                    Election Commission for assistance.
                    """)
                    # Show base map as fallback
                    st.subheader("Chattanooga City Council Districts")
                    m = create_base_district_map()
                    st_folium(m, width=700, height=500)
            else:
                st.error("Unable to locate your address. Please check the format and try again.")
                # Show base map as fallback
                st.subheader("Chattanooga City Council Districts")
                m = create_base_district_map()
                st_folium(m, width=700, height=500)
        else:
            st.error("""
            Please enter a valid Chattanooga address in the format:
            '123 Main St 37402'

            Include:
            - Street number
            - Street name
            - ZIP code
            """)
            # Show base map as fallback
            st.subheader("Chattanooga City Council Districts")
            m = create_base_district_map()
            st_folium(m, width=700, height=500)

with col2:
    st.subheader("Helpful Information")
    st.markdown("""
    ### Address Format Example
    Enter your address as shown below:
    ```
    123 Main St 37402
    ```

    ### Valid ZIP Codes
    Chattanooga ZIP codes include:
    37401, 37402, 37403, 37404, 37405, 
    37406, 37407, 37408, 37409, 37410, 
    37411, 37412, 37415, 37416, etc.

    ### Need Help?
    Contact the Hamilton County Election Commission:
    - Phone: (423) 493-5100
    - Email: vote@hamiltontn.gov
    """)

# Footer
st.markdown("---")
st.markdown(
    "Data provided by City of Chattanooga. "
    "For official information, visit the [Election Commission website](https://elect.hamiltontn.gov/)."
)