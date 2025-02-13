import streamlit as st
from datetime import datetime
import pytz

# Page Configuration
st.set_page_config(
    page_title="How to Vote | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide",
)

# Function to load PDF file
def get_pdf_data():
    with open("attached_assets/cha-sample-ballot-2025.pdf", "rb") as file:
        return file.read()

# Election countdown
election_date = datetime(2025, 3, 4, tzinfo=pytz.timezone('America/New_York'))
current_time = datetime.now(pytz.timezone('America/New_York'))
time_until_election = election_date - current_time

days = time_until_election.days
hours = time_until_election.seconds // 3600
minutes = (time_until_election.seconds % 3600) // 60

# Display countdown
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

    # Add download button for the sample ballot
    pdf_data = get_pdf_data()
    st.download_button(
        label="Download Sample Ballot",
        data=pdf_data,
        file_name="sample-ballot-2025.pdf",
        mime="application/pdf",
        type="primary"
    )

    # Display PDF using iframe
    pdf_display = f"""
        <iframe
            src="attached_assets/cha-sample-ballot-2025.pdf"
            width="100%"
            height="800"
            type="application/pdf">
        </iframe>
    """
    st.components.v1.html(pdf_display, height=800)

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Important Dates")
    st.markdown("""
    - **Election Day:** March 4th, 2025
    - **Early Voting:** February 12th - February 27th, 2025
    - **Registration Deadline:** February 2nd, 2025
    """)

    st.subheader("Early Voting Locations")
    st.markdown("""
    - **Election Commission Office:**
        - 700 River Terminal Road
        - Monday - Friday, 8 AM - 6 PM
        - Saturday, 9 AM - 4 PM
    
    - **Brainerd Recreation Center:**
        - 1010 N Moore Road
        - Monday - Friday, 10 AM - 6 PM
        - Saturday, 9 AM - 4 PM
        
    - **Hixson Community Center:**
        - 5401 School Drive
        - Monday - Friday, 10 AM - 6 PM
        - Saturday, 9 AM - 4 PM
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
    st.subheader("What to Bring")
    st.markdown("""
    #### Valid Photo ID:
    - Tennessee driver license
    - US Passport
    - Photo ID issued by Tennessee Department of Safety
    - US Military photo ID
    - Tennessee handgun carry permit with photo
    """)
    
    st.subheader("Need a Ride?")
    st.markdown("""
    Free rides to polling locations are available.
    Call (423) 209-8683 for assistance.
    """)
    
    st.subheader("Be a Poll Worker")
    st.markdown("""
    Help your community by becoming a poll worker!
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