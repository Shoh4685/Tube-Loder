import streamlit as st
import yt_dlp
import os
import tempfile

# Page Config for a professional look
st.set_page_config(page_title="Tube-Loder MP3", page_icon="🎵", layout="centered")

# Custom CSS for a cleaner interface
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF0000; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 Tube-Loder: MP3 Converter")
st.write("Enter a YouTube link to extract high-quality audio.")

# Input section
video_url = st.text_input("", placeholder="Paste YouTube link here...", label_visibility="collapsed")

if video_url:
    try:
        # Step 1: Fetch Metadata first to show the user a preview
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'Audio File')
            thumbnail = info.get('thumbnail')
            duration = info.get('duration_string')

        # Display UI Card for the video
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(thumbnail, use_container_width=True)
        with col2:
            st.subheader(title)
            st.write(f"⏱ Duration: {duration}")

        # Step 2: Download and Convert
        if st.button("🎸 Convert to MP3"):
            with tempfile.TemporaryDirectory() as tmpdirname:
                with st.spinner("Extracting audio... please wait."):
                    
                    # Options optimized for MP3 extraction
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'nocheckcertificate': True,
                        'quiet': True,
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['ios', 'web'],
                                'po_token': ['web+generated'],
                            }
                        }
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                        # The file extension changes to .mp3 after post-processing
                        expected_filename = os.path.join(tmpdirname, f"{title}.mp3")
                        
                        # Find the actual file in case title has special characters
                        downloaded_files = [f for f in os.listdir(tmpdirname) if f.endswith(".mp3")]
                        if downloaded_files:
                            final_path = os.path.join(tmpdirname, downloaded_files[0])
                            
                            with open(final_path, "rb") as f:
                                file_data = f.read()
                                
                            st.success("Conversion Successful!")
                            st.download_button(
                                label="📥 Save MP3 to Device",
                                data=file_data,
                                file_name=f"{title}.mp3",
                                mime="audio/mpeg"
                            )
                        else:
                            st.error("Audio processing failed.")

    except Exception as e:
        st.error("Could not fetch video details. Please check the URL.")
        if "403" in str(e):
            st.info("YouTube is currently limiting this server's access. Try again in a moment.")

else:
    st.info("💡 Pro Tip: You can even paste Shorts links to get the audio!")
