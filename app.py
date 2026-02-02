import streamlit as st
import yt_dlp
import os
import tempfile

# Page Config
st.set_page_config(page_title="Tube-Loder", page_icon="📥")
st.title("Tube-Loder")
st.markdown("Download videos at the **highest resolution** available.")

# UI Inputs
video_url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")
quality_option = st.selectbox("Select Quality:", ["Best Available (4K/1080p)", "Standard (720p/MP4)"])

if st.button("Prepare Download"):
    if video_url:
        try:
            # Create a temporary directory on the server
            with tempfile.TemporaryDirectory() as tmpdirname:
                st.info("Processing... This may take a minute for high-res videos.")
                
                # Configuration for yt-dlp
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best' if "Best" in quality_option else 'best',
                    'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    file_path = ydl.prepare_filename(info)
                    
                    # Read the file into memory to give to the user
                    with open(file_path, "rb") as f:
                        btn = st.download_button(
                            label="📥 Download Video to Computer",
                            data=f,
                            file_name=os.path.basename(file_path),
                            mime="video/mp4"
                        )
                st.success("Ready! Click the button above to save the file.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a URL first.")