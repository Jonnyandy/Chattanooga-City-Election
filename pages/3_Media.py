import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timezone
import pytz

# Page configuration
st.set_page_config(
    page_title="Helpful Media | Chattanooga.Vote",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set sidebar title for the media page
st.sidebar.title("Helpful Media")



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

# Title
st.title("Helpful Media")

# The Chattanooga Show Section
st.header("The Chattanooga Show")

# Instagram embed code
instagram_embed = """
<blockquote class="instagram-media" data-instgrm-permalink="https://www.instagram.com/reel/DE7SC4JtTrl/?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:540px; min-width:326px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);">
    <!-- Instagram embed code here -->
</blockquote>
<script async src="//www.instagram.com/embed.js"></script>
"""

# Use components.html to render the Instagram embed
components.html(
    instagram_embed,
    height=600,
    scrolling=True
)

# ChattaMatters Section
st.header("ChattaMatters")
st.markdown("[ChattaMatters Article](https://chattamatters.com/whos-running-for-mayor-and-city-council-chattanooga-2025/)")

# YouTube embed
youtube_embed = """
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
    <iframe 
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
        src="https://www.youtube-nocookie.com/embed/x8wwylBLIVE?si=BrJCCX0u0gCMx0n1" 
        title="YouTube video player" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        referrerpolicy="strict-origin-when-cross-origin" 
        allowfullscreen>
    </iframe>
</div>
"""

# Use components.html to render the YouTube embed
components.html(
    youtube_embed,
    height=400
)