import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="App Icon.jpeg", 
    layout="centered"
)

# --- SYMMETRICAL NEO-BRUTALISM CSS ---
st.markdown("""
    <style>
    /* FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* GLOBAL RESET */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #e0e0e0;
    }

    /* BACKGROUND: Deep Matte Charcoal */
    .stApp {
        background-color: #121212;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    /* --- CENTERED HEADERS --- */
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 3rem;
        letter-spacing: 4px;
        text-align: center;
        color: #ffffff;
        margin-bottom: 5px;
        text-shadow: 0px 0px 10px rgba(255,255,255,0.1);
    }
    
    .sub-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        color: #666;
        margin-bottom: 40px;
        display: block;
        border-bottom: 1px solid #333;
        line-height: 0.1em;
        margin: 10px 0 40px; 
    }
    
    .sub-title span { 
        background: #121212; 
        padding: 0 10px; 
    }

    /* --- INPUT FIELD (SYMMETRICAL) --- */
    .stTextInput > div > div > input {
        background-color: #000000;
        border: 1px solid #333;
        border-left: 1px solid #333; /* Reset */
        border-right: 1px solid #333; /* Reset */
        border-bottom: 2px solid #fff; /* Focus accent */
        color: #fff;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        padding: 15px;
        border-radius: 0px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        background-color: #1a1a1a;
        border-color: #fff;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    /* --- RADIO TOGGLE (CENTERED) --- */
    div[role="radiogroup"] {
        display: flex;
        justify-content: center;
        gap: 20px;
        border: none;
        background: transparent;
    }
    
    div[role="radiogroup"] label {
        background: #1a1a1a;
        padding: 8px 16px;
        border: 1px solid #333;
        border-radius: 0px;
        color: #888;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        letter-spacing: 1px;
        text-transform: uppercase;
        cursor: pointer;
        transition: 0.2s;
    }
    
    /* Highlight the selected radio button (Streamlit specific hack) */
    div[role="radiogroup"] [data-baseweb="radio"] > div:first-child {
        background-color: #fff !important;
        border-color: #fff !important;
    }

    /* --- ACTION BUTTON (FULL WIDTH) --- */
    .stButton > button {
        width: 100%;
        border-radius: 0px;
        height: 50px;
        background-color: #ffffff;
        color: #000000;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        border: 1px solid #fff;
        box-shadow: 0px 5px 0px #222; /* Hard Shadow */
        transition: all 0.1s;
        margin-top: 20px;
    }
    
    .stButton > button:hover {
        background-color: #f0f0f0;
        transform: translateY(2px);
        box-shadow: 0px 3px 0px #222;
    }
    
    .stButton > button:active {
        transform: translateY(5px);
        box-shadow: 0px 0px 0px #222;
    }

    /* --- RESULT CARD (SYMMETRICAL SPLIT) --- */
    .video-card {
        background: #000;
        border: 1px solid #333;
        padding: 0; /* Remove padding to let grid touch edges if needed */
        margin-top: 40px;
        display: flex; /* Flexbox for alignment */
    }
    
    /* IMAGE CONTAINER */
    .card-image {
        border-right: 1px solid #333;
        padding: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #050505;
    }
    
    /* TEXT CONTAINER */
    .card-text {
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: left; /* Text remains left for readability */
    }

    h3 {
        margin: 0;
        font-size: 1.1rem;
        line-height: 1.3;
        color: #fff;
        font-weight: 600;
    }

    /* DOWNLOAD LINK BUTTON */
    .download-btn {
        display: block;
        width: 100%;
        padding: 12px 0;
        background: #111;
        color: #fff !important;
        text-decoration: none;
        border: 1px solid #444;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        text-align: center;
        font-size: 11px;
        text-transform: uppercase;
        margin-top: 15px;
        transition: 0.2s;
    }

    .download-btn:hover {
        background: #fff;
        color: #000 !important;
        border-color: #fff;
    }

    /* HIDE STREAMLIT UI CRUFT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

import streamlit as st

# Custom CSS for the "Deloitte-style" Tubeloader logo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@700&display=swap');

    .deloitte-style {
        font-family: 'Open Sans', Helvetica, Arial, sans-serif;
        font-size: 48px;
        font-weight: 700;
        letter-spacing: -1.5px;
        color: #FFFFFF; /* Main text color */
        display: flex;
        align-items: baseline;
    }

    .dot {
        color: #FFFFFF; /* The white dot */
        margin-left: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# The Title Implementation
st.markdown('<div class="deloitte-style">TUBELOADER<span class="dot">.</span></div>', unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="main-title">TUBELOADER</div>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-title"><span></span></h2>', unsafe_allow_html=True)

# --- INPUT SECTION ---
video_url = st.text_input("", placeholder="PASTE_SOURCE_URL_HERE")

# --- CONTROLS ---
# Using columns to perfectly center the radio buttons visually if needed, 
# though CSS handles the flex centering.
format_choice = st.radio(
    "",
    ("VIDEO [MP4]", "AUDIO [M4A]"),
    horizontal=True,
    label_visibility="collapsed"
)

fetch_button = st.button("INITIALIZE DOWNLOAD")

# --- LOGIC & RENDER ---
if video_url or fetch_button:
    if not video_url:
        st.markdown("<br><center style='color: #444; font-family: JetBrains Mono; font-size: 12px;'>WAITING FOR INPUT SIGNAL...</center>", unsafe_allow_html=True)
    else:
        try:
            # Logic: Determine Format
            is_audio = "AUDIO" in format_choice
            format_string = 'bestaudio[ext=m4a]/bestaudio/best' if is_audio else 'best[ext=mp4]/best'

            ydl_opts = {
                'format': format_string,
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
            }
            
            with st.spinner("PROCESSING DATA PACKETS..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'UNKNOWN_ASSET')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')

            if download_url:
                # --- SYMMETRICAL CARD RENDER ---
                # We use a container with a border, then 2 equal columns inside
                with st.container():
                    st.markdown("""<div style="height: 20px;"></div>""", unsafe_allow_html=True) # Spacer
                    
                    # Outer Card Border
                    st.markdown("""
                        <div style="border: 1px solid #333; background: #080808; padding: 0px;">
                    """, unsafe_allow_html=True)
                    
                    # The 50/50 Grid
                    col_img, col_txt = st.columns(2)
                    
                    with col_img:
                        # Image Section (Padding handled via st.image standard or inner div)
                        st.markdown('<div style="padding: 20px;">', unsafe_allow_html=True)
                        st.image(thumbnail, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    with col_txt:
                        # Text Section
                        st.markdown('<div style="padding: 20px; border-left: 1px solid #333; height: 100%; display: flex; flex-direction: column; justify-content: center;">', unsafe_allow_html=True)
                        st.markdown(f"<h3 style='color: #fff; font-size: 16px; margin: 0;'>{title}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #666; font-family: JetBrains Mono; font-size: 12px; margin-top: 5px;'>DURATION: {duration}</p>", unsafe_allow_html=True)
                        
                        btn_text = "ACCESS AUDIO" if is_audio else "ACCESS VIDEO"
                        st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">{btn_text}</a>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True) # Close Outer Card

                # Preview Section
                st.markdown("<br><center style='font-family: JetBrains Mono; font-size: 10px; color: #444; letter-spacing: 2px;'>// PREVIEW_MONITORING_ACTIVE</center><br>", unsafe_allow_html=True)
                
                if is_audio:
                    st.audio(download_url, format='audio/mp4')
                else:
                    st.video(download_url)
                
            else:
                st.error("ERROR: RESTRICTED ACCESS")

        except Exception as e:
            st.error("ERROR: CONNECTION FAILURE")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<center style='font-family: JetBrains Mono; font-size: 10px; color: #333;'>Made with ❤️ and a little bit hate</center>", unsafe_allow_html=True)







