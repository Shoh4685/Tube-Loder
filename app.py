import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder MP3", page_icon="🎵")
st.title("🎵 Tube-Loder: MP3 Converter")

video_url = st.text_input("Paste YouTube URL here:")

if video_url:
    try:
        # Use a single YDL session to fetch info AND download
        # This reduces the number of requests to YouTube (preventing blocks)
        with tempfile.TemporaryDirectory() as tmpdirname:
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                # 2026 FIX: Use the iOS client and disable the broken android client
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios', 'web'],
                        'po_token': ['web+generated'],
                    }
                },
                'quiet': True,
                'nocheckcertificate': True,
            }

            if st.button("🎸 Convert to MP3"):
                with st.spinner("Fetching details and converting..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Fetch and Download in one go
                        info = ydl.extract_info(video_url, download=True)
                        title = info.get('title', 'audio')
                        
                        # Find the converted MP3 file
                        files = [f for f in os.listdir(tmpdirname) if f.endswith(".mp3")]
                        if files:
                            with open(os.path.join(tmpdirname, files[0]), "rb") as f:
                                st.audio(f.read(), format="audio/mpeg")
                                st.download_button(
                                    label="📥 Save MP3",
                                    data=open(os.path.join(tmpdirname, files[0]), "rb"),
                                    file_name=f"{title}.mp3"
                                )
                            st.success(f"Successfully converted: {title}")

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Check if the URL is correct or try a different video.")
