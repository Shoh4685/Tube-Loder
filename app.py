import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="🎵", 
    layout="centered"
)

# --- CRED-Inspired Neo-Brutalism CSS (Symmetrical & High Contrast) ---
st.markdown("""
    <style>
    /* Import Tech Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* RESET & BASE */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #f0f0f0;
    }

    /* DEEP MATTE CHARCOAL BACKGROUND (Not Pitch Black) */
    .stApp {
        background-color: #121212;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
    }

    /* SYMMETRICAL INPUT FIELDS */
    .stTextInput>div>div>input {
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-bottom: 2px solid #ffffff; /* Stark High Contrast */
        color: #ffffff;
        border-radius: 0px; 
        padding: 15px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        text-align: center; /* Center text for symmetry */
        transition: all 0.2s ease;
    }

    .stTextInput>div>div>input:focus {
        background-color: #222;
        border-color: #ffffff;
    }

    /* RADIO BUTTONS (The Toggle) - Centered */
    div[role="radiogroup"] {
        background: #1a1a1a;
        padding: 12px;
        border: 1px solid #333;
        display: flex;
        justify-content: center;
        border-radius: 0px;
        margin-top: 10px;
    }
    
    div[role="radiogroup"] label {
        color: #999 !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* THE 'CRED' BUTTON - High Contrast & Tactile */
    .stButton>button {
        width: 100%;
        border-radius: 0px; 
        height: 4em;
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.1s ease;
        box-shadow: 6px 6px 0px #000000; /* Deep Shadow for Depth */
    }
    
    .stButton>button:hover {
        transform: translate(2px, 2px);
        box-shadow: 4px 4px 0px #000000;
        background-color: #e6e6e6;
    }
    
    .stButton>button:active {
        transform: translate(6px, 6px);
        box-shadow: none;
    }

    /* THE CARD - Perfectly Symmetrical Layout */
    .video-card {
        background: #1a1a1a;
        border: 1px solid #444;
        border-top: 4px solid #ffffff; /* Top accent for balance */
        padding: 30px;
        margin-top: 40px;
        position: relative;
    }
    
    /* TECH DECORATION */
    .video-card::before {
        content: "DATA_PACKET_RECEIVED";
        position: absolute;
        top: -25px;
        left: 50%;
        transform: translateX(-50%); /* Perfectly Centered Tag */
        background: #121212;
        color: #666;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        padding: 5px 10px;
        border: 1px solid #333;
    }

    /* HEADERS - Centered */
    h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800 !important;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: -1px;
        font-size: 3.5rem !important;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .caption-text {
        font-family: 'JetBrains Mono', monospace;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.75rem;
        text-align: center;
        margin-bottom: 30px;
        display: block;
    }
    
    h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: #fff;
        font-weight: 600;
        font-size: 1.2rem;
        margin-top: 0;
    }

    /* DOWNLOAD LINK */
    .download-btn {
        display: block;
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
        margin-top: 15px;
        transition: 0.2s;
    }

    .download-btn:hover {
        background: #fff;
        color: #000 !important;
        border-color: #000;
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
st.title("tubeloader...")
st.markdown("<span class='caption-text'>// SYSTEM_READY // PROTOCOL_INITIATED</span>", unsafe_allow_html=True)

# --- Logic Section ---
# Centered input via CSS targeting
video_url = st.text_input("", placeholder="INSERT_SOURCE_URL_HERE")

# Format Selection Toggle
format_choice = st.radio(
    "", # Empty label
    ("VIDEO_STREAM [MP4]", "AUDIO_STREAM [M4A]"),
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True) 
fetch_button = st.button("EXECUTE DOWNLOAD")

if video_url or fetch_button:
    if not video_url:
        st.info("AWAITING INPUT > WAITING FOR SIGNAL...")
    else:
        try:
            # Determine format
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
            
            with st.spinner("DECRYPTING STREAM PROTOCOLS..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'UNKNOWN_ASSET')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')

            if download_url:
                # --- The Symmetrical Card ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # Perfect 50/50 Split for Symmetry
                col1, col2 = st.columns([1, 1], gap="large")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {title}")
                    st.markdown(f"<span style='font-family: JetBrains Mono; color: #888; font-size: 12px;'>TIME_INDEX: {duration}</span>", unsafe_allow_html=True)
                    
                    btn_text = "ACCESS AUDIO DATA" if is_audio else "ACCESS VIDEO DATA"
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">{btn_text}</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<br><center style='font-family: JetBrains Mono; font-size: 12px; color: #666;'>// PREVIEW_MONITOR</center>", unsafe_allow_html=True)
                
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
st.markdown("<center class='footer-text'>SYMMETRY // EFFICIENCY // SPEED</center>", unsafe_allow_html=True)

