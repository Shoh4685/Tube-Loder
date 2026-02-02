import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder MP3", page_icon="🎵")
st.title("🎵 Tube-Loder: MP3 Converter")
st.write("Using authenticated session to bypass bot detection.")

video_url = st.text_input("Paste YouTube URL here:")

if video_url:
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Check if cookies.txt exists
            cookie_path = 'cookies.txt'
            if not os.path.exists(cookie_path):
                st.error("Missing cookies.txt! Please upload it to your GitHub repo.")
                st.stop()

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
                'cookiefile': cookie_path,  # <--- AUTHENTICATION LINE
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'nocheckcertificate': True,
            }

            if st.button("🎸 Convert to MP3"):
                with st.spinner("Authenticating and converting..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        title = info.get('title', 'audio')
                        
                        files = [f for f in os.listdir(tmpdirname) if f.endswith(".mp3")]
                        if files:
                            audio_path = os.path.join(tmpdirname, files[0])
                            with open(audio_path, "rb") as f:
                                data = f.read()
                                st.audio(data, format="audio/mpeg")
                                st.download_button(
                                    label="📥 Save MP3 File",
                                    data=data,
                                    file_name=f"{title}.mp3"
                                )
                            st.success(f"Converted: {title}")

    except Exception as e:
        st.error(f"Error: {e}")
