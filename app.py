import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder", page_icon="📥")
st.title("Tube-Loder")
st.markdown("Stable Download Mode (February 2026 Patch)")

video_url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Prepare Download"):
    if video_url:
        try:
            with tempfile.TemporaryDirectory() as tmpdirname:
                st.info("Fetching video data... please wait.")
                
                # CURRENT 2026 WORKAROUND: Disabling android_sdkless
                # This specifically targets the cause of recent 403 errors on cloud servers.
                ydl_opts = {
                    'format': 'best', 
                    'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'nocheckcertificate': True,
                    'quiet': True,
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['default', '-android_sdkless'],
                            'po_token': ['web+generated'],
                        }
                    },
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    }
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    file_path = ydl.prepare_filename(info)
                    
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        
                    st.download_button(
                        label="📥 Download Video",
                        data=file_data,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )
                st.success("Download ready!")
        except Exception as e:
            st.error(f"Download Failed: {e}")
            st.write("YouTube frequently blocks cloud servers. Try again in a few minutes.")
    else:
        st.warning("Please enter a URL.")
