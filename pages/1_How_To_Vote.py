
import streamlit as st
from datetime import datetime
import pytz

# Page Configuration
st.set_page_config(
    page_title="How to Vote | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

    st.image('assets/chattanoogashow_jonathanholborn.png', use_container_width=True)
