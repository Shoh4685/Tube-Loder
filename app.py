import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder Audio", page_icon="🎵")
st.title("🎵 Tube-Loder: Audio Downloader")

video_url = st.text_input("Paste YouTube Link:")

if video_url:
    try:
        # Check for cookies.txt (Essential for bypass)
        cookie_path = 'cookies.txt'
        if not os.path.exists(cookie_path):
            st.error("❌ **Error:** Please upload `cookies.txt` to your GitHub repository.")
            st.stop()

        with tempfile.TemporaryDirectory() as tmp_dir:
            ydl_opts = {
                # 1. 'bestaudio' is the most compatible request
                'format': 'bestaudio/best', 
                'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                'cookiefile': cookie_path,
                'noplaylist': True,
                'quiet': True,
                
                # 2. This POST-PROCESSOR converts whatever YouTube gives us into M4A
                # (M4A is generally more stable than MP3 on cloud servers)
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                    'preferredquality': '192',
                }],
                
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios', 'web'],
                        'po_token': ['web+generated'],
                    }
                }
            }

            if st.button("🎸 Convert to Audio"):
                with st.spinner("Finding best stream and converting..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        title = info.get('title', 'audio')
                        
                        # Locate the converted file
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
                            st.error("Conversion failed. Check your 'packages.txt' for ffmpeg.")

    except Exception as e:
        st.error(f"Error: {e}")
