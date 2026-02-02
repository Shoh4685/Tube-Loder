import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder MP3", page_icon="🎵")
st.title("🎵 Tube-Loder: Final MP3 Patch")

url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("🚀 Convert to MP3 (192kbps)"):
        # 1. Essential Check for Cookie File
        if not os.path.exists('cookies.txt'):
            st.error("❌ 'cookies.txt' not found! Please upload it to your GitHub repository.")
            st.stop()

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                # 2. Flexible Options: Grab whatever is best and transcode locally
                ydl_opts = {
                    'format': 'bestaudio/best',  # Flexible selection to avoid 403/Format errors
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    'cookiefile': 'cookies.txt',
                    'nocheckcertificate': True,
                    'quiet': True,
                    # Forced Transcoding to MP3 192kbps
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'extractor_args': {
                        'youtube': {
                            # iOS is currently the most 'trusted' client by YouTube
                            'player_client': ['ios', 'web'],
                            'po_token': ['web+generated'],
                        }
                    }
                }

                with st.spinner("Extracting and Converting... This takes about 30-60 seconds."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        title = info.get('title', 'audio_file')
                        
                        # Locate the MP3 (yt-dlp changes the extension after processing)
                        files = [f for f in os.listdir(tmpdir) if f.endswith(".mp3")]
                        
                        if files:
                            target_file = os.path.join(tmpdir, files[0])
                            with open(target_file, "rb") as f:
                                audio_data = f.read()
                            
                            st.success(f"✅ Ready: {title}")
                            st.audio(audio_data, format="audio/mpeg")
                            st.download_button(
                                label="📥 Download MP3 to Computer",
                                data=audio_data,
                                file_name=f"{title}.mp3",
                                mime="audio/mpeg"
                            )
                        else:
                            st.error("Conversion failed. Ensure 'ffmpeg' is in your packages.txt.")

        except Exception as e:
            st.error(f"Critical Error: {e}")
            st.info("💡 Hint: If it still fails, your cookies may have expired. Re-export them from YouTube!")
