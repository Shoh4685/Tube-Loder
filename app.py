import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="💳", 
    layout="centered"
)

# --- CRED-Inspired Neo-Brutalism CSS ---
st.markdown("""
    <style>
    /* Import Premium Tech Font */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        background-color: #000000;
        color: #FFFFFF;
    }

    /* True Pitch Black Background with subtle noise */
    .stApp {
        background-color: #000000;
        background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
        background-attachment: fixed;
    }

    /* Input Field: The "Terminal" Look */
    .stTextInput>div>div>input {
        background-color: transparent !important;
        border: none;
        border-bottom: 2px solid #333;
        color: #E2B77A; /* Copper Text */
        border-radius: 0px;
        padding: 15px 5px;
        font-size: 18px;
        font-family: 'Space Grotesk', monospace;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }

    .stTextInput>div>div>input:focus {
        border-bottom: 2px solid #E2B77A;
        box-shadow: none;
        color: #fff;
    }

    /* The "CRED" Button */
    .stButton>button {
        width: 100%;
        border-radius: 0px; /* Sharp edges */
        height: 4em;
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #FFFFFF;
        font-weight: 800;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
        box-shadow: 5px 5px 0px 0px #333; /* Hard shadow */
    }
    
    .stButton>button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 8px 8px 0px 0px #E2B77A; /* Copper shadow on hover */
        border-color: #E2B77A;
    }

    /* Radio Buttons */
    .stRadio > div {
        background-color: #111;
        padding: 10px;
        border: 1px solid #333;
    }

    /* The "Premium Ticket" Card */
    .video-card {
        background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%);
        border: 1px solid #333;
        border-top: 4px solid #E2B77A; /* Copper Top Border */
        padding: 0px;
        margin-top: 30px;
        position: relative;
        overflow: hidden;
    }

    .card-content {
        padding: 25px;
    }

    /* Typography Override */
    h1 {
        font-weight: 800 !important;
        color: #FFFFFF;
        font-size: 3.5rem !important;
        letter-spacing: -2px;
        text-transform: lowercase;
    }
    
    h3 {
        font-weight: 700;
        color: #fff;
        font-size: 1.5rem;
        margin-bottom: 5px;
        line-height: 1.2;
    }

    /* The Action Link */
    .download-btn {
        display: block;
        padding: 18px;
        background: #111;
        color: #E2B77A !important;
        text-decoration: none;
        border: 1px solid #333;
        font-weight: 700;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 20px;
        transition: 0.3s;
    }

    .download-btn:hover {
        background: #E2B77A;
        color: #000 !important;
        border-color: #E2B77A;
    }
    
    .footer-text {
        font-family: 'Space Grotesk', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 10px;
        color: #444;
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    st.markdown("<h1>tubeloader<span style='color:#E2B77A'>.</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: monospace; color: #666;'>EXPERIENCE THE DOWNLOAD.</p>", unsafe_allow_html=True)

# --- Logic Section ---
video_url = st.text_input("", placeholder="PASTE_URL_HERE_")

# Format Selection
st.markdown("<br>", unsafe_allow_html=True)
format_choice = st.radio(
    "",
    ("Video (MP4)", "Audio Only (M4A)"),
    horizontal=True
)
st.markdown("<br>", unsafe_allow_html=True)

fetch_button = st.button("PROCEED TO EXTRACT")

if video_url or fetch_button:
    if not video_url:
        st.info("INPUT_REQUIRED")
    else:
        try:
            if format_choice == "Audio Only (M4A)":
                format_string = 'bestaudio[ext=m4a]/bestaudio/best'
            else:
                format_string = 'best[ext=mp4]/best'

            ydl_opts = {
                'format': format_string,
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }
            
            with st.spinner("AUTHENTICATING STREAM..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'Video Content')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')

            if download_url:
                # --- The "Ticket" Card ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # Image Section
                st.image(thumbnail, use_container_width=True)
                
                # Content Section
                st.markdown('<div class="card-content">', unsafe_allow_html=True)
                st.markdown(f"### {title}")
                st.markdown(f"<p style='color: #666; font-family: monospace;'>DURATION: {duration} // FMT: {format_choice.upper()}</p>", unsafe_allow_html=True)
                
                btn_text = "ACCESS AUDIO" if format_choice == "Audio Only (M4A)" else "ACCESS VIDEO"
                st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">{btn_text}</a>', unsafe_allow_html=True)
                st.markdown('</div></div>', unsafe_allow_html=True)

                st.markdown("<br><br>", unsafe_allow_html=True)
                
                if format_choice == "Audio Only (M4A)":
                    st.audio(download_url, format='audio/mp4')
                else:
                    st.video(download_url)
                
            else:
                st.error("RESTRICTED_ACCESS")

        except Exception as e:
            st.error("CONNECTION_REFUSED")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center class='footer-text'>MEMBERS ONLY // TUBE_LOADER v2.0</center>", unsafe_allow_html=True)
