import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="🖤", 
    layout="centered"
)

# --- CRED-Inspired Neo-Brutalism CSS ---
st.markdown("""
    <style>
    /* Import Tech Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* RESET & BASE */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #e0e0e0;
    }

    /* PITCH BLACK BACKGROUND WITH SUBTLE GRID */
    .stApp {
        background-color: #000000;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    /* NEO-BRUTALIST INPUT FIELDS */
    .stTextInput>div>div>input {
        background-color: #000000;
        border: 1px solid #333333;
        border-bottom: 2px solid #ffffff; /* Stark underline */
        color: #ffffff;
        border-radius: 0px; /* Sharp edges */
        padding: 15px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        transition: all 0.2s ease;
    }

    .stTextInput>div>div>input:focus {
        background-color: #0a0a0a;
        border-color: #ffffff;
        box-shadow: none;
    }

    /* RADIO BUTTONS (The Toggle) */
    div[role="radiogroup"] {
        background: #0a0a0a;
        padding: 10px;
        border: 1px solid #333;
        display: flex;
        justify-content: center;
        border-radius: 0px;
    }
    
    div[role="radiogroup"] label {
        color: #888 !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: 700;
    }

    div[role="radiogroup"] [data-baseweb="radio"] > div:first-child {
        background-color: #000 !important;
        border: 1px solid #555 !important;
    }

    /* THE 'CRED' BUTTON - High Contrast, Physical Feel */
    .stButton>button {
        width: 100%;
        border-radius: 0px; /* Brutalist Square */
        height: 3.5em;
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.1s ease;
        box-shadow: 4px 4px 0px #333333; /* Hard Shadow */
    }
    
    .stButton>button:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #333333;
        background-color: #f0f0f0;
        color: #000;
        border-color: #fff;
    }
    
    .stButton>button:active {
        transform: translate(4px, 4px);
        box-shadow: none;
    }

    /* THE CARD - Raw & Industrial */
    .video-card {
        background: #050505;
        border: 1px solid #333;
        border-left: 4px solid #ffffff; /* Accent border */
        padding: 25px;
        margin-top: 30px;
        position: relative;
    }
    
    /* RETRO TECH DECORATION ON CARD */
    .video-card::after {
        content: "RAW_DATA_STREAM";
        position: absolute;
        top: -10px;
        right: 10px;
        background: #000;
        color: #555;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        padding: 0 5px;
    }

    /* HEADERS */
    h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700 !important;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: -2px;
        font-size: 3rem !important;
        text-shadow: 2px 2px 0px #333;
    }
    
    .caption-text {
        font-family: 'JetBrains Mono', monospace;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.7rem;
        margin-bottom: 20px;
    }
    
    h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: #fff;
        font-weight: 500;
    }

    /* DOWNLOAD LINK - Monospaced Tag */
    .download-btn {
        display: inline-block;
        width: 100%;
        padding: 15px 0;
        background: #000;
        color: #fff !important;
        text-decoration: none;
        border: 1px solid #fff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        text-align: center;
        text-transform: uppercase;
        font-size: 12px;
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
        color: #444;
        text-transform: uppercase;
        font-size: 10px;
        letter-spacing: 2px;
    }
    
    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.title("TUBELOADER")
    st.markdown("<p class='caption-text'>// SYSTEM.READY // MODE: EXTRACTION</p>", unsafe_allow_html=True)

# --- Logic Section ---
video_url = st.text_input("", placeholder="ENTER_SOURCE_URL")

# Format Selection Toggle
format_choice = st.radio(
    "", # Empty label for cleaner look
    ("VIDEO_STREAM [MP4]", "AUDIO_STREAM [M4A]"),
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True) # Spacer
fetch_button = st.button("INITIALIZE DOWNLOAD")

if video_url or fetch_button:
    if not video_url:
        st.info("Input required > Waiting for signal...")
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
            
            with st.spinner("Decrypting Stream Protocols..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'UNKNOWN_ASSET')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')

            if download_url:
                # --- The Brutalist Card ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.3], gap="large")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {title}")
                    st.markdown(f"<span style='font-family: JetBrains Mono; color: #666; font-size: 12px;'>TIME_INDEX: {duration}</span>", unsafe_allow_html=True)
                    
                    btn_text = "ACCESS AUDIO DATA" if is_audio else "ACCESS VIDEO DATA"
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">{btn_text}</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<br><p style='font-family: JetBrains Mono; font-size: 12px; color: #fff;'>// PREVIEW_MONITOR</p>", unsafe_allow_html=True)
                
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
st.markdown("<center class='footer-text'>DESIGNED FOR EFFICIENCY. BUILT FOR SPEED.</center>", unsafe_allow_html=True)
