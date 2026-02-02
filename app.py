import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder Audio", page_icon="🎵")
st.title("🎵 Tube-Loder: Audio Downloader")
st.write("Using authenticated session to bypass bot detection.")

video_url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    try:
        # Check if cookies.txt exists on the server
        cookie_path = 'cookies.txt'
        if not os.path.exists(cookie_path):
            st.error("❌ Missing cookies.txt! Please upload your exported cookies.txt to GitHub.")
            st.stop()

        with tempfile.TemporaryDirectory() as tmpdirname:
            # We use 'ba[ext=m4a]' for the most convenient direct audio stream
            ydl_opts = {
                'format': 'ba[ext=m4a]', 
                'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
                'cookiefile': cookie_path,  # This tells YouTube you are a real user
                'noplaylist': True,
                'quiet': True,
                'nocheckcertificate': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios', 'web'],
                        'po_token': ['web+generated'],
                    }
                }
            }

            if st.button("🎸 Get Audio"):
                with st.spinner("Authenticating and fetching audio..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        title = info.get('title', 'audio')
                        file_path = ydl.prepare_filename(info)
                        
                        with open(file_path, "rb") as f:
                            data = f.read()
                            st.audio(data, format="audio/mp4")
                            st.download_button(
                                label="📥 Save M4A Audio",
                                data=data,
                                file_name=f"{title}.m4a",
                                mime="audio/mp4"
                            )
                st.success("Success!")

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("If you still see a bot error, try re-exporting fresh cookies from your browser.")
