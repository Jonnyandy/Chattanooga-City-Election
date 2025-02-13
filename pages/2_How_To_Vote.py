import streamlit as st
from datetime import datetime
import pytz
import base64

# Page Configuration
st.set_page_config(
    page_title="How to Vote | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide",
)

# Function to display and create download link for PDF
def get_pdf_download_link(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    return f'<a href="data:application/pdf;base64,{base64_pdf}" download="sample-ballot-2025.pdf">Click here to download the Sample Ballot</a>'

# Election countdown
election_date = datetime(2025, 3, 4, tzinfo=pytz.timezone('America/New_York'))
current_time = datetime.now(pytz.timezone('America/New_York'))
time_until_election = election_date - current_time

days = time_until_election.days
hours = time_until_election.seconds // 3600
minutes = (time_until_election.seconds % 3600) // 60

# Display election countdown 
st.markdown(
    f"""
    <div style="background-color: #1B4E5D; color: white; padding: 10px; text-align: center; border-radius: 5px; margin-bottom: 20px;">
         {days} days until Election Day: March 4th, 2025
    </div>
    """,
    unsafe_allow_html=True
)

st.title("How to Vote")
st.markdown("### Important Information for Chattanooga Voters")

# Sample Ballot Section
with st.expander("📋 View Sample Ballot", expanded=False):
    st.markdown("### 2025 City Council Election Sample Ballot")
    # Display PDF viewer
    st.markdown("""
        <iframe src="data:application/pdf;base64,{}" width="100%" height="800px" type="application/pdf">
        </iframe>
        """.format(base64.b64encode(open("attached_assets/cha-sample-ballot-2025.pdf", "rb").read()).decode('utf-8')), 
        unsafe_allow_html=True
    )
    # Download button for the sample ballot
    st.markdown(get_pdf_download_link("attached_assets/cha-sample-ballot-2025.pdf"), unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    # Early Voting Information
    with st.expander("Early Voting Information", expanded=True):
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

    # Voter Registration Information
    with st.expander("Check Registration", expanded=True):
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

with col2:
    # Need Help Section
    with st.expander("❓ Need Help?", expanded=True):
        st.markdown("""
        **Election Commission:**
        📞 (423) 493-5100
        📧 vote@hamiltontn.gov
        """)

    # Poll Worker Information
    with st.expander("🤝 Become a Poll Worker", expanded=True):
        st.markdown("""
        Poll officials get a stipend of $135 - $175 per election.  
        Sign up at [elect.hamiltontn.gov/pollworker](http://elect.hamiltontn.gov/pollworker)
        """)

# Add title and attribution to sidebar
st.sidebar.markdown("""
<hr>
    <div style='text-align: center; padding-top: 0; margin-bottom: 10px;'>
        <h1 style='color: #1B4E5D; margin-bottom: 5px;'>chattanooga.vote</h1>
    </div>
""", unsafe_allow_html=True)
st.sidebar.image('assets/chattanoogashow_jonathanholborn.png', width=320, use_container_width=False)

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