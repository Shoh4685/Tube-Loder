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
    /* --- Global Variables --- */
    :root {
        --bg-color: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --accent-color: #6366f1; /* Soft Indigo */
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
    }

    /* --- Background & App Container --- */
    .stApp {
        background-color: var(--bg-color);
        background-image: radial-gradient(at 50% 0%, #1e293b 0px, transparent 50%),
                          radial-gradient(at 100% 0%, #312e81 0px, transparent 20%);
        font-family: 'Inter', sans-serif;
    }

    /* --- Typography --- */
    h1 {
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem !important;
    }
    
    p {
        color: var(--text-secondary) !important;
    }

    /* --- Input Field --- */
    .stTextInput>div>div>input {
        border-radius: 16px;
        background-color: rgba(255, 255, 255, 0.03);
        color: var(--text-primary);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 12px 15px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--accent-color);
        background-color: rgba(255, 255, 255, 0.05);
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }

    /* --- Main Action Button --- */
    .stButton>button {
        width: 100%;
        border-radius: 16px;
        height: 3.2em;
        background: var(--accent-color);
        color: white;
        border: none;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
        background-color: #4f46e5;
    }

    /* --- Result Card (Glassmorphism) --- */
    .video-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 24px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-top: 30px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .video-card h3 {
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    /* --- Download Link Button --- */
    .download-btn {
        display: inline-block;
        width: 100%;
        padding: 12px 0;
        background-color: rgba(255, 255, 255, 0.05);
        color: var(--text-primary) !important;
        text-decoration: none;
        border-radius: 12px;
        font-weight: 500;
        text-align: center;
        margin-top: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s;
    }

    .download-btn:hover {
        background-color: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* --- Video Player Container --- */
    .stVideo {
        border-radius: 20px;
        overflow: hidden;
        margin-top: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
st.title("TubeLoader")
st.markdown("Premium extraction. Minimalist design.")

# --- Logic Section ---
video_url = st.text_input("", placeholder="Paste video link here...")
fetch_button = st.button("Extract Media")

if video_url or fetch_button:
    if not video_url:
        st.info("Please input a URL to proceed.")
    else:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }
            
            with st.spinner("Analyzing stream data..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'Video Content')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')

            if download_url:
                # --- The Modern Card ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.2], gap="large")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {title}")
                    st.markdown(f"<p style='font-size:0.9rem; opacity:0.8;'>Duration: {duration}</p>", unsafe_allow_html=True)
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">Open Raw Stream ↗</a>', unsafe_allow_html=True)
                    st.caption("Right-click video player to 'Save As'")
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("#### Preview")
                st.video(download_url)
                
            else:
                st.error("Link extraction failed. Try a different URL.")

        except Exception as e:
            st.error("Access denied or invalid URL.")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center style='opacity: 0.3; font-size: 0.75rem; font-family: monospace;'>Made with code & conscience</center>", unsafe_allow_html=True)
