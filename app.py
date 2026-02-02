import streamlit as st
import yt_dlp
import os
import tempfile

# 1. Page Configuration
st.set_page_config(page_title="Tube-Loder MP3", page_icon="🎵", layout="centered")

st.title("🎵 Tube-Loder: High-Quality MP3")
st.markdown("""
    Extract high-quality audio from any YouTube video. 
    *Using authenticated session via cookies.txt.*
""")

# Input Field
video_url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    try:
        # Check if cookies.txt exists on the server
        cookie_path = 'cookies.txt'
        if not os.path.exists(cookie_path):
            st.error("❌ **Action Required:** Please upload `cookies.txt` to your GitHub repository.")
            st.stop()

        with tempfile.TemporaryDirectory() as tmpdirname:
            # 2. Configure yt-dlp for Audio Extraction & MP3 Conversion
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
                'cookiefile': cookie_path,
                'nocheckcertificate': True,
                'quiet': True,
                # The Post-Processor handles the conversion to MP3
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192', # High-quality bitrate
                }],
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios', 'web'],
                        'po_token': ['web+generated'],
                    }
                }
            }

            if st.button("🎸 Convert to MP3"):
                with st.spinner("Authenticating and converting... this takes a moment."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Extract and download
                        info = ydl.extract_info(video_url, download=True)
                        title = info.get('title', 'audio_file')
                        
                        # Find the actual processed MP3 file
                        files = [f for f in os.listdir(tmpdirname) if f.endswith(".mp3")]
                        
                        if files:
                            audio_path = os.path.join(tmpdirname, files[0])
                            
                            with open(audio_path, "rb") as f:
                                audio_bytes = f.read()
                                
                            st.success(f"✅ Ready: {title}")
                            
                            # Audio Preview
                            st.audio(audio_bytes, format="audio/mpeg")
                            
                            # Final Download Button
                            st.download_button(
                                label="📥 Save MP3 to Device",
                                data=audio_bytes,
                                file_name=f"{title}.mp3",
                                mime="audio/mpeg"
                            )
                        else:
                            st.error("Conversion failed. Ensure FFmpeg is installed via packages.txt.")

    except Exception as e:
        st.error(f"Error: {e}")
        if "403" in str(e):
            st.warning("YouTube has blocked the server IP. Try re-exporting fresh cookies.")
