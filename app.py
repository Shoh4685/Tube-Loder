import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="tubeLoader...", 
    page_icon="⚖️", 
    layout="centered"
)

# --- Symmetrical Neo-Brutalism CSS ---
st.markdown("""
    <style>
    /* Import Tech Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* RESET & BASE */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #e0e0e0;
    }

    /* DEEP ONYX BACKGROUND (Not Pitch Black) */
    .stApp {
        background-color: #111111; /* Softer than #000 */
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
    }

    /* SYMMETRICAL INPUT FIELDS */
    .stTextInput>div>div>input {
        background-color: #111111;
        border: 2px solid #333333; /* Uniform border */
        color: #ffffff;
        border-radius: 0px; 
        padding: 15px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        text-align: center; /* Center text for symmetry */
        transition: all 0.2s ease;
    }

    .stTextInput>div>div>input:focus {
        background-color: #1a1a1a;
        border-color: #ffffff;
        box-shadow: none;
    }

    /* RADIO BUTTONS (The Toggle) */
    div[role="radiogroup"] {
        background: #1a1a1a;
        padding: 12px;
        border: 2px solid #333;
        display: flex;
        justify-content: center;
        border-radius: 0px;
        margin-bottom: 10px;
    }
    
    div[role="radiogroup"] label {
        color: #888 !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
    }

    div[role="radiogroup"] [data-baseweb="radio"] > div:first-child {
        background-color: #111 !important;
        border: 1px solid #666 !important;
    }

    /* THE BUTTON - High Contrast, Symmetrical */
    .stButton>button {
        width: 100%;
        border-radius: 0px; 
        height: 3.5em;
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.1s ease;
        box-shadow: 0px 4px 0px #333333; /* Vertical Shadow only for symmetry feel */
    }
    
    .stButton>button:hover {
        transform: translateY(2px);
        box-shadow: 0px 2px 0px #333333;
        background-color: #f0f0f0;
    }
    
    .stButton>button:active {
        transform: translateY(4px);
        box-shadow: none;
    }

    /* THE CARD - Perfectly Symmetrical Box */
    .video-card {
        background: #161616;
        border: 2px solid #ffffff; /* Uniform White Border */
        padding: 30px;
        margin-top: 30px;
        position: relative;
        text-align: center; /* Force Center Alignment */
    }
    
    /* TECH DECORATION (Centered) */
    .video-card::after {
        content: "RAW_DATA_STREAM";
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%); /* Perfectly Centered Tag */
        background: #111;
        border: 1px solid #fff;
        color: #fff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        padding: 2px 8px;
        letter-spacing: 1px;
    }

    /* HEADERS */
    h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700 !important;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 4px; /* Wider spacing */
        font-size: 2.5rem !important;
        text-align: center;
    }
    
    .caption-text {
        font-family: 'JetBrains Mono', monospace;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.7rem;
        margin-bottom: 25px;
        text-align: center;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }
    
    h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: #fff;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* DOWNLOAD LINK */
    .download-btn {
        display: inline-block;
        width: 100%;
        padding: 16px 0;
        background: #111;
        color: #fff !important;
        text-decoration: none;
        border: 2px solid #fff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        text-align: center;
        text-transform: uppercase;
        font-size: 13px;
        margin-top: 20px;
        transition: 0.2s;
    }

    .download-btn:hover {
        background: #fff;
        color: #000 !important;
    }
    
    /* Footer */
    .footer-text {
        font-family: 'JetBrains Mono', monospace;
        color: #555;
        text-transform: uppercase;
        font-size: 10px;
        letter-spacing: 3px;
    }
    
    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
# Using a single centered column for perfect symmetry
col_spacer1, col_main, col_spacer2 = st.columns([1, 6, 1])

with col_main:
    st.title("TUBELOADER")
    st.markdown("<div class='caption-text'>SYSTEM_READY // MODE: SYMMETRICAL_EXTRACTION</div>", unsafe_allow_html=True)

    # --- Logic Section ---
    video_url = st.text_input("", placeholder="INSERT_SOURCE_URL")

    # Format Selection Toggle
    format_choice = st.radio(
        "", 
        ("VIDEO_STREAM [MP4]", "AUDIO_STREAM [M4A]"),
        horizontal=True
    )

    st.markdown("<br>", unsafe_allow_html=True) 
    fetch_button = st.button("INITIALIZE DOWNLOAD")

    if video_url or fetch_button:
        if not video_url:
            st.info("INPUT_REQUIRED")
        else:
            try:
                # Determine format based on user choice
                if "AUDIO" in format_choice:
                    format_string = 'bestaudio[ext=m4a]/bestaudio/best'
                    is_audio = True
                else:
                    format_string = 'best[ext=mp4]/best'
                    is_audio = False

                ydl_opts = {
                    'format': format_string,
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
                }
                
                with st.spinner("DECRYPTING..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=False)
                        download_url = info.get('url')
                        title = info.get('title', 'UNKNOWN_ASSET')
                        thumbnail = info.get('thumbnail')
                        duration = info.get('duration_string')

                if download_url:
                    # --- The Symmetrical Card ---
                    st.markdown('<div class="video-card">', unsafe_allow_html=True)
                    
                    # Image centered full width inside card for symmetry
                    st.image(thumbnail, use_container_width=True)
                    
                    st.markdown(f"### {title}")
                    st.markdown(f"<span style='font-family: JetBrains Mono; color: #888; font-size: 12px;'>TIME_INDEX: {duration}</span>", unsafe_allow_html=True)
                    
                    btn_text = "ACCESS AUDIO DATA" if is_audio else "ACCESS VIDEO DATA"
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">{btn_text}</a>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("<br><center><p style='font-family: JetBrains Mono; font-size: 12px; color: #666;'>// PREVIEW_MONITOR //</p></center>", unsafe_allow_html=True)
                    
                    if is_audio:
                        st.audio(download_url, format='audio/mp4')
                    else:
                        st.video(download_url)
                    
                else:
                    st.error("ERROR: LINK_RESTRICTED")

            except Exception as e:
                st.error("ERROR: INVALID_SIGNAL")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center class='footer-text'>FORM FOLLOWS FUNCTION</center>", unsafe_allow_html=True)

