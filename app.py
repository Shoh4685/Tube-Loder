import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="📥", # Note: Ensure your local .png file is in the same directory
    layout="centered"
)

# --- Instagram Theme Styling ---
st.markdown("""
    <style>
    /* Main Background */
    .main {
        background-color: #000000;
    }
    
    /* Input Box */
    .stTextInput>div>div>input {
        border-radius: 12px;
        background-color: #121212;
        color: white;
        border: 1px solid #333;
    }

    /* Instagram Gradient Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
        color: white;
        border: none;
        font-weight: bold;
        font-size: 18px;
        transition: transform 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        color: white;
        border: none;
    }

    /* Video Card Info */
    .video-card {
        background-color: #121212;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #262626;
    }

    /* Direct Link Button */
    .download-btn {
        display: inline-block;
        padding: 0.8em 1.5em;
        background: linear-gradient(45deg, #F58529, #FEDA77);
        color: #000 !important;
        text-decoration: none;
        border-radius: 10px;
        font-weight: 700;
        text-align: center;
        margin-top: 15px;
        width: 100%;
    }

    /* Headline Styling */
    h1 {
        background: -webkit-linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.title("TubeLoader")
st.markdown("##### 🚀 Fast Metadata & Stream Extraction")
st.info("⚡ **Instagram Style:** High-quality streams and metadata extraction.")

# --- Input Section ---
with st.container():
    video_url = st.text_input("", placeholder="Paste YouTube link here...")
    fetch_button = st.button("Generate Download Link")

if video_url or fetch_button:
    if not video_url:
        st.warning("Please enter a URL first!")
    else:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }
            
            with st.spinner("✨ Creating your link..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'Video')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')
                    views = info.get('view_count', 0)

            if download_url:
                # --- Result UI ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.2], gap="medium")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                    st.caption(f"⏱️ Duration: {duration}")
                
                with col2:
                    st.subheader(title)
                    st.markdown(f"**Views:** {views:,}")
                    
                    # Gradient Download Button
                    st.markdown(f"""
                        <a href="{download_url}" target="_blank" class="download-btn">DOWNLOAD NOW</a>
                        <p style="font-size: 0.8rem; color: #8e8e8e; margin-top: 12px; line-height: 1.2;">
                        <b>Pro Tip:</b> Click button, then hit the 3 dots (⋮) on the video player to save.
                        </p>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.divider()
                st.markdown("### 📽️ Quick Preview")
                st.video(download_url)
                
            else:
                st.error("Could not find a streamable link.")

        except Exception as e:
            st.error(f"Something went wrong. The video might be restricted.")
            with st.expander("Details"):
                st.code(e)

# --- Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("<center>Made with not ❤️ but hate for capitalism</center>", unsafe_allow_html=True)
