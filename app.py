import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder Audio", page_icon="🎵")
st.title("🎵 Tube-Loder: Final Fix")

video_url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    try:
        # 1. Verify Cookies (Crucial for bypass)
        if not os.path.exists('cookies.txt'):
            st.error("❌ cookies.txt not found! Upload it to GitHub to bypass the bot check.")
            st.stop()

        with tempfile.TemporaryDirectory() as tmp_dir:
            ydl_opts = {
                # 'bestaudio' is the most compatible request—it grabs WebM if M4A is hidden
                'format': 'bestaudio/best', 
                'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                'cookiefile': 'cookies.txt',
                'noplaylist': True,
                'quiet': True,
                'nocheckcertificate': True,
                
                # 2. The Converter: This turns the raw data into a standard M4A
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                    'preferredquality': '192',
                }],
                
                # 3. 2026 Bypass Args
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios', 'web'],
                        'po_token': ['web+generated'],
                    }
                }
            }

            if st.button("🎸 Prepare Audio"):
                with st.spinner("Extracting & Converting..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Extract and download in one step
                        info = ydl.extract_info(video_url, download=True)
                        title = info.get('title', 'audio_file')
                        
                        # Find the file (it might have a slightly different name due to characters)
                        files = [f for f in os.listdir(tmp_dir) if f.endswith(".m4a")]
                        if files:
                            file_path = os.path.join(tmp_dir, files[0])
                            with open(file_path, "rb") as f:
                                data = f.read()
                                st.audio(data, format="audio/mp4")
                                st.download_button(
                                    label="📥 Save Audio",
                                    data=data,
                                    file_name=f"{title}.m4a",
                                    mime="audio/mp4"
                                )
                            st.success(f"Success: {title}")
                        else:
                            st.error
