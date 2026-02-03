import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="🖤", 
    layout="centered"
)

# --- CRED-inspired Premium CSS ---
st.markdown("""
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #000000;
        color: #ffffff;
    }

    /* The "Void" Background */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at 50% -20%, #2a2a2a 0%, #000000 50%);
        background-attachment: fixed;
    }

    /* Minimalist Input - The "Underline" Style */
    .stTextInput>div>div>input {
        background-color: #0f0f0f !important;
        border: 1px solid #222 !important;
        border-bottom: 2px solid #333 !important;
        color: #e0e0e0 !important;
        border-radius: 4px;
        padding: 15px;
        font-size: 16px;
        font-family: 'Space Grotesk', sans-serif;
        transition: all 0.3s ease;
    }

    .stTextInput>div>div>input:focus {
        border-bottom: 2px solid #ffffff !important;
        box-shadow: none;
    }

    /* High-Contrast "Premium" Button */
    .stButton>button {
        width: 100%;
        border-radius: 0px; /* Sharp corners */
        height: 3.5em;
        background: #ffffff;
        color: #000000;
        border: none;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
        clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%); /* Tech cut corner */
    }
    
    .stButton>button:hover {
        background: #e0e0e0;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(255, 255, 255, 0.1);
    }

    /* The Radio Button Customization */
    .stRadio > div {
        flex-direction: row;
        gap: 20px;
    }
    .stRadio label {
        color: #888 !important;
        font-weight: 600;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* The "Premium Card" Container */
    .video-card {
        background: #090909;
        border: 1px solid #1f1f1f;
        border-radius: 12px;
        padding: 30px;
        margin-top: 30px;
        position: relative;
        overflow: hidden;
    }
    
    /* Subtle Shine Effect on Card */
    .video-card::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, transparent 60%);
        pointer-events: none;
    }

    /* Typography Overrides */
    h1 {
        font-weight: 800 !important;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -2px;
        background: linear-gradient(180deg, #fff, #888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
    }
    
    h3 {
        font-weight: 600;
        color: #fff;
        margin-top: 0;
        letter-spacing: -0.5px;
    }

    /* The "Action" Link Button */
    .download-btn {
        display: block;
        padding: 14px;
        background: linear-gradient(45deg, #3a3a3a, #1a1a1a);
        color: #ffffff !important;
        text-decoration: none;
        border-radius: 4px;
        font-weight: 700;
        text-align: center;
        margin-top: 20px;
        border: 1px solid #333;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: 0.3s;
    }

    .download-btn:hover {
        background: #ffffff;
        color: #000000 !important;
        border-color: #ffffff;
    }
    
    /* Footer */
    .footer-text {
        opacity: 0.3; 
        font-family: 'Space Grotesk', monospace;
        font-size: 0.7rem; 
        color: #fff;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
# Using columns to center the sleek header
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.title("TUBELOADER")
    st.markdown("<p style='color: #666; font-family: Space Grotesk; margin-top: -20px; letter-spacing: 1px;'>PREMIUM STREAM EXTRACTION</p>", unsafe_allow_html=True)

# --- Logic Section ---
st.markdown("<br>", unsafe_allow_html=True)
video_url = st.text_input("", placeholder="PASTE URL HERE")

# Format Toggle - Clean & Minimal
st.markdown("<br>", unsafe_allow_html=True)
format_choice = st.radio(
    "",
    ("Video (MP4)", "Audio Only (M4A)"),
    horizontal=True,
    label_visibility="collapsed" # Hide default label for cleaner look
)

# Custom display for radio selection context
st.caption(f"SELECTED FORMAT: {format_choice.upper()}")

st.markdown("<br>", unsafe_allow_html=True)
fetch_button = st.button("INITIATE DOWNLOAD")

if video_url or fetch_button:
    if not video_url:
        st.info("INPUT REQUIRED")
    else:
        try:
            # Determine format based on user choice
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
                # --- The Premium Card ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.2], gap="large")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {title}")
                    st.markdown(f"<span style='color: #666; font-family: Space Grotesk;'>DURATION / {duration}</span>", unsafe_allow_html=True)
                    
                    # Button text changes based on format
                    btn_text = "ACCESS AUDIO" if format_choice == "Audio Only (M4A)" else "ACCESS VIDEO"
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">{btn_text}</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<br><h4 style='color: #444; font-family: Space Grotesk; letter-spacing: 1px;'>PREVIEW STREAM</h4>", unsafe_allow_html=True)
                
                # Smart Preview: Audio player for Audio mode, Video player for Video mode
                if format_choice == "Audio Only (M4A)":
                    st.audio(download_url, format='audio/mp4')
                else:
                    st.video(download_url)
                
            else:
                st.error("RESTRICTED CONTENT")

        except Exception as e:
            st.error("INVALID PROTOCOL OR URL")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center class='footer-text'>crafted for members only</center>", unsafe_allow_html=True)
