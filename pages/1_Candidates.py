# Content from All_Candidates.py
import streamlit as st
from utils.candidate_data import get_all_candidates, get_district_candidates, Candidate
from utils.photo_scraper import get_candidate_photo
from typing import Optional
from pathlib import Path
from PIL import Image
from datetime import datetime, timezone

def social_media_icon(platform: str) -> str:
    """Return HTML img tag for social media platform icon"""
    icons = {
        'email': '📧',
        'phone': '📞',
        'facebook': '<img src="https://raw.githubusercontent.com/gauravghongde/social-icons/master/SVG/Color/Facebook.svg" style="height: 32px; width: 32px; vertical-align: middle; margin: 0 5px;">',
        'instagram': '<img src="https://raw.githubusercontent.com/gauravghongde/social-icons/master/SVG/Color/Instagram.svg" style="height: 32px; width: 32px; vertical-align: middle; margin: 0 5px;">',
        'linkedin': '<img src="https://raw.githubusercontent.com/gauravghongde/social-icons/master/SVG/Color/LinkedIN.svg" style="height: 32px; width: 32px; vertical-align: middle; margin: 0 5px;">',
        'twitter': '<img src="https://raw.githubusercontent.com/gauravghongde/social-icons/master/SVG/Color/Twitter.svg" style="height: 32px; width: 32px; vertical-align: middle; margin: 0 5px;">',
        'website': '🌐',
        'youtube': '📺'
    }
    return icons.get(platform, '🔗')

def candidate_card(candidate: Candidate):
    """Display a candidate card with photo and contact information"""
    with st.container():
        st.markdown("""
        <style>
        .candidate-card {
            background-color: white;
            padding: 0;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            overflow: hidden;
        }
        .candidate-photo {
            width: 100%;
            max-height: 450px;
            object-fit: cover;
            margin: 0;
            display: block;
        }
        img {
            max-height: 450px;
            object-fit: cover;
        }
        .candidate-info {
            padding: 20px;
        }
        .photo-placeholder {
            width: 100%;
            height: 300px;
            background-color: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
        }
        .candidate-name {
            color: #1976D2;
            font-size: 24px;
            margin-bottom: 10px;
        }
        .candidate-contact {
            margin-top: 10px;
        }
        .social-link {
            margin-right: 10px;
            text-decoration: none;
            color: #666;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="candidate-card">', unsafe_allow_html=True)

        # Photo handling with improved error recovery
        try:
            photo_path = get_candidate_photo(candidate.name, candidate.district)
            if photo_path and Path(photo_path).exists():
                try:
                    st.image(photo_path, use_container_width=True, output_format="JPEG", caption=candidate.name)
                except Exception as e:
                    st.error(f"Error displaying photo for {candidate.name}")
                    st.markdown(
                        f'<div class="photo-placeholder">Photo not available</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    f'<div class="photo-placeholder">Photo not available</div>',
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"Error processing photo for {candidate.name}")
            st.markdown(
                f'<div class="photo-placeholder">Photo not available</div>',
                unsafe_allow_html=True
            )

        # Name
        st.markdown(f'<div class="candidate-name">{candidate.name}</div>', unsafe_allow_html=True)


        # Contact Information
        if candidate.contact:
            st.markdown('<div class="candidate-contact">', unsafe_allow_html=True)

            if candidate.contact.website:
                if "youtube.com" in candidate.contact.website and candidate.name == "Doll Sandridge":
                    video_url = candidate.contact.website.replace('shorts/', 'embed/')
                    show_video = st.button(f"{social_media_icon('youtube')} Watch Video", key=f"video_btn_{candidate.name}")
                    if show_video:
                        st.video(video_url)
                else:
                    st.markdown(f"{social_media_icon('website')} [{candidate.contact.website}]({candidate.contact.website})")

            if candidate.contact.email:
                st.markdown(f"{social_media_icon('email')} {candidate.contact.email}")

            if candidate.contact.phone:
                st.markdown(f"{social_media_icon('phone')} {candidate.contact.phone}")

            # Social Media
            social_links = []
            if candidate.contact.facebook:
                social_links.append(f'<a href="{candidate.contact.facebook}" target="_blank">{social_media_icon("facebook")}</a>')
            if candidate.contact.instagram:
                social_links.append(f'<a href="{candidate.contact.instagram}" target="_blank">{social_media_icon("instagram")}</a>')
            if candidate.contact.linkedin:
                social_links.append(f'<a href="{candidate.contact.linkedin}" target="_blank">{social_media_icon("linkedin")}</a>')
            if candidate.contact.twitter:
                social_links.append(f'<a href="{candidate.contact.twitter}" target="_blank">{social_media_icon("twitter")}</a>')

            if social_links:
                st.markdown(" ".join(social_links), unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# Page Configuration
st.set_page_config(
    page_title="Candidates | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide"
)

# Election countdown
election_date = datetime(2025, 3, 4, tzinfo=timezone.utc)
current_time = datetime.now(timezone.utc)
time_until_election = election_date - current_time

days = time_until_election.days
hours = time_until_election.seconds // 3600
minutes = (time_until_election.seconds % 3600) // 60

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

# Display election countdown 
st.markdown(
    f"""
    <div style="background-color: #1B4E5D; color: white; padding: 10px; text-align: center; border-radius: 5px; margin-bottom: 20px;">
         {days} days until Election Day: March 4th, 2025
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🗳️ City Council Candidates")
st.markdown("### March 4th, 2025 Election")

# Get district from URL parameter if available
params = st.query_params
initial_district = params.get("district", "All Districts")

# Filter by district
district_filter = st.selectbox(
    "Filter by District",
    ["All Districts"] + [str(i) for i in range(1, 10)],
    index=["All Districts"] + [str(i) for i in range(1, 10)].index(initial_district) if initial_district in map(str, range(1, 10)) else 0
)

# Display candidates
if district_filter == "All Districts":
    # Get all candidates and sort them by district number
    candidates = sorted(get_all_candidates(), key=lambda x: int(x.district))
else:
    candidates = get_district_candidates(district_filter)

# Group candidates by district
candidates_by_district = {}
for candidate in candidates:
    if candidate.district not in candidates_by_district:
        candidates_by_district[candidate.district] = []
    candidates_by_district[candidate.district].append(candidate)

# Display candidates grouped by district
for district in sorted(candidates_by_district.keys(), key=int):
    st.markdown(f"## District {district}")
    col1, col2 = st.columns(2)
    district_candidates = candidates_by_district[district]
    for i, candidate in enumerate(district_candidates):
        with col1 if i % 2 == 0 else col2:
            candidate_card(candidate)