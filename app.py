import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder Fix", page_icon="🎵")
st.title("🎵 Tube-Loder: Emergency Patch")

url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("🚀 Force Download Audio"):
        if not os.path.exists('cookies.txt'):
            st.error("❌ 'cookies.txt' is missing from GitHub!")
            st.stop()

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                ydl_opts = {
                    # 'best' is a single-file format. It's much harder for YT to hide this 
                    # than separate high-res audio streams.
                    'format': 'best', 
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    'cookiefile': 'cookies.txt',
                    'nocheckcertificate': True,
                    'quiet': True,
                    # We download the video file but ONLY extract the audio
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '128', # Lowering bitrate slightly for better server stability
                    }],
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['ios'], # ONLY use iOS client
                            'po_token': ['web+generated'],
                        }
                    }
                }

                with st.spinner("Bypassing YouTube's format filters..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        title = info.get('title', 'audio_file')
                        
                        # Find the MP3 file
                        files = [f for f in os.listdir(tmpdir) if f.endswith(".mp3")]
                        
                        if files:
                            target_file = os.path.join(tmpdir, files[0])
                            with open(target_file, "rb") as f:
                                audio_data = f.read()
                            
                            st.success(f"✅ Success: {title}")
                            st.audio(audio_data, format="audio/mpeg")
                            st.download_button(
                                label="📥 Download MP3",
                                data=audio_data,
                                file_name=f"{title}.mp3",
                                mime="audio/mpeg"
                            )
                        else:
                            st.error("Server could not find FFmpeg. Check 'packages.txt'.")

        except Exception as e:
            st.error(f"Error: {e}")
