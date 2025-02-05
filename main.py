import streamlit as st
import folium
from datetime import datetime
from streamlit_folium import st_folium
from utils.geocoding import validate_address, geocode_address
from utils.district_data import get_district_info, get_council_member
from utils.mapping import create_district_map, create_base_district_map

# Page configuration
st.set_page_config(
    page_title="Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            transition: all 0.3s ease-in-out;
        }
        .stButton button {
            width: 100%;
        }
        .st-emotion-cache-1cypcdb {
            padding-top: 50px !important;
        }
        /* Add modal CSS */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.7);
            z-index: 1000;
            backdrop-filter: blur(5px);
            justify-content: center;
            align-items: center;
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
        }

        .modal-overlay.visible {
            opacity: 1;
        }

        .modal-content {
            background: white;
            padding: 20px;
            border-radius: 10px;
            width: 90%;
            max-width: 800px;
            max-height: 90vh;
            overflow-y: auto;
            position: relative;
            transform: translateY(-20px);
            transition: transform 0.3s ease-in-out;
        }

        .modal-overlay.visible .modal-content {
            transform: translateY(0);
        }

        .modal-close {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 24px;
            cursor: pointer;
            color: #666;
            transition: color 0.3s;
        }

        .modal-close:hover {
            color: #000;
        }

        .video-container {
            position: relative;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
            height: 0;
            overflow: hidden;
        }

        .video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
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
# Initialize session state for modals
if 'show_chattanooga_show' not in st.session_state:
    st.session_state.show_chattanooga_show = False
if 'show_chattamatters' not in st.session_state:
    st.session_state.show_chattamatters = False


# Add sidebar content
with st.sidebar:
    st.title("Quick Links")
    st.markdown("---")

    with st.expander("🗳️ Voting Information", expanded=True):
        if st.button("📍 Find My District"):
            st.session_state.active_section = "find_district"

        st.markdown("---")
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

    with st.expander("✓ Registration", expanded=False):
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

    st.markdown("---")
    with st.expander("❓ Need Help?", expanded=True):
        st.markdown("""
        **Election Commission:**
        📞 (423) 493-5100
        📧 vote@hamiltontn.gov
        """)

    with st.expander("ℹ️ Helpful Information", expanded=False):
        if st.button("📺 The Chattanooga Show"):
            st.session_state.show_chattanooga_show = True

        if st.button("📰 ChattaMatters"):
            st.session_state.show_chattamatters = True

        # Add JavaScript for panel and lightbox control
        st.markdown("""
        <div class="lightbox" id="lightbox">
            <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
            <div class="lightbox-content" id="lightbox-content"></div>
        </div>
        <script>
        function hidePanel() {
            document.querySelector('.slide-out-panel').classList.remove('active');
        }
        
        function openLightbox(content) {
            document.getElementById('lightbox-content').innerHTML = content;
            document.getElementById('lightbox').classList.add('active');
        }
        
        function closeLightbox() {
            document.getElementById('lightbox').classList.remove('active');
        }
        </script>
        """, unsafe_allow_html=True)

    with st.expander("🤝 Become a Poll Worker", expanded=False):
        st.markdown("""
        Poll officials get a stipend of $135 - $175 per election.  
        Sign up at [elect.hamiltontn.gov/pollworker](http://elect.hamiltontn.gov/pollworker)
        """)

# Countdown to Election Day
election_date = datetime(2025, 3, 4)
now = datetime.now()
delta = election_date - now

if delta.days >= 0:
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    countdown_text = f"🗓️ {days} days until Election Day"
    st.markdown(f'<p class="header-countdown">{countdown_text}</p>', unsafe_allow_html=True)

# Add modals
if st.session_state.show_chattanooga_show:
    modal_html = """
    <div class="modal-overlay visible" id="chattanoogaShowModal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal('chattanoogaShowModal')">&times;</span>
            <h2>The Chattanooga Show</h2>
            <div class="video-container">
                <blockquote class="instagram-media" data-instgrm-permalink="https://www.instagram.com/reel/DE7SC4JtTrl/"
                    data-instgrm-version="14" style="width: 100%;">
                </blockquote>
            </div>
            <script async src="//www.instagram.com/embed.js"></script>
        </div>
    </div>
    <script>
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
            window.streamlitResetState();
        }
    </script>
    """
    st.markdown(modal_html, unsafe_allow_html=True)

