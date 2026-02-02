import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Ultra HD Downloader", page_icon="🎬")
st.title("🎬 Ultra HD Video Downloader")
st.write("Downloads the highest available resolution (4K/1080p).")

video_url = st.text_input("Paste YouTube Link:")

if video_url:
    try:
        # Use a temporary directory so we don't clog the server
        with tempfile.TemporaryDirectory() as tmp_dir:
            
            # Format: 'bestvideo+bestaudio/best' forces the highest quality merge
           ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
    'merge_output_format': 'mp4',
    'noplaylist': True,
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web'],
            'po_token': ['web+generated'], # Attempts to generate a fresh token
        }
    }
}

            if st.button("Prepare High-Res Download"):
                with st.spinner("Downloading and Merging highest quality... this takes a moment."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        file_path = ydl.prepare_filename(info)
                        
                        # Once finished, let user download the merged file
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 Save High-Res Video to Device",
                                data=f,
                                file_name=os.path.basename(file_path),
                                mime="video/mp4"
                            )
                st.success("Merge complete! Click the button above.")

    except Exception as e:
        st.error(f"Error: {e}")
        if "ffmpeg" in str(e).lower():
            st.warning("FFmpeg is missing! Ensure 'packages.txt' contains 'ffmpeg' on your GitHub.")

