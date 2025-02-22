import streamlit as st
from utils.candidate_data import get_all_candidates, get_district_candidates, Candidate
from utils.photo_scraper import get_candidate_photo
from typing import Optional
from pathlib import Path
from PIL import Image
from datetime import datetime, timezone

def show_campaign_video(video_id: str, aspect_ratio: str = "16:9") -> str:
    """Return HTML for embedding a YouTube video with specified aspect ratio"""
    if aspect_ratio == "9:16":
        width = 315  # Standard width for vertical video
        height = 560  # Height for 9:16 aspect ratio
    else:
        width = 560  # Standard width for horizontal video
        height = 315  # Height for 16:9 aspect ratio

    return f"""
    <div style="display: flex; justify-content: center;">
        <iframe
            width="{width}"
            height="{height}"
            src="https://www.youtube.com/embed/{video_id}"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
    </div>
    """

def candidate_card(candidate: Candidate):
    """Display a candidate card with photo and contact information"""
    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            try:
                photo_path = get_candidate_photo(candidate.name, candidate.district)
                if photo_path and Path(photo_path).exists():
                    st.image(photo_path, use_container_width=True)
            except Exception as e:
                st.error(f"Error displaying photo for {candidate.name}")

        with col2:
            st.markdown(f"### {candidate.name}")

            # Video section using expander
            with st.expander("📺 Watch Campaign Video"):
                if candidate.name == "Doll Sandridge" and candidate.contact and candidate.contact.website:
                    video_url = candidate.contact.website
                    if "youtube.com/shorts/" in video_url:
                        video_id = video_url.split("/")[-1]
                        st.markdown(show_campaign_video(video_id, "9:16"), unsafe_allow_html=True)
                    else:
                        st.markdown(show_campaign_video('SAMPLE_VIDEO_ID'), unsafe_allow_html=True)
                else:
                    st.markdown(show_campaign_video('SAMPLE_VIDEO_ID'), unsafe_allow_html=True)


            # Contact information
            if candidate.contact:
                if candidate.contact.website:
                    st.markdown(f"🌐 [Website]({candidate.contact.website})")
                if candidate.contact.email:
                    st.markdown(f"📧 {candidate.contact.email}")
                if candidate.contact.phone:
                    st.markdown(f"📞 {candidate.contact.phone}")

                # Social media links
                social_links = []
                if candidate.contact.facebook:
                    social_links.append(f'[Facebook]({candidate.contact.facebook})')
                if candidate.contact.instagram:
                    social_links.append(f'[Instagram]({candidate.contact.instagram})')
                if candidate.contact.linkedin:
                    social_links.append(f'[LinkedIn]({candidate.contact.linkedin})')
                if candidate.contact.twitter:
                    social_links.append(f'[Twitter]({candidate.contact.twitter})')

                if social_links:
                    st.markdown(" • ".join(social_links))

# Page configuration
st.set_page_config(
    page_title="Candidates | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide"
)

# Main content
st.title("🗳️ City Council Candidates")
st.markdown("### March 4th, 2025 Election")

# District filter
district_filter = st.selectbox(
    "Filter by District",
    ["All Districts"] + [str(i) for i in range(1, 10)],
    index=0
)

# Get and display candidates
if district_filter == "All Districts":
    candidates = sorted(get_all_candidates(), key=lambda x: int(x.district))
else:
    candidates = get_district_candidates(district_filter)

# Group candidates by district
candidates_by_district = {}
for candidate in candidates:
    if candidate.district not in candidates_by_district:
        candidates_by_district[candidate.district] = []
    candidates_by_district[candidate.district].append(candidate)

# Display candidates
for district in sorted(candidates_by_district.keys(), key=int):
    st.markdown(f"## District {district}")
    col1, col2 = st.columns(2)
    district_candidates = candidates_by_district[district]
    for i, candidate in enumerate(district_candidates):
        with col1 if i % 2 == 0 else col2:
            candidate_card(candidate)