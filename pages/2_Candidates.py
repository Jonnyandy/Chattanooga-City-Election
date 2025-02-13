import streamlit as st
import base64
from utils.candidate_data import get_all_candidates, get_district_candidates
from pathlib import Path

# Page Configuration
st.set_page_config(
    page_title="Candidates | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide"
)

# Function to create download link for PDF
def get_pdf_download_link(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    return f'<a href="data:application/pdf;base64,{base64_pdf}" download="sample-ballot-2025.pdf" class="download-button">Download Sample Ballot</a>'

# Custom CSS for the download button
st.markdown("""
    <style>
    .download-button {
        display: inline-block;
        padding: 0.5em 1em;
        color: white;
        background-color: #1B4E5D;
        text-decoration: none;
        border-radius: 5px;
        margin: 1em 0;
        transition: background-color 0.3s;
    }
    .download-button:hover {
        background-color: #2C7A92;
    }
    </style>
""", unsafe_allow_html=True)

st.title("2025 City Council Candidates")

# Add Sample Ballot download button
st.markdown(get_pdf_download_link("attached_assets/cha-sample-ballot-2025.pdf"), unsafe_allow_html=True)

# Display candidates by district
candidates = get_all_candidates()

# Group candidates by district
for district in sorted(set(c.district for c in candidates)):
    st.header(f"District {district}")
    district_candidates = get_district_candidates(district)
    
    cols = st.columns(min(3, len(district_candidates)))
    for idx, candidate in enumerate(district_candidates):
        with cols[idx % 3]:
            st.subheader(candidate.name)
            
            # Display candidate photo if available
            if candidate.assets_photo:
                st.image(candidate.assets_photo, use_column_width=True)
            
            # Display contact information
            if candidate.contact:
                if candidate.contact.website:
                    st.markdown(f"[Campaign Website]({candidate.contact.website})")
                if candidate.contact.email:
                    st.markdown(f"📧 {candidate.contact.email}")
                if candidate.contact.phone:
                    st.markdown(f"📞 {candidate.contact.phone}")
                if candidate.contact.facebook:
                    st.markdown(f"[Facebook]({candidate.contact.facebook})")
                if candidate.contact.instagram:
                    st.markdown(f"[Instagram]({candidate.contact.instagram})")
                if candidate.contact.twitter:
                    st.markdown(f"[Twitter]({candidate.contact.twitter})")
                if candidate.contact.linkedin:
                    st.markdown(f"[LinkedIn]({candidate.contact.linkedin})")

# Sidebar content
st.sidebar.markdown("""
<hr>
    <div style='text-align: center; padding-top: 0; margin-bottom: 10px;'>
        <h1 style='color: #1B4E5D; margin-bottom: 5px;'>chattanooga.vote</h1>
    </div>
""", unsafe_allow_html=True)

st.sidebar.image('assets/chattanoogashow_jonathanholborn.png', width=320)

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
