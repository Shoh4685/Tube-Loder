import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder Audio", page_icon="🎵")
st.title("🎵 Tube-Loder: Fast Audio Downloader")
st.write("Extracting high-quality M4A (AAC) directly from YouTube.")

video_url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            # We use 'bestaudio[ext=m4a]' to get the pre-made high-quality file
            # This bypasses the need for FFmpeg and complex merging
            ydl_opts = {
                'format': 'ba[ext=m4a]', 
                'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios', 'web'],
                        'po_token': ['web+generated'],
                    }
                }
            }

            if st.button("🎸 Get Audio File"):
                with st.spinner("Fetching audio..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        title = info.get('title', 'audio')
                        file_path = ydl.prepare_filename(info)
                        
                        # Read and provide for download
                        with open(file_path, "rb") as f:
                            data = f.read()
                            st.audio(data, format="audio/mp4")
                            st.download_button(
                                label="📥 Save M4A Audio",
                                data=data,
                                file_name=f"{title}.m4a",
                                mime="audio/mp4"
                            )
                st.success("Download ready!")

    except Exception as e:
        st.error(f"Error: {e}")
