import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="📥", 
    layout="centered"
)

# --- YouTube "Dark Mode" Styling ---
st.markdown("""
    <style>
    /* Main Background (YouTube Dark Theme) */
    .stApp {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    
    /* Input Box styling */
    .stTextInput>div>div>input {
        border-radius: 40px; /* YouTube search bar style */
        background-color: #121212;
        color: white;
        border: 1px solid #333;
        padding-left: 20px;
    }

    /* YouTube Red Primary Button */
    .stButton>button {
        width: 100%;
        border-radius: 40px;
        height: 3em;
        background-color: #FF0000;
        color: white;
        border: none;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: background-color 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #cc0000;
        color: white;
        border: none;
    }

    /* Video Info Card */
    .video-card {
        background-color: #1f1f1f;
        padding: 20px;
        border-radius: 12px;
        border: none;
        margin-top: 20px;
    }

    /* Secondary Download Button (Grey/White style) */
    .download-btn {
        display: inline-block;
        padding: 0.6em 1.2em;
        background-color: #ffffff;
        color: #000000 !important;
        text-decoration: none;
        border-radius: 40px;
        font-weight: 600;
        text-align: center;
        margin-top: 10px;
        width: 100%;
    }
    
    .download-btn:hover {
        background-color: #d9d9d9;
    }

    /* Custom Header */
    .yt-title {
        font-family: "YouTube Sans", "Roboto", sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<div class="yt-title"><span>📥</span> TubeLoader</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #aaa;'>Search and extract video streams</p>", unsafe_allow_html=True)

# --- Input Section ---
video_url = st.text_input("", placeholder="🔍 Search or paste link...")
fetch_button = st.button("Extract Video")

if video_url or fetch_button:
    if not video_url:
        st.warning("Please paste a URL first!")
    else:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }
            
            with st.spinner("⏳ Accessing YouTube servers..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'Video')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')
                    channel = info.get('uploader')

            if download_url:
                # --- Result UI ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.2], gap="medium")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {title}")
                    st.markdown(f"<p style='color: #aaa; margin-top: -15px;'>{channel} • {duration}</p>", unsafe_allow_html=True)
                    
                    # White YouTube-style Button
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">Get Download Link</a>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.divider()
                st.markdown("#### Preview")
                st.video(download_url)
                
            else:
                st.error("Could not find a streamable link.")

        except Exception as e:
            st.error(f"Something went wrong. This video might be private or region-locked.")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center style='color: #606060; font-size: 0.8rem;'>Made with not ❤️ but hate for capitalism</center>", unsafe_allow_html=True)
