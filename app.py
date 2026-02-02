import streamlit as st
import yt_dlp

# Page Config
st.set_page_config(page_title="Tube-Loder", page_icon="Gemini_Generated_Image_a4qg97a4qg97a4qg.png")
st.title("Tube-Loder")
st.write("Max download 360p")

video_url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    try:
        # Options to just extract the data
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        with st.spinner("Fetching direct link..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                # YouTube provides a direct URL to the video stream
                download_url = info.get('url')
                title = info.get('title', 'video')
                thumbnail = info.get('thumbnail')

        if download_url:
            st.image(thumbnail, width=300)
            st.success(f"**Found:** {title}")
            
            # Show a preview player
            st.video(download_url)
            
            # The direct download link
            st.markdown(f"""
                ### 📥 Download Link
                [Click here to open the raw video file]({download_url})
                
                **Instructions:** 1. Click the link above.
                2. Once the video opens, **Right-Click** on it.
                3. Select **'Save Video As...'** to save it to your device.
            """, unsafe_allow_html=True)
        else:
            st.error("Could not generate a direct download link for this video.")

    except Exception as e:
        st.error(f"An error occurred: {e}")




