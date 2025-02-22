import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stoggle import stoggle

# Basic page config
st.set_page_config(
    page_title="Test App",
    page_icon="🧪",
    layout="wide"
)

# Simple content
st.title("Test Streamlit App")

# Test expandable content (simpler alternative to modal)
with st.expander("Watch Campaign Video 📺"):
    st.markdown("""
        <iframe
            width="315"
            height="560"
            src="https://www.youtube.com/embed/SAMPLE_VIDEO_ID"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
    """, unsafe_allow_html=True)

st.write("If you can see this and the video expander above, the Streamlit server is working correctly!")