if st.session_state.show_chattamatters:
    modal_html = """
    <div class="modal-overlay visible" id="chattamattersModal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal('chattamattersModal')">&times;</span>
            <h2>ChattaMatters</h2>
            <div class="video-container">
                <iframe width="100%" height="315"
                    src="https://www.youtube.com/embed/YOUR_VIDEO_ID"
                    title="ChattaMatters"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
                </iframe>
            </div>
        </div>
    </div>
    <script>
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
            window.streamlitResetState();
        }

        // Reset session state when modal is closed
        window.streamlitResetState = function() {
            const streamlit = window.parent.streamlit;
            streamlit.setComponentValue({
                show_chattanooga_show: false,
                show_chattamatters: false
            });
        }
    </script>
    """
    st.markdown(modal_html, unsafe_allow_html=True)


# Header
st.title("🗳️ Chattanooga . Vote")

st.markdown("""
Find your city council district by entering your address below. 
This tool uses official City of Chattanooga district boundaries.
""")

# Main content
row1_col1, row1_col2 = st.columns([1, 2], gap="large")
row2_col1 = st.columns(1)

with row1_col1:
    st.subheader("Find Your District")

    # Address input
    street_address = st.text_input(
        "Street Address",
        placeholder="123 Main St",
        help="Enter your street address"
    )

    zip_code = st.text_input(
        "ZIP Code",
        placeholder="37402",
        help="Enter your ZIP code",
        max_chars=5
    )

    # Search button
    if st.button("Find District", type="primary"):
        if street_address and zip_code:
            address = f"{street_address}, {zip_code}"

            if validate_address(address):
                coords = geocode_address(address)

                if coords:
                    # Store current search in session state
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

    # Display results based on session state
    if st.session_state.search_performed and st.session_state.current_coords:
        lat, lon = st.session_state.current_coords
        district_info = st.session_state.district_info

        if district_info and district_info["district_number"] != "District not found":
            # Show district information below form in col1
            st.subheader("Your District Information")
            council_info = get_council_member(district_info["district_number"])

            st.markdown(f"**District:** {district_info['district_number']}")
            st.markdown(f"**Current Council Member:** {council_info['name']}")

            if district_info.get('candidates'):
                st.markdown("---")
                st.markdown("**March 4th, 2025 Election Candidates:**")
                for candidate in district_info['candidates']:
                    st.markdown(f"• {candidate}")

            st.markdown("---")
            if district_info["polling_place"] != "Not found":
                st.markdown(f"""
                **Polling Location:** {district_info["polling_place"]}  
                **Address:** {district_info["polling_address"]}  
                **Precinct:** {district_info["precinct"]}
                """)
        else:
            st.error("Address not found in Chattanooga city limits")


with row1_col2:
    if not st.session_state.search_performed:
        st.subheader("Chattanooga City Council Districts")
        m = create_base_district_map()
        map_data = st_folium(m, width=None, height=500, key="base_map")

    # Show map in col2
    if st.session_state.search_performed and st.session_state.current_coords:
        lat, lon = st.session_state.current_coords
        district_info = st.session_state.district_info

        if district_info and district_info["district_number"] != "District not found":
            m = create_district_map(lat, lon, district_info)
            map_key = f"map_{st.session_state.current_address}"
            map_data = st_folium(m, width=None, height=500, key=map_key)


# Rest of the content (Helpful Information sections) - removed redundant section
with row2_col1[0]:
    st.subheader("Helpful Information")


# Footer
st.markdown("---")
st.markdown(
    "Data provided by City of Chattanooga. "
    "For official information, visit the [Election Commission website](https://elect.hamiltontn.gov/).",
    unsafe_allow_html=True
)