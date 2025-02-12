
import streamlit as st
from datetime import datetime, timezone

def show_shared_sidebar():
    # Early Voting Information
    with st.sidebar.expander("Early Voting Information", expanded=False):
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

    with st.sidebar.expander("Check Registration", expanded=False):
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

    st.sidebar.markdown("---")
    with st.sidebar.expander("❓ Need Help?", expanded=True):
        st.markdown("""
        **Election Commission:**
        📞 (423) 493-5100
        📧 vote@hamiltontn.gov
        """)

    # Add title and attribution to sidebar
    st.sidebar.markdown("""
        <div style='text-align: center; padding-top: 0; margin-bottom: 20px;'>
            <h1 style='color: #1B4E5D; margin-bottom: 5px;'>chattanooga.vote</h1>
            <div style='margin: 20px 0;'>
                <div style='text-align: center; margin-bottom: 10px;'>
                    <img src='./assets/chattanoogashow_jonathanholborn.png' style='max-width: 400px; height: auto;' alt='The Chattanooga Show and Jonathan Holborn'>
                </div>
            </div>
            <p style='font-style: italic; color: #666;'>
                Brought to you by<br>
                <a href="https://www.instagram.com/chattanoogashow/" target="_blank">The Chattanooga Show</a><br>
                &
                <a href="https://jonathanholborn.com" target="_blank">Jonathan Holborn</a>
            </p>
        </div>
        <hr>
    """, unsafe_allow_html=True)
