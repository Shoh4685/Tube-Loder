import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder 2026", page_icon="🎵")
st.title("🎵 Tube-Loder: Final Stability Patch")

# Simple, clean UI
url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("🚀 Start Conversion"):
        # 1. Check for the Cookie File
        if not os.path.exists('cookies.txt'):
            st.error("❌ Error: 'cookies.txt' not found in GitHub. YouTube is blocking the server.")
            st.stop()

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                # 2. Flexible Options: Download BEST audio and convert it locally
                ydl_opts = {
                    'format': 'bestaudio/best',  # Don't specify extension here
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    'cookiefile': 'cookies.txt',
                    'nocheckcertificate': True,
                    'quiet': True,
                    # Post-processor handles the conversion to M4A (most stable format)
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

                with st.spinner("Bypassing filters and extracting audio..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Extract and download in one step
                        info = ydl.extract_info(url, download=True)
                        title = info.get('title', 'audio_file')
                        
                        # Find the output file
                        files = [f for f in os.listdir(tmpdir) if f.endswith(".m4a")]
                        
                        if files:
                            target_file = os.path.join(tmpdir, files[0])
                            with open(target_file, "rb") as f:
                                audio_data = f.read()
                            
                            st.success(f"✅ Successfully extracted: {title}")
                            st.audio(audio_data, format="audio/mp4")
                            st.download_button(
                                label="📥 Download Audio File",
                                data=audio_data,
                                file_name=f"{title}.m4a",
                                mime="audio/mp4"
                            )
                        else:
                            st.error("Conversion failed. Is 'ffmpeg' in your packages.txt?")

        except Exception as e:
            st.error(f"Critical Failure: {e}")
            st.info("Try deleting the app from Streamlit Cloud and redeploying to get a fresh IP address.")
