# Content from Media.py
import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Helpful Media | Chattanooga.Vote",
    page_icon="🎥",
    layout="wide"
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