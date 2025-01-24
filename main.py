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
Find your city council district by entering your address below. 
This tool uses official City of Chattanooga district boundaries.
""")

# Main content columns
col1, col2 = st.columns([2, 1], gap="large")

with col1:
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
    address = f"{street_address} {zip_code}" if search_button else ""

    # Map container with 1:1 aspect ratio
    st.markdown('<div class="map-container">', unsafe_allow_html=True)

    # Process address and show map
    if not address or not search_button:
        st.subheader("Chattanooga City Council Districts")
        m = create_base_district_map()
        map_data = st_folium(m, width=None, height=None, returned_objects=[])
    else:
        if validate_address(address):
            coords = geocode_address(address)
            if coords:
                lat, lon = coords
                district_info = get_district_info(lat, lon)

                if district_info["district_number"] != "District not found":
                    m = create_district_map(lat, lon, district_info)
                    map_data = st_folium(m, width=None, height=None, returned_objects=[])

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

                    # Display district info
                    with col2:
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
                "Please enter a valid Chattanooga address in the format:\n"
                "'123 Main St 37402'\n\n"
                "Include:\n"
                "- Street number\n"
                "- Street name\n"
                "- ZIP code"
            )

    st.markdown('</div>', unsafe_allow_html=True)

# Add helpful information content that will be moved to off-canvas menu
helpful_info = """
<div id="off-canvas-content">
    <div class="info-section">
        <h3>📺 Video Guide</h3>
        <p>Watch this helpful video about voting in Chattanooga:</p>
        <blockquote class="instagram-media" data-instgrm-captioned data-instgrm-permalink="https://www.instagram.com/reel/DE7SC4JtTrl/?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:540px; min-width:326px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:16px;"> <a href="https://www.instagram.com/reel/DE7SC4JtTrl/?utm_source=ig_embed&amp;utm_campaign=loading" style=" background:#FFFFFF; line-height:0; padding:0 0; text-align:center; text-decoration:none; width:100%;" target="_blank"> <div style=" display: flex; flex-direction: row; align-items: center;"> <div style="background-color: #F4F4F4; border-radius: 50%; flex-grow: 0; height: 40px; margin-right: 14px; width: 40px;"></div> <div style="display: flex; flex-direction: column; flex-grow: 1; justify-content: center;"> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; margin-bottom: 6px; width: 100px;"></div> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; width: 60px;"></div></div></div><div style="padding: 19% 0;"></div> <div style="display:block; height:50px; margin:0 auto 12px; width:50px;"><svg width="50px" height="50px" viewBox="0 0 60 60" version="1.1" xmlns="https://www.w3.org/2000/svg" xmlns:xlink="https://www.w3.org/1999/xlink"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><g transform="translate(-511.000000, -20.000000)" fill="#000000"><g><path d="M556.869,30.41 C554.814,30.41 553.148,32.076 553.148,34.131 C553.148,36.186 554.814,37.852 556.869,37.852 C558.924,37.852 560.59,36.186 560.59,34.131 C560.59,32.076 558.924,30.41 556.869,30.41 M541,60.657 C535.114,60.657 530.342,55.887 530.342,50 C530.342,44.114 535.114,39.342 541,39.342 C546.887,39.342 551.658,44.114 551.658,50 C551.658,55.887 546.887,60.657 541,60.657 M541,33.886 C532.1,33.886 524.886,41.1 524.886,50 C524.886,58.899 532.1,66.113 541,66.113 C549.9,66.113 557.115,58.899 557.115,50 C557.115,41.1 549.9,33.886 541,33.886 M565.378,62.101 C565.244,65.022 564.756,66.606 564.346,67.663 C563.803,69.06 563.154,70.057 562.106,71.106 C561.058,72.155 560.06,72.803 558.662,73.347 C557.607,73.757 556.021,74.244 553.102,74.378 C549.944,74.521 548.997,74.552 541,74.552 C533.003,74.552 532.056,74.521 528.898,74.378 C525.979,74.244 524.393,73.757 523.338,73.347 C521.94,72.803 520.942,72.155 519.894,71.106 C518.846,70.057 518.197,69.06 517.654,67.663 C517.244,66.606 516.755,65.022 516.623,62.101 C516.479,58.943 516.448,57.996 516.448,50 C516.448,42.003 516.479,41.056 516.623,37.899 C516.755,34.978 517.244,33.391 517.654,32.338 C518.197,30.938 518.846,29.942 519.894,28.894 C520.942,27.846 521.94,27.196 523.338,26.654 C524.393,26.244 525.979,25.756 528.898,25.623 C532.057,25.479 533.004,25.448 541,25.448 C548.997,25.448 549.943,25.479 553.102,25.623 C556.021,25.756 557.607,26.244 558.662,26.654 C560.06,27.196 561.058,27.846 562.106,28.894 C563.154,29.942 563.803,30.938 564.346,32.338 C564.756,33.391 565.244,34.978 565.378,37.899 C565.522,41.056 565.552,42.003 565.552,50 C565.552,57.996 565.522,58.943 565.378,62.101 M570.82,37.631 C570.674,34.438 570.167,32.258 569.425,30.349 C568.659,28.377 567.633,26.702 565.965,25.035 C564.297,23.368 562.623,22.342 560.652,21.575 C558.743,20.834 556.562,20.326 553.369,20.18 C550.169,20.033 549.148,20 541,20 C532.853,20 531.831,20.033 528.631,20.18 C525.438,20.326 523.257,20.834 521.349,21.575 C519.376,22.342 517.703,23.368 516.035,25.035 C514.368,26.702 513.342,28.377 512.574,30.349 C511.834,32.258 511.326,34.438 511.181,37.631 C511.035,40.831 511,41.851 511,50 C511,58.147 511.035,59.17 511.181,62.369 C511.326,65.562 511.834,67.743 512.574,69.651 C513.342,71.625 514.368,73.296 516.035,74.965 C517.703,76.634 519.376,77.658 521.349,78.425 C523.257,79.167 525.438,79.673 528.631,79.82 C531.831,79.965 532.853,80.001 541,80.001 C549.148,80.001 550.169,79.965 553.369,79.82 C556.562,79.673 558.743,79.167 560.652,78.425 C562.623,77.658 564.297,76.634 565.965,74.965 C567.633,73.296 568.659,71.625 569.425,69.651 C570.167,67.743 570.674,65.562 570.82,62.369 C570.966,59.17 571,58.147 571,50 C571,41.851 570.966,40.831 570.82,37.631"></path></g></g></g></svg></div><div style="padding-top: 8px;"> <div style=" color:#3897f0; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:550; line-height:18px;">View this post on Instagram</div></div><div style="padding: 12.5% 0;"></div> <div style="display: flex; flex-direction: row; margin-bottom: 14px; align-items: center;"><div> <div style="background-color: #F4F4F4; border-radius: 50%; height: 12.5px; width: 12.5px; transform: translateX(0px) translateY(7px);"></div> <div style="background-color: #F4F4F4; height: 12.5px; transform: rotate(-45deg) translateX(3px) translateY(1px); width: 12.5px; flex-grow: 0; margin-right: 14px; margin-left: 2px;"></div> <div style="background-color: #F4F4F4; border-radius: 50%; height: 12.5px; width: 12.5px; transform: translateX(9px) translateY(-18px);"></div></div><div style="margin-left: 8px;"> <div style=" background-color: #F4F4F4; border-radius: 50%; flex-grow: 0; height: 20px; width: 20px;"></div> <div style=" width: 0; height: 0; border-top: 2px solid transparent; border-left: 6px solid #f4f4f4; border-bottom: 2px solid transparent; transform: translateX(16px) translateY(-4px) rotate(30deg)"></div></div><div style="margin-left: auto;"> <div style=" width: 0px; border-top: 8px solid #F4F4F4; border-right: 8px solid transparent; transform: translateY(16px);"></div> <div style=" background-color: #F4F4F4; flex-grow: 0; height: 12px; width: 16px; transform: translateY(-4px);"></div> <div style=" width: 0; height: 0; border-top: 8px solid #F4F4F4; border-left: 8px solid transparent; transform: translateY(-4px) translateX(8px);"></div></div></div> <div style="display: flex; flex-direction: column; flex-grow: 1; justify-content: center; margin-bottom: 24px;"> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; margin-bottom: 6px; width: 224px;"></div> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; width: 144px;"></div></div></a><p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;"><a href="https://www.instagram.com/reel/DE7SC4JtTrl/?utm_source=ig_embed&amp;utm_campaign=loading" style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none;" target="_blank">A post shared by The Chattanooga Show (@chattanoogashow)</a></p></div></blockquote>
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
        <p><strong>Need to register or update your information?</strong>  
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
        <p>Preview the March 4th, 2025 City Council Election ballot below.</p>
        <a href="attached_assets/cha-sample-ballot-2025.pdf" download="chattanooga-sample-ballot-2025.pdf">
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

# Footer
st.markdown("---")
st.markdown(
    "Data provided by City of Chattanooga. "
    "For official information, visit the [Election Commission website](https://elect.hamiltontn.gov/).",
    unsafe_allow_html=True
)