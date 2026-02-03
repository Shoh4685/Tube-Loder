import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="🖤", 
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

    /* DEEP MATTE CHARCOAL BACKGROUND */
    .stApp {
        background-color: #121212;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    /* SYMMETRICAL HEADER */
    h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800 !important;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: -2px;
        font-size: 3.5rem !important;
        text-align: center; /* Mathematical Center */
        margin-bottom: 5px;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }
    
    .caption-text {
        font-family: 'JetBrains Mono', monospace;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 0.7rem;
        text-align: center;
        display: block;
        margin-bottom: 40px;
        border-bottom: 1px solid #333;
        padding-bottom: 20px;
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
        box-shadow: 0 0 15px rgba(255,255,255,0.05);
    }

    /* RADIO BUTTONS (The Toggle) - Centered */
    div[role="radiogroup"] {
        background: transparent;
        padding: 12px;
        display: flex;
        justify-content: center; /* Center alignment */
        border-radius: 0px;
        margin-top: 10px;
    }
    
    div[role="radiogroup"] label {
        color: #999 !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    /* Customizing the active radio button to be white */
    div[role="radiogroup"] [data-baseweb="radio"] > div:first-child {
        background-color: #1a1a1a !important;
        border-color: #666 !important;
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
        transition: all 0.2s cubic-bezier(0.25, 1, 0.5, 1);
        box-shadow: 0px 4px 0px #333;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 0px #333;
        background-color: #f2f2f2;
    }
    
    .stButton>button:active {
        transform: translateY(2px);
        box-shadow: 0px 0px 0px #333;
    }

    /* THE CARD - Perfectly Symmetrical Layout */
    .video-card {
        background: #1a1a1a;
        border: 1px solid #333;
        padding: 40px;
        margin-top: 40px;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    
    /* TECH DECORATION - Centered Tag */
    .video-card::before {
        content: "DATA_PACKET_RECEIVED";
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translateX(-50%); 
        background: #121212;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 9px;
        padding: 4px 12px;
        border: 1px solid #333;
        letter-spacing: 1px;
    }

    /* CARD TYPOGRAPHY */
    .card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 10px;
        line-height: 1.2;
    }

    .card-meta {
        font-family: 'JetBrains Mono', monospace;
        color: #666;
        font-size: 12px;
        margin-bottom: 25px;
        display: inline-block;
        border: 1px solid #333;
        padding: 5px 10px;
    }

    /* DOWNLOAD LINK */
    .download-btn {
        display: inline-block;
        width: 100%;
        padding: 18px 0;
        background: #121212;
        color: #fff !important;
        text-decoration: none;
        border: 1px solid #444;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        text-align: center;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 1px;
        transition: 0.3s;
    }

    .download-btn:hover {
        background: #fff;
        color: #000 !important;
        border-color: #fff;
    }
    
    /* Footer */
    .footer-text {
        font-family: 'JetBrains Mono', monospace;
        color: #333;
        text-transform: uppercase;
        font-size: 10px;
        letter-spacing: 3px;
        margin-top: 50px;
    }
    
    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
st.markdown("<h1>TUBELOADER</h1>", unsafe_allow_html=True)
st.markdown("<span class='caption-text'>// SYSTEM_READY // PROTOCOL_INITIATED</span>", unsafe_allow_html=True)

# --- Logic Section ---
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
                    # Using CSS classes defined above for perfect centering and typography
                    st.markdown(f"<div class='card-title'>{title}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='card-meta'>TIME_INDEX: {duration}</div>", unsafe_allow_html=True)
                    
                    btn_text = "ACCESS AUDIO DATA" if is_audio else "ACCESS VIDEO DATA"
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">{btn_text}</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<br><center style='font-family: JetBrains Mono; font-size: 10px; color: #444; letter-spacing: 2px;'>// PREVIEW_MONITOR //</center>", unsafe_allow_html=True)
                
                if is_audio:
                    st.audio(download_url, format='audio/mp4')
                else:
                    st.video(download_url)
                
            else:
                st.error("ERROR: LINK_RESTRICTED")

        except Exception as e:
            st.error("ERROR: INVALID_SIGNAL")

# --- Footer ---
st.markdown("<center class='footer-text'>SYMMETRY // EFFICIENCY // SPEED</center>", unsafe_allow_html=True)
