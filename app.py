import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="Gemini_Generated_Image_a4qg97a4qg97a4qg.png", 
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-image: linear-gradient(to right, #FF4B4B, #FF8E53);
        color: white;
        border: none;
        font-weight: bold;
    }
    .video-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #374151;
        margin-bottom: 20px;
    }
    .download-btn {
        display: inline-block;
        padding: 0.6em 1.2em;
        background-color: #22c55e;
        color: white !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 500;
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.title("Gemini_Generated_Image_a4qg97a4qg97a4qg.png Tube-Loader")
st.markdown("##### High-speed video metadata & stream extraction")
st.info("💡 **Note:** This tool provides a direct stream link for up to 360p/720p playback and saving.")

# --- Input Section ---
with st.container():
    video_url = st.text_input("", placeholder="Paste your YouTube link here (e.g., https://youtube.com/...)")
    
    # Optional: Add a 'Fetch' button to trigger the action
    fetch_button = st.button("Fetch Video Details")

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
            
            with st.spinner("⚡ Processing video... please wait"):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'Video')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')
                    views = info.get('view_count', 0)

            if download_url:
                # --- Result UI ---
                col1, col2 = st.columns([1, 1.5], gap="medium")
                
                with col1:
                    st.image(thumbnail, use_container_width=True, caption=f"Duration: {duration}")
                
                with col2:
                    st.subheader(title)
                    st.caption(f"👁️ {views:,} views")
                    
                    # Modern Download Instructions
                    st.markdown(f"""
                        <a href="{download_url}" target="_blank" class="download-btn">🚀 Open Direct Video Link</a>
                        <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 10px;">
                        <b>How to save:</b><br>
                        1. Click the green button.<br>
                        2. On the video page, click the <b>three dots (⋮)</b> or <b>Right-Click</b>.<br>
                        3. Choose <b>'Save video as...'</b>.
                        </p>
                    """, unsafe_allow_html=True)

                st.divider()
                st.write("### 📺 Preview")
                st.video(download_url)
                
            else:
                st.error("Could not generate a direct download link for this video.")

        except Exception as e:
            st.error(f"**Error:** Something went wrong. The video might be restricted or private.")
            with st.expander("Show Technical Details"):
                st.code(e)

# --- Footer ---
st.markdown("---")
st.markdown("<center>Made with ❤️ for easy downloading</center>", unsafe_allow_html=True)


