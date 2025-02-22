import streamlit as st
from utils.candidate_data import get_all_candidates, get_district_candidates
from streamlit_modal import Modal
from pathlib import Path

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

# Page configuration
st.set_page_config(
    page_title="Candidates | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide"
)

# Add custom CSS to control image and content layout
st.markdown("""
    <style>
        .candidate-photo {
            max-width: 300px;
            margin: 0 auto;
            display: block;
        }
        .candidate-info {
            margin-top: 1rem;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Main content
st.title("🗳️ City Council Candidates")
st.markdown("### March 4th, 2025 Election")

# District filter
district_filter = st.selectbox(
    "Filter by District",
    ["All Districts"] + [str(i) for i in range(1, 10)],
    index=0
)

try:
    # Get candidates
    if district_filter == "All Districts":
        candidates = sorted(get_all_candidates(), key=lambda x: int(x.district))
    else:
        candidates = get_district_candidates(district_filter)

    # Display candidates
    for candidate in candidates:
        with st.container():
            st.markdown("---")

            # Candidate photo
            if candidate.assets_photo:
                st.image(candidate.assets_photo, use_column_width=True, clazz="candidate-photo")

            # Candidate information - centered under photo
            st.markdown('<div class="candidate-info">', unsafe_allow_html=True)
            st.markdown(f"### {candidate.name}")

            # Campaign video modal
            modal = Modal(
                title=f"Campaign Video - {candidate.name}",
                key=f"modal_{candidate.district}_{candidate.name.replace(' ', '_')}"
            )

            st.button(
                "📺 Watch Campaign Video",
                key=f"btn_{candidate.district}_{candidate.name.replace(' ', '_')}",
                on_click=modal.open
            )

            if modal.is_open():
                with modal.container():
                    video_id = 'SAMPLE_VIDEO_ID'  # Default video ID for testing
                    if candidate.name == "Doll Sandridge" and candidate.contact and candidate.contact.website:
                        if "youtube.com/shorts/" in candidate.contact.website:
                            video_id = candidate.contact.website.split("/")[-1]

                    st.markdown(
                        show_campaign_video(video_id, "9:16" if video_id != 'SAMPLE_VIDEO_ID' else "16:9"),
                        unsafe_allow_html=True
                    )

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
            st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred while loading candidates: {str(e)}")