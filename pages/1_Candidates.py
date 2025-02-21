import streamlit as st
from utils.candidate_data import get_all_candidates, get_district_candidates, Candidate
from utils.photo_scraper import get_candidate_photo
from typing import Optional
from pathlib import Path
from PIL import Image
from datetime import datetime, timezone

def show_campaign_video(video_id, aspect_ratio="16:9"):
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
        .candidate-info {
            padding: 20px;
        }
        .video-button {
            margin: 10px 0;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

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

            # Video button
            with st.expander("Watch Campaign Video"):
                if candidate.name == "Doll Sandridge" and candidate.contact and candidate.contact.website:
                    video_url = candidate.contact.website
                    if "youtube.com/shorts/" in video_url:
                        video_id = video_url.split("/")[-1]
                        st.markdown(show_campaign_video(video_id, "9:16"), unsafe_allow_html=True)
                else:
                    st.markdown(show_campaign_video('SAMPLE_VIDEO_ID', "16:9"), unsafe_allow_html=True)

            # Contact information
            if candidate.contact:
                if candidate.contact.website:
                    st.markdown(f"🌐 [Website]({candidate.contact.website})")
                if candidate.contact.email:
                    st.markdown(f"📧 {candidate.contact.email}")
                if candidate.contact.phone:
                    st.markdown(f"📞 {candidate.contact.phone}")

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

        st.markdown(f'<div class="candidate-name">{candidate.name}</div>', unsafe_allow_html=True)

        #Removed the old modal implementation as it's replaced by the expander in the new candidate_card

        
        if candidate.contact:
            st.markdown('<div class="candidate-contact">', unsafe_allow_html=True)

            
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

st.set_page_config(
    page_title="Candidates | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide"
)

election_date = datetime(2025, 3, 4, tzinfo=timezone.utc)
current_time = datetime.now(timezone.utc)
time_until_election = election_date - current_time

days = time_until_election.days
hours = time_until_election.seconds // 3600
minutes = (time_until_election.seconds % 3600) // 60

st.sidebar.markdown("""
<hr>
    <div style='text-align: center; padding-top: 0; margin-bottom: 10px;'>
        <h1 style='color: #1B4E5D; margin-bottom: 5px;'>chattanooga.vote</h1>
    </div>
""", unsafe_allow_html=True)

st.sidebar.image('assets/chattanoogashow_jonathanholborn.png', width=320, use_container_width=False)

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

params = st.query_params
initial_district = params.get("district", "All Districts")

district_filter = st.selectbox(
    "Filter by District",
    ["All Districts"] + [str(i) for i in range(1, 10)],
    index=(["All Districts"] + [str(i) for i in range(1, 10)]).index(initial_district) if initial_district in list(map(str, range(1, 10))) else 0
)

if district_filter == "All Districts":
    candidates = sorted(get_all_candidates(), key=lambda x: int(x.district))
else:
    candidates = get_district_candidates(district_filter)

candidates_by_district = {}
for candidate in candidates:
    if candidate.district not in candidates_by_district:
        candidates_by_district[candidate.district] = []
    candidates_by_district[candidate.district].append(candidate)

for district in sorted(candidates_by_district.keys(), key=int):
    st.markdown(f"## District {district}")
    col1, col2 = st.columns(2)
    district_candidates = candidates_by_district[district]
    for i, candidate in enumerate(district_candidates):
        with col1 if i % 2 == 0 else col2:
            candidate_card(candidate)