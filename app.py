import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder Audio", page_icon="🎵")
st.title("🎵 Tube-Loder: Audio Downloader")
st.markdown("---")

video_url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    try:
        # Check for cookies.txt first (Essential for bypass)
        cookie_path = 'cookies.txt'
        if not os.path.exists(cookie_path):
            st.error("❌ **Action Required:** Please upload `cookies.txt` to your GitHub repository.")
            st.stop()

        with tempfile.TemporaryDirectory() as tmp_dir:
            # 2026 STABILITY CONFIGURATION
            ydl_opts = {
                # 'bestaudio/best' is the most flexible format request
                'format': 'bestaudio/best', 
                'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                'cookiefile': cookie_path,
                'noplaylist': True,
                'quiet': True,
                'nocheckcertificate': True,
                # Force conversion to M4A or MP3 to ensure compatibility
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a', # Most convenient & compatible
                    'preferredquality': '192',
                }],
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios', 'web'],
                        'po_token': ['web+generated'],
                    }
                }
            }

            if st.button("🎸 Prepare Audio Download"):
                with st.spinner("Fetching best available format and converting..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        title = info.get('title', 'audio')
                        
                        # Find the actual file (yt-dlp may change extension after post-processing)
                        files = [f for f in os.listdir(tmp_dir) if f.endswith(".m4a")]
                        if files:
                            file_path = os.path.join(tmp_dir, files[0])
                            with open(file_path, "rb") as f:
                                data = f.read()
                                st.audio(data, format="audio/mp4")
                                st.download_button(
                                    label="📥 Save Audio File",
                                    data=data,
                                    file_name=f"{title}.m4a",
                                    mime="audio/mp4"
                                )
                        else:
                            st.error("Audio processing failed. Check logs for FFmpeg errors.")

    except Exception as e:
        st.error(f"Error: {e}")
