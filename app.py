import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="📥", 
    layout="centered"
)

# --- YouTube "Dark Mode" Styling ---
st.markdown("""
    <style>
    /* Main Background (YouTube Dark Theme) */
    .stApp {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    
    /* Input Box styling */
    .stTextInput>div>div>input {
        border-radius: 40px; /* YouTube search bar style */
        background-color: #121212;
        color: white;
        border: 1px solid #333;
        padding-left: 20px;
    }

    /* YouTube Red Primary Button */
    .stButton>button {
        width: 100%;
        border-radius: 40px;
        height: 3em;
        background-color: #FF0000;
        color: white;
        border: none;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: background-color 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #cc0000;
        color: white;
        border: none;
    }

    /* Video Info Card */
    .video-card {
        background-color: #1f1f1f;
        padding: 20px;
        border-radius: 12px;
        border: none;
        margin-top: 20px;
    }

    /* Secondary Download Button (Grey/White style) */
    .download-btn {
        display: inline-block;
        padding: 0.6em 1.2em;
        background-color: #ffffff;
        color: #000000 !important;
        text-decoration: none;
        border-radius: 40px;
        font-weight: 600;
        text-align: center;
        margin-top: 10px;
        width: 100%;
