import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="blk_icon.png", 
    layout="centered"
)

# --- CRED-inspired "Industrial Luxury" CSS ---
st.markdown("""
    <style>
    /* 1. Global Font & Reset */
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&family=Space+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
        color: #f5f5f5;
    }

    /* 2. The "Void" Background */
    .stApp {
        background-color: #000000;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 40px 40px; /* Subtle grid pattern */
    }

    /* 3. The "Monolith" Input Field */
    .stTextInput>div>div>input {
        background-color: #0f0f0f;
        border: 1px solid #333;
        color: #e0e0e0;
        border-radius: 0px; /* Brutalist sharp edges */
        padding: 15px;
        font-family: 'Space Mono', monospace; /* Tech feel */
        font-size: 14px;
        transition: all 0.3s ease;
    }

    .stTextInput>div>div>input:focus {
        border-color: #ffffff; /* Stark white focus */
        background-color: #000000;
        box-shadow: none;
    }

    /* 4. The "Control" Button (High Contrast) */
    .stButton>button {
        width: 100%;
        border-radius: 0px;
        height: 3.5em;
        background-color: #ffffff; /* CRED White */
        color: #000000;
        border: none;
        font-weight: 800;
        font-family: 'Manrope', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 10px 30px rgba(255, 255, 255, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(255, 255, 255, 0.2);
        background-color: #f0f0f0;
        color: #000000;
    }
    
    .stButton>button:active {
        transform: translateY(1px);
    }

    /* 5. Radio Buttons (Custom Toggles) */
    div[role="radiogroup"] label {
        background-color: #0f0f0f !important;
        border: 1px solid #333;
        padding: 8px 16px;
        border-radius: 0px;
        font-family: 'Space Mono', monospace;
        font-size: 12px;
        color: #888;
        transition: 0.3s;
    }
    
    div[role="radiogroup"] {
        gap: 10px;
    }

    /* 6. The "Obsidian" Card */
    .video-card {
        background: #0a0a0a;
        border-left: 4px solid #ffffff; /* Asymmetric accent */
        padding: 30px;
        margin-top: 30px;
        position: relative;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }

    /* Typography Overrides */
    h1 {
        font-weight: 800 !important;
        color: #ffffff;
        letter-spacing: -1px;
        font-size: 3rem !important;
        text-transform: lowercase;
    }
    
    .sub-header {
        font-family: 'Space Mono', monospace;
        color: #666;
        font-size: 12px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    h3 {
        font-weight: 700;
        color: #ffffff;
        margin-top: 0;
        font-size: 1.2rem;
    }

    /* The "Action" Link */
    .download-btn {
        display: inline-block;
        padding: 12px 25px;
        background: transparent;
        color: #ffffff !important;
        text-decoration: none;
        border: 1px solid #ffffff;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 12px;
        margin-top: 20px;
        transition: 0.3s;
        font-family: 'Space Mono', monospace;
    }

    .download-btn:hover {
        background: #ffffff;
        color: #000000 !important;
    }
    
    /* Footer */
    .footer-text {
        font-family: 'Space Mono', monospace;
        opacity: 0.3; 
        font-size: 10px; 
        color: #ffffff;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    st.markdown("<div class='sub-header'>System // v.2.0</div>", unsafe_allow_html=True)
    st.title("TubeLoader.") # The period adds a brutalist touch

# --- Logic Section ---
# Spacing
st.write("")

video_url = st.text_input("", placeholder="ENTER SOURCE URL_")

st.write("") # Spacer

# Format Selection Toggle
format_choice = st.radio(
    "OUTPUT_FORMAT",
    ("Video (MP4)", "Audio Only (M4A)"),
    horizontal=True,
    label_visibility="collapsed" # Hides the label for cleaner look
)

st.write("") # Spacer

fetch_button = st.button("INITIATE DOWNLOAD")

if video_url or fetch_button:
    if not video_url:
        st.caption("Error: No input signal detected.")
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
            
            with st.spinner("DECRYPTING STREAM PROTOCOLS..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'Unknown Asset')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')

            if download_url:
                # --- The Obsidian Card ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.5], gap="large")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {title}")
                    st.markdown(f"<p style='font-family: Space Mono; font-size: 12px; color: #666;'>DURATION: {duration} // FMT: {format_choice.upper()}</p>", unsafe_allow_html=True)
                    
                    # Button text changes based on format
                    btn_text = "ACCESS AUDIO FEED" if format_choice == "Audio Only (M4A)" else "ACCESS VIDEO FEED"
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">{btn_text}</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<br><p style='font-family: Space Mono; font-size: 12px; color: #444;'>// PREVIEW MODE ACTIVE</p>", unsafe_allow_html=True)
                
                # Smart Preview
                if format_choice == "Audio Only (M4A)":
                    st.audio(download_url, format='audio/mp4')
                else:
                    st.video(download_url)
                
            else:
                st.error("Protocol Mismatch: Stream restricted.")

        except Exception as e:
            st.error("System Failure: Invalid URL provided.")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center class='footer-text'>Designed for the members.</center>", unsafe_allow_html=True)
