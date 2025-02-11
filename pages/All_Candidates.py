import streamlit as st
from utils.candidate_data import get_all_candidates, get_district_candidates, Candidate
from utils.photo_scraper import get_candidate_photo
from typing import Optional
from pathlib import Path
from PIL import Image # Added import for Image.open()

def social_media_icon(platform: str) -> str:
    """Return emoji for social media platform"""
    icons = {
        'email': '📧',
        'phone': '📞',
        'facebook': 'ꜰʙ',
        'instagram': 'ɪɢ',
        'linkedin': 'ʟɪ',
        'twitter': '𝕏',
        'website': '🌐'
    }
    return icons.get(platform, '🔗')

def candidate_card(candidate: Candidate):
    """Display a candidate card with photo and contact information"""
    with st.container():
        st.markdown("""
        <style>
        .candidate-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
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

        # Photo handling
        try:
            photo_path = None
            if candidate.assets_photo:
                photo_path = candidate.assets_photo
            else:
                photo_path = get_candidate_photo(candidate.name, candidate.district)

            if photo_path and Path(photo_path).exists():
                try:
                    # Try to open the image to verify it's valid
                    Image.open(photo_path)
                    st.image(photo_path, use_column_width=True)
                except Exception as e:
                    st.error(f"Error displaying photo for {candidate.name}: {str(e)}")
        except Exception as e:
            st.error(f"Error processing photo for {candidate.name}: {str(e)}")

        # Name and District
        st.markdown(f'<div class="candidate-name">{candidate.name}</div>', unsafe_allow_html=True)
        st.markdown(f"**District {candidate.district}**")

        # Contact Information
        if candidate.contact:
            st.markdown('<div class="candidate-contact">', unsafe_allow_html=True)

            if candidate.contact.website:
                st.markdown(f"{social_media_icon('website')} [{candidate.contact.website}]({candidate.contact.website})")

            if candidate.contact.email:
                st.markdown(f"{social_media_icon('email')} {candidate.contact.email}")

            if candidate.contact.phone:
                st.markdown(f"{social_media_icon('phone')} {candidate.contact.phone}")

            # Social Media
            social_links = []
            if candidate.contact.facebook:
                social_links.append(f"[{social_media_icon('facebook')}]({candidate.contact.facebook})")
            if candidate.contact.instagram:
                social_links.append(f"[{social_media_icon('instagram')}]({candidate.contact.instagram})")
            if candidate.contact.linkedin:
                social_links.append(f"[{social_media_icon('linkedin')}]({candidate.contact.linkedin})")
            if candidate.contact.twitter:
                social_links.append(f"[{social_media_icon('twitter')}]({candidate.contact.twitter})")

            if social_links:
                st.markdown(" ".join(social_links))

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

from datetime import datetime, timezone

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

st.markdown(
    f"""
    <div style="background-color: #1B4E5D; color: white; padding: 10px; text-align: center; border-radius: 5px; margin-bottom: 20px;">
        Time until Election Day: {days} days, {hours} hours, {minutes} minutes
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
    candidates = get_all_candidates()
else:
    candidates = get_district_candidates(district_filter)

# Create a grid layout for cards
col1, col2 = st.columns(2)
for i, candidate in enumerate(candidates):
    with col1 if i % 2 == 0 else col2:
        candidate_card(candidate)