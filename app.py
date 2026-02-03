import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="black_circle", 
    layout="centered"
)

# --- CRED-Inspired Neo-Brutalism CSS ---
st.markdown("""
    <style>
    /* Import Fonts: Space Grotesk (Headings) & JetBrains Mono (Tech/Data) */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #e0e0e0;
    }

    /* PITCH BLACK BACKGROUND WITH GRID */
    .stApp {
        background-color: #000000;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    /* TECH INPUT FIELD */
    .stTextInput>div>div>input {
        background-color: #090909 !important;
        border: 1px solid #333 !important;
        color: #fff !important;
        border-radius: 0px !important; /* Brutalist sharp edges */
        padding: 15px;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
        transition: all 0.3s;
    }

    .stTextInput>div>div>input:focus {
        border-color: #fff !important;
        background-color: #000 !important;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
    }

    /* PREMIUM 'HYPER-WHITE' ACTION BUTTON */
    .stButton>button {
        width: 100%;
        border-radius: 0px; /* Sharp */
        height: 3.5em;
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.2s cubic-bezier(0.25, 1, 0.5, 1);
        box-shadow: 0 0 0 transparent;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 5px 5px 0px #333; /* Brutalist shadow offset */
        border-color: #fff;
        background-color: #f0f0f0;
        color: #000;
    }

    .stButton>button:active {
        transform: translateY(0px);
        box-shadow: 0px 0px 0px transparent;
    }

    /* MONOLITH CARD STYLE */
    .video-card {
        background: #050505;
        border: 1px solid #222;
        padding: 0px;
        margin-top: 30px;
        position: relative;
        overflow: hidden;
    }
    
    /* Decorative 'CRED' Bar at top of card */
    .video-card::before {
        content: "";
        display: block;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #cb9b51, #f6e27a, #cb9b51); /* Gold/Copper Gradient */
    }

    .card-content {
        padding: 25px;
    }

    /* HEADINGS */
    h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800 !important;
        color: #ffffff;
        letter-spacing: -2px;
        text-transform: lowercase;
        font-size: 3rem !important;
    }
    
    h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin-top: 0;
    }

    /* DOWNLOAD LINK BUTTON (The 'Claim' Button style) */
    .download-btn {
        display: block;
        padding: 14px;
        background: #1a1a1a;
        color: #cb9b51 !important; /* Gold text */
        text-decoration: none;
        border: 1px solid #333;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        text-align: center;
        margin-top: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.3s;
    }

    .download-btn:hover {
        background: #cb9b51;
        color: #000 !important;
        border-color: #cb9b51;
    }
    
    /* RADIO BUTTONS (Custom Hack) */
    div[role="radiogroup"] > label > div:first-child {
        background-color: #000;
        border-color: #333;
    }
    div[role="radiogroup"] > label > div:first-child[data-checked="true"] {
        background-color: #fff !important;
        border-color: #fff !important;
    }

    /* FOOTER */
    .footer-text {
        font-family: 'JetBrains Mono', monospace;
        opacity: 0.3; 
        font-size: 0.7rem; 
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.title("tube.loader") # Lowercase for that 'cool' tech brand feel
    st.markdown("<p style='font-family: \"JetBrains Mono\"; opacity: 0.5; margin-top: -20px;'>/// SYSTEM.EXTRACT_STREAM</p>", unsafe_allow_html=True)

# --- Logic Section ---
st.markdown("<br>", unsafe_allow_html=True)
video_url = st.text_input("", placeholder="INPUT_SOURCE_URL")

st.markdown("<br>", unsafe_allow_html=True)
# Format Selection Toggle
format_choice = st.radio(
    "",
    ("Video (MP4)", "Audio Only (M4A)"),
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True)
fetch_button = st.button("INITIATE DOWNLOAD")

if video_url or fetch_button:
    if not video_url:
        st.info("Input required.")
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
            
            with st.spinner("DECRYPTING STREAM..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'Video Content')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')

            if download_url:
                # --- The Monolith Card ---
                st.markdown('<div class="video-card"><div class="card-content">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.2], gap="large")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {title}")
                    st.markdown(f"<span style='font-family: \"JetBrains Mono\"; color: #666;'>DURATION :: {duration}</span>", unsafe_allow_html=True)
                    
                    # Button text changes based on format
                    btn_text = "ACCESS AUDIO" if format_choice == "Audio Only (M4A)" else "ACCESS VIDEO"
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">{btn_text}</a>', unsafe_allow_html=True)
                
                st.markdown('</div></div>', unsafe_allow_html=True)

                st.markdown("<br>#### PREVIEW_STREAM", unsafe_allow_html=True)
                
                # Smart Preview
                if format_choice == "Audio Only (M4A)":
                    st.audio(download_url, format='audio/mp4')
                else:
                    st.video(download_url)
                
            else:
                st.error("STREAM ERROR: RESTRICTED")

        except Exception as e:
            st.error("SYSTEM ERROR: INVALID INPUT")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center class='footer-text'>NO_CAPITALISM.PY // V.2.0</center>", unsafe_allow_html=True)
