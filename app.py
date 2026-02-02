import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="📥", # Note: Ensure your local .png file is in the same directory
    layout="centered"
)

# --- Instagram Theme Styling ---
st.markdown("""
    <style>
    /* Main Background */
    .main {
        background-color: #000000;
    }
    
    /* Input Box */
    .stTextInput>div>div>input {
        border-radius: 12px;
        background-color: #121212;
        color: white;
        border: 1px solid #333;
    }

    /* Instagram Gradient Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
        color: white;
        border: none;
        font-weight: bold;
        font-size: 18px;
        transition: transform 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        color: white;
        border: none;
    }

    /* Video Card Info */
    .video-card {
        background-color: #121212;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #262626;
    }

    /* Direct Link Button */
    .download-btn {
        display: inline-block;
        padding: 0.8em 1.5em;
        background: linear-gradient(45deg, #F58529, #FEDA77);
        color: #000 !important;
        text-decoration: none;
        border-radius: 10px;
        font-weight: 700;
        text-align: center;
        margin-top: 15px;
        width: 100%;
    }

    /* Headline Styling */
    h1 {
        background: -webkit-linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.title("TubeLoader")
st.markdown("##### 🚀 Fast Metadata & Stream Extraction")
st.info("⚡ **Instagram Style:** High-quality streams and metadata extraction.")

# --- Input Section ---
with st.container():
    video_url = st.text_input("", placeholder="Paste YouTube link here...")
    fetch_button = st.button("Generate Download Link")

if video_url or fetch_button:
    if not video_url:
        st.warning("Please enter a
