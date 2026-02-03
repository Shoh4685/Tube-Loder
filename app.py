import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="tao", 
    layout="centered"
)

# --- SYMMETRICAL NEO-BRUTALISM CSS ---
st.markdown("""
    <style>
    /* Import Tech Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* BASE SETTINGS */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #f0f0f0;
    }

    /* BACKGROUND: Deep Charcoal with Symmetrical Grid */
    .stApp {
        background-color: #121212;
        background-image: 
            linear-gradient(#1a1a1a 1px, transparent 1px),
            linear-gradient(90deg, #1a1a1a 1px, transparent 1px);
        background-size: 40px 40px;
        background-position: center top; /* Grid aligns to center */
    }

    /* 1. INPUT FIELD: Perfectly Centered */
    .stTextInput>div>div>input {
        background-color: #000000;
        border: 2px solid #333; /* Even border on all sides */
        border-bottom: 2px solid #fff;
        color: #fff;
        border-radius: 0px; 
        padding: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        text-align: center; /* Text centers from the middle */
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }

    .stTextInput>div>div>input:focus {
        background-color: #111;
        border-color: #fff;
        letter-spacing: 2px; /* Expands on focus */
    }

    /* 2. RADIO TOGGLE: Centered Block */
    div[role="radiogroup"] {
        background: transparent;
        border: none;
        display: flex;
        justify-content: center; /* Center align items */
        gap: 20px; /* Symmetrical gap */
        margin-top: 10px;
    }
    
    div[role="radiogroup"] label {
        color: #666 !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        font-weight: 700;
        border: 1px solid #333;
        padding: 8px 16px;
        background: #000;
        transition: 0.3s;
    }
    
    /* Highlight the selected option symmetrically */
    div[role="radiogroup"] [data-baseweb="radio"] {
        margin-right: 0px;
    }

    /* 3. BUTTON: No Directional Shadow (Symmetry Preserved) */
    .stButton>button {
        width: 100%;
        border-radius: 0px; 
        height: 4.5em;
        background-color: #000;
        color: #fff;
        border: 2px solid #fff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 3px;
        transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
        position: relative;
        overflow: hidden;
    }
    
    /* Hover Effect: Invert Colors (Perfectly balanced) */
    .stButton>button:hover {
        background-color: #fff;
        color: #000;
        border-color: #fff;
        transform: scale(1.02); /* Symmetrical scale */
    }
    
    .stButton>button:active {
        transform: scale(0.98);
    }

    /* 4. THE CARD: Symmetrical Split Layout */
    .video-card {
        background: #000;
        border: 1px solid #333;
        padding: 0;
        margin-top: 50px;
        position: relative;
        display: flex;
        flex-direction: row; /* Force row layout */
    }
    
    /* Top Accent Bar */
    .video-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 40px;
        height: 4px;
        background: #fff;
    }

    /* Center Badge */
    .card-badge {
        text-align: center;
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        background: #121212;
        border: 1px solid #333;
        font-family: 'JetBrains Mono', monospace;
        font-size: 9px;
        color: #888;
        padding: 2px 10px;
        letter-spacing: 1px;
    }

    /* HEADERS */
    h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800 !important;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 4px; /* Wide spacing for grandeur */
        font-size: 3rem !important;
        text-align: center;
        margin: 0;
        padding: 0;
    }
    
    .subtitle {
        font-family: 'JetBrains Mono', monospace;
        color: #444;
        text-transform: uppercase;
        font-size: 10px;
        letter-spacing: 4px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 40px;
        border-top: 1px solid #333; /* Center line */
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
        padding-top: 10px;
    }

    /* CONTENT STYLING */
    h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: #fff;
        font-weight: 400;
        font-size: 1.4rem;
        margin: 0 0 10px 0;
        line-height: 1.2;
    }

    .meta-data {
        font-family: 'JetBrains Mono', monospace;
        color: #666; 
        font-size: 11px;
        letter-spacing: 1px;
        border-left: 2px solid #fff;
        padding-left: 10px;
        margin-bottom: 20px;
    }

    /* DOWNLOAD LINK */
    .download-btn {
        display: block;
        width: 100%;
        padding: 18px 0;
        background: #fff;
        color: #000 !important;
        text-decoration: none;
        border: 1px solid #fff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        text-align: center;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 1px;
        transition: 0.2s;
    }

    .download-btn:hover {
        background: #000;
        color: #fff !important;
        border-color: #fff;
    }
    
    /* PREVIEW CONTAINER */
    .preview-box {
        border: 1px solid #333;
        padding: 10px;
        margin-top: 20px;
        background: #000;
    }
    
    /* UTILS */
    .center-content {
        display: flex; 
        justify-content: center; 
        align-items: center;
        height: 100%;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Header Section (Pure HTML for Center Alignment) ---
st.markdown("<h1>TUBELOADER</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>SYMMETRY // EXTRACTION // PROTOCOL</div>", unsafe_allow_html=True)

# --- Logic Section ---
video_url = st.text_input("", placeholder="INSERT_TARGET_URL")

# Format Selection
format_choice = st.radio(
    "", # No label
    ("VIDEO [MP4]", "AUDIO [M4A]"),
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True) 
fetch_button = st.button("INITIATE SEQUENCE")

if video_url or fetch_button:
    if not video_url:
        st.info("WAITING FOR INPUT STREAM...")
    else:
        try:
            # Logic: Determine format
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
            
            with st.spinner("PROCESSING DATA..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'UNKNOWN_ASSET')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')

            if download_url:
                # --- The Symmetrical Card Structure ---
                st.markdown("""
                    <div class='video-card'>
                        <div class='card-badge'>PACKET_RECEIVED</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # We use Streamlit columns to hold the content inside the "Visual Card"
                # The visual card is just CSS; the content sits inside these columns
                c1, c2 = st.columns([1, 1], gap="medium")
                
                with c1:
                    # Force image to look brutally rectangular
                    st.image(thumbnail, use_container_width=True)
                
                with c2:
                    # Vertical Alignment Spacer
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<div class='meta-data'>DURATION: {duration} // {format_choice}</div>", unsafe_allow_html=True)
                    
                    btn_text = "DOWNLOAD AUDIO" if is_audio else "DOWNLOAD VIDEO"
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">{btn_text}</a>', unsafe_allow_html=True)

                # --- Preview Section ---
                st.markdown("<br><center style='font-family: JetBrains Mono; font-size: 10px; color: #444; letter-spacing: 2px;'>// MEDIA_PREVIEW_WINDOW</center>", unsafe_allow_html=True)
                
                # Encapsulate player in a bordered box for neatness
                with st.container():
                     if is_audio:
                        st.audio(download_url, format='audio/mp4')
                     else:
                        st.video(download_url)
                
            else:
                st.error("ERROR: RESTRICTED_ACCESS")

        except Exception as e:
            st.error("ERROR: INVALID_SIGNAL_PATH")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center class='footer-text'>DESIGNED FOR BALANCE.</center>", unsafe_allow_html=True)
