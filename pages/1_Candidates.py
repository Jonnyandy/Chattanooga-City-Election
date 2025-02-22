import streamlit as st
from utils.candidate_data import get_all_candidates, get_district_candidates
from streamlit_modal import Modal
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Candidates | Chattanooga.Vote",
    page_icon="🗳️",
    layout="wide"
)

# Add custom CSS for grid layout and styling
st.markdown("""
    <style>
        .candidate-container {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            background: white;
        }
        .candidate-photo {
            max-width: 300px;
            width: 100%;
            margin: 0 auto;
            display: block;
        }
        .candidate-info {
            margin-top: 1rem;
            text-align: center;
        }
        .contact-info {
            margin: 1rem 0;
            text-align: center;
        }
        .social-links {
            margin-top: 0.5rem;
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

    # Calculate number of columns based on screen width
    num_columns = 3
    cols = st.columns(num_columns)

    # Display candidates in grid
    for idx, candidate in enumerate(candidates):
        with cols[idx % num_columns]:
            st.markdown('<div class="candidate-container">', unsafe_allow_html=True)

            # Candidate photo
            if candidate.assets_photo:
                st.image(candidate.assets_photo, use_column_width=True, clazz="candidate-photo")

            # Candidate name and district
            st.markdown(f"### {candidate.name}")
            st.markdown(f"**District {candidate.district}**")

            # Campaign video button
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
                    video_id = 'SAMPLE_VIDEO_ID'  # Default video ID
                    if candidate.name == "Doll Sandridge" and candidate.contact and candidate.contact.website:
                        if "youtube.com/shorts/" in candidate.contact.website:
                            video_id = candidate.contact.website.split("/")[-1]

                    st.markdown(
                        f"""
                        <iframe
                            width="{315 if video_id != 'SAMPLE_VIDEO_ID' else 560}"
                            height="{560 if video_id != 'SAMPLE_VIDEO_ID' else 315}"
                            src="https://www.youtube.com/embed/{video_id}"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen>
                        </iframe>
                        """,
                        unsafe_allow_html=True
                    )

            # Contact information
            if candidate.contact:
                st.markdown('<div class="contact-info">', unsafe_allow_html=True)
                if candidate.contact.website:
                    st.markdown(f"🌐 [Website]({candidate.contact.website})")
                if candidate.contact.email:
                    st.markdown(f"📧 {candidate.contact.email}")
                if candidate.contact.phone:
                    st.markdown(f"📞 {candidate.contact.phone}")
                st.markdown('</div>', unsafe_allow_html=True)

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
                    st.markdown('<div class="social-links">', unsafe_allow_html=True)
                    st.markdown(" • ".join(social_links))
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred while loading candidates: {str(e)}")