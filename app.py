import streamlit as st
import yt_dlp
import os
import tempfile

# 1. Page Configuration
st.set_page_config(page_title="Ultra HD Downloader", page_icon="🎬")
st.title("🎬 Ultra HD Video Downloader")
st.markdown("---")

video_url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    try:
        # 2. Use a temporary directory for the server to process files
        with tempfile.TemporaryDirectory() as tmp_dir:
            
            # 3. Enhanced Configuration for 2026 YouTube Bypasses
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'nocheckcertificate': True,
                'quiet': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios', 'web'],
                        'po_token': ['web+generated'],
                    }
                },
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
            }

            if st.button("🚀 Prepare High-Res Download"):
                with st.spinner("Processing... This involves downloading 4K video and HD audio separately and merging them. Please wait."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        file_path = ydl.prepare_filename(info)
                        
                        # Read the merged file
                        with open(file_path, "rb") as f:
                            file_data = f.read()
                            
                        # Provide the download button
                        st.download_button(
                            label="📥 Save High-Res Video to Device",
                            data=file_data,
                            file_name=os.path.basename(file_path),
                            mime="video/mp4"
                        )
                st.success("Success! Click the button above to save your file.")

    except Exception as e:
        st.error(f"Error: {e}")
