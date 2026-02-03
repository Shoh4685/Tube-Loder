import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="Page icon.png", 
    layout="centered"
)

# --- Modern Minimalist CSS ---
st.markdown("""
    <style>
    /* Global Reset & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Deep Soothing Background */
    .stApp {
        background-color: #0E1117;
        background-image: radial-gradient(circle at 50% 0%, #1c212e 0%, #0E1117 50%);
        background-attachment: fixed;
    }

    /* Minimalist Input Field */
    .stTextInput>div>div>input {
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #e6edf3;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
        transition: border-color 0.3s ease;
    }

    .stTextInput>div>div>input:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
    }

    /* Modern Primary Button (Monochrome) */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #f0f6fc;
        color: #0f1117;
        border: none;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        background-color: #ffffff;
        box-shadow: 0 8px 15px rgba(255,255,255,0.1);
    }

    /* Sleek Content Card */
    .video-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 24px;
        margin-top: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    /* Titles */
    h1 {
        font-weight: 700 !important;
        color: #f0f6fc;
        letter-spacing: -0.5px;
    }
    
    h3 {
        font-weight: 600;
        color: #f0f6fc;
        margin-top: 0;
    }

    /* Link Button */
    .download-btn {
        display: block;
        padding: 12px;
        background: #238636;
        color: #ffffff !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 500;
        text-align: center;
        margin-top: 15px;
        transition: 0.2s;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .download-btn:hover {
        background: #2ea043;
        transform: scale(1.01);
    }
    
    /* Footer Opacity */
    .footer-text {
        opacity: 0.4; 
        font-size: 0.8rem; 
        color: #8b949e;
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.title("TubeLoader")
    st.caption("Minimalist stream extraction tool.")

# --- Logic Section ---
video_url = st.text_input("", placeholder="Paste video URL here...")
fetch_button = st.button("Analyze & Download")

if video_url or fetch_button:
    if not video_url:
        st.info("Please enter a valid URL to begin.")
    else:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }
            
            with st.spinner("Processing stream data..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'Video Content')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')

            if download_url:
                # --- The Sleek Card ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.2], gap="large")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {title}")
                    st.markdown(f"<span style='color: #8b949e;'>Duration: {duration}</span>", unsafe_allow_html=True)
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">Open Stream</a>', unsafe_allow_html=True)
                    st.caption("Right-click the player below to save.")
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("#### Preview")
                st.video(download_url)
                
            else:
                st.error("Could not extract link. The video might be restricted.")

        except Exception as e:
            st.error("Unable to process this URL. Please check the link.")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center class='footer-text'>Simplicity in a complex world.</center>", unsafe_allow_html=True)
