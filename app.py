import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder Final", page_icon="🎵")
st.title("🎵 Tube-Loder: Final Stability Patch")

url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("🚀 Prepare High-Quality MP3"):
        if not os.path.exists('cookies.txt'):
            st.error("❌ 'cookies.txt' is missing! Upload it to GitHub to bypass bot detection.")
            st.stop()

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                ydl_opts = {
                    # 2026 FIX: Use 'best' instead of 'bestaudio'. 
                    # Combined streams (video+audio) are less restricted than audio-only streams.
                    'format': 'best', 
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    'cookiefile': 'cookies.txt',
                    'nocheckcertificate': True,
                    'quiet': True,
                    # We download the combined file and let FFmpeg convert it to MP3 locally
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'extractor_args': {
                        'youtube': {
                            # iOS client remains the most trusted as of Feb 2026
                            'player_client': ['ios'],
                            'po_token': ['web+generated'],
                        }
                    }
                }

                with st.spinner("Bypassing YouTube's format wall..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        title = info.get('title', 'audio_file')
                        
                        # Find the MP3 produced by FFmpeg
                        files = [f for f in os.listdir(tmpdir) if f.endswith(".mp3")]
                        
                        if files:
                            target_path = os.path.join(tmpdir, files[0])
                            with open(target_path, "rb") as f:
                                audio_data = f.read()
                            
                            st.success(f"✅ Extracted: {title}")
                            st.audio(audio_data, format="audio/mpeg")
                            st.download_button(
                                label="📥 Download MP3 File",
                                data=audio_data,
                                file_name=f"{title}.mp3",
                                mime="audio/mpeg"
                            )
                        else:
                            st.error("Conversion failed. Is 'ffmpeg' in your packages.txt?")

        except Exception as e:
            st.error(f"Critical Failure: {e}")
            st.info("💡 Tip: If it still fails, your cookies have expired. Re-export them from YouTube!")
