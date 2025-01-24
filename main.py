import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.geocoding import validate_address, geocode_address
from utils.district_data import get_district_info, get_council_member
from utils.mapping import create_district_map, create_base_district_map
from datetime import datetime, timezone, timedelta

# Page configuration
st.set_page_config(
    page_title="Chattanooga Voting Information",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS and JavaScript
with open('styles/custom.css') as f:
    css = f.read()

# JavaScript for off-canvas menu
js = """
<script>
function toggleMenu() {
    const menu = document.querySelector('.off-canvas-menu');
    const overlay = document.querySelector('.off-canvas-overlay');
    const body = document.querySelector('body');

    menu.classList.toggle('active');
    overlay.classList.toggle('active');
    body.style.overflow = menu.classList.contains('active') ? 'hidden' : '';
}

function closeMenu() {
    const menu = document.querySelector('.off-canvas-menu');
    const overlay = document.querySelector('.off-canvas-overlay');
    const body = document.querySelector('body');

    menu.classList.remove('active');
    overlay.classList.remove('active');
    body.style.overflow = '';
}
</script>

<button onclick="toggleMenu()" class="menu-toggle">
    <span>Helpful Info</span>
</button>

<div class="off-canvas-overlay" onclick="closeMenu()"></div>
<div class="off-canvas-menu">
    <h2>Helpful Information</h2>
    <div id="helpful-info-content"></div>
</div>
"""

st.markdown(f"""
    <style>
        {css}
    </style>
    {js}
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
st.title("🗳️ Chattanooga . Vote")

st.markdown("""
<div style="text-align: center; max-width: 800px; margin: 0 auto 2rem;">
    Find your city council district, view candidate information, and access important voting resources. 
    This tool uses official City of Chattanooga district boundaries.
</div>
""", unsafe_allow_html=True)

# Main content area
address_container = st.container()

with address_container:
    st.markdown('<div style="max-width: 800px; margin: 0 auto;">', unsafe_allow_html=True)

    st.subheader("Find Your District")

    col_addr, col_zip = st.columns([2, 1])
    with col_addr:
        street_address = st.text_input(
            "Street Address",
            placeholder="123 Main St",
            help="Enter a valid street address within the city limits of Chattanooga, TN",
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

    st.markdown('</div>', unsafe_allow_html=True)

# Map and results container
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Map column
st.markdown('<div class="map-column">', unsafe_allow_html=True)
address = f"{street_address} {zip_code}" if search_button else ""

if not address or not search_button:
    st.subheader("Chattanooga City Council Districts")
    m = create_base_district_map()
    map_data = st_folium(m, width=None, height=500, returned_objects=[])
else:
    if validate_address(address):
        coords = geocode_address(address)
        if coords:
            lat, lon = coords
            district_info = get_district_info(lat, lon)

            if district_info["district_number"] != "District not found":
                m = create_district_map(lat, lon, district_info)
                map_data = st_folium(m, width=None, height=500, returned_objects=[])

                # District information HTML
                district_html = f"""
                <div class="district-info">
                    <h3>Your District Information</h3>
                    <p><strong>District:</strong> {district_info['district_number']}</p>
                    <p><strong>Current Council Member:</strong> {get_council_member(district_info['district_number'])['name']}</p>

                    <hr>
                    <h4>March 4th, 2025 Election Candidates:</h4>
                    <ul>
                """

                for candidate in district_info.get('candidates', []):
                    district_html += f"<li>{candidate}</li>"

                district_html += """
                    </ul>

                    <hr>
                    <h4>Your Polling Location</h4>
                """

                if district_info["polling_place"] != "Not found":
                    district_html += f"""
                    <p><strong>Location:</strong> {district_info["polling_place"]}</p>
                    <p><strong>Address:</strong> {district_info["polling_address"]}</p>
                    <p><strong>Precinct:</strong> {district_info["precinct"]}</p>
                    """
                else:
                    district_html += """
                    <p class="warning">Polling location information not available for this address. 
                    Please contact the Election Commission for assistance.</p>
                    """

                district_html += "</div>"

                st.markdown(district_html, unsafe_allow_html=True)
            else:
                st.error(
                    "Unable to determine your district. This may mean your address is "
                    "outside the Chattanooga city limits. Please verify your address "
                    "or contact the Election Commission for assistance."
                )
        else:
            st.error("Unable to locate your address. Please check the format and try again.")
    else:
        st.error(
            "Please enter a valid Chattanooga address including:\n"
            "- Street number\n"
            "- Street name\n"
            "- ZIP code"
        )

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; padding: 2rem 0;">Data provided by City of Chattanooga. '
    'For official information, visit the <a href="https://elect.hamiltontn.gov/" target="_blank">'
    'Election Commission website</a>.</div>',
    unsafe_allow_html=True
)

# Add the information sections to the off-canvas menu
helpful_info = """
<div id="off-canvas-content">
    <div class="info-section">
        <h3>📺 Video Guide</h3>
        <p>Watch this helpful video about voting in Chattanooga:</p>
        <blockquote class="instagram-media" data-instgrm-captioned data-instgrm-permalink="https://www.instagram.com/reel/DE7SC4JtTrl/?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14"></blockquote>
        <script async src="//www.instagram.com/embed.js"></script>
    </div>

    <div class="info-section">
        <h3>✓ Check Voter Registration</h3>
        <p>To check if you're registered to vote in the March 4th, 2025 election, visit the official Tennessee voter lookup tool:</p>
        <p><a href="https://tnmap.tn.gov/voterlookup/" target="_blank">Click here to verify your registration ↗</a></p>
        <p><strong>Need help?</strong></p>
        <ul>
            <li>Call Hamilton County Election Commission: (423) 493-5100</li>
            <li>Visit: 700 River Terminal Rd, Chattanooga, TN 37406</li>
            <li>Email: vote@hamiltontn.gov</li>
        </ul>
        <p><strong>Need to register or update your information?</strong><br>
        Visit <a href="https://govotetn.gov" target="_blank">GoVoteTN.gov</a></p>
    </div>

    <div class="info-section">
        <h3>🗳️ Early Voting Details</h3>
        <p><strong>Early Voting Period:</strong> February 12 – February 27, 2025<br>
        <em>ALL LOCATIONS CLOSED MONDAY, FEBRUARY 17TH, FOR PRESIDENTS DAY</em></p>

        <h4>Early Voting Locations:</h4>
        <ol>
            <li><strong>Election Commission</strong><br>
                700 River Terminal Rd, Chattanooga, TN 37406<br>
                <em>Monday - Friday: 8:00 am – 7:00 pm</em><br>
                <em>Saturday: 8:00 am – 4:00 pm</em></li>

            <li><strong>Hixson Community Center</strong><br>
                5401 School Dr, Hixson, TN 37343<br>
                <em>Monday - Friday: 10:00 am – 6:00 pm</em><br>
                <em>Saturday: 10:00 am – 4:00 pm</em></li>

            <li><strong>Chris L. Ramsey Sr. Community Center</strong><br>
                1010 N Moore Rd, Chattanooga, TN 37411<br>
                <em>Monday - Friday: 10:00 am – 6:00 pm</em><br>
                <em>Saturday: 10:00 am – 4:00 pm</em></li>
        </ol>

        <p><strong>Important Notes:</strong></p>
        <ul>
            <li>Only eligible voters who reside in the City of Chattanooga may participate</li>
            <li>PHOTO ID ISSUED BY STATE OF TN OR FEDERAL GOVT REQUIRED TO VOTE</li>
            <li>Visit <a href="http://govotetn.gov" target="_blank">govotetn.gov</a> to update your information</li>
        </ul>
    </div>

    <div class="info-section">
        <h3>📋 View Sample Ballot</h3>
        <p>Preview the March 4th, 2025 City Council Election ballot.</p>
        <a href="attached_assets/cha-sample-ballot-2025.pdf" download="chattanooga-sample-ballot-2025.pdf" 
           class="download-button">
            📥 Download Sample Ballot PDF
        </a>
        <p><em>Note: This is a sample ballot for reference. Your actual ballot may vary based on your district.</em></p>
    </div>

    <div class="info-section">
        <h3>📮 Valid ZIP Codes</h3>
        <p>Chattanooga ZIP codes include:</p>
        <ul>
            <li>37401-37412</li>
            <li>37415, 37416</li>
            <li>37419, 37421</li>
            <li>37450, 37351</li>
        </ul>
    </div>

    <div class="info-section">
        <h3>🤝 Become a Poll Worker</h3>
        <p>Poll officials get a stipend of $135 - $175 per election.<br>
        Sign up at <a href="http://elect.hamiltontn.gov/pollworker" target="_blank">elect.hamiltontn.gov/pollworker</a></p>
    </div>

    <div class="info-section">
        <h3>❓ Need Help?</h3>
        <p><strong>Contact the Hamilton County Election Commission:</strong></p>
        <ul>
            <li>Phone: (423) 493-5100</li>
            <li>Email: vote@hamiltontn.gov</li>
        </ul>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const content = document.getElementById('off-canvas-content');
    const target = document.getElementById('helpful-info-content');
    if (content && target) {
        target.innerHTML = content.innerHTML;
        content.remove();
    }
});
</script>
"""

st.markdown(helpful_info, unsafe_allow_html=True)