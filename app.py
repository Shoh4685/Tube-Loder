import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Tube-Loder", page_icon="📥")
st.title("Tube-Loder")
st.markdown("Download videos quickly and reliably.")

video_url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Prepare Download"):
    if video_url:
        try:
            with tempfile.TemporaryDirectory() as tmpdirname:
                st.info("Processing... please wait.")
                
                # Optimized options to avoid 403 errors and ensure single-file download
                ydl_opts = {
                    # 'best' finds the highest quality single file (usually 720p)
                    # This avoids 403 errors caused by multi-stream merging on servers
                    'format': 'best', 
                    'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'nocheckcertificate': True,
                    'quiet': True,
                    # Impersonates a standard browser to bypass bot detection
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-us',
                    }
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extract info and download to the temporary server folder
                    info = ydl.extract_info(video_url, download=True)
                    file_path = ydl.prepare_filename(info)
                    
                    # Read the file into memory
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        
                    # Provide the download button for the user's browser
                    st.download_button(
                        label="📥 Download Video to Computer",
                        data=file_data,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )
                st.success("Ready! Click the button above to save the file.")
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Tip: If you see a 403 error, try again in a few minutes or try a different video.")
    else:
        st.warning("Please enter a URL first.")
