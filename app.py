import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="Page icon.png", 
    layout="centered"
)

# --- Smart Animated Background & CSS ---
st.markdown("""
    <style>
    /* Animated Smart Background */
    .stApp {
        background: linear-gradient(125deg, #000000, #000000, #1a0b2e, #2e0b1a, #000000);
        background-size: 400% 400%;
        animation: gradientAnimation 15s ease infinite;
    }

    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism Card Effect */
    .video-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }

    /* Input Box Styling */
    .stTextInput>div>div>input {
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.07);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Instagram Gradient Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
        color: white;
        border: none;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(193, 53, 132, 0.4);
        color: white;
    }

    /* Headline Gradient */
    h1 {
        background: -webkit-linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    .download-btn {
        display: block;
        padding: 12px;
        background: linear-gradient(45deg, #F58529, #FEDA77);
        color: #000 !important;
        text-decoration: none;
        border-radius: 10px;
        font-weight: 800;
        text-align: center;
        margin-top: 15px;
        transition: 0.3s;
    }

    .download-btn:hover {
        transform: scale(1.02);
        filter: brightness(1.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
st.title ("TubeLoader")
st.markdown("<p style='color: #888;'>Premium stream extraction with a conscience.</p>", unsafe_allow_html=True)

# --- Logic Section ---
video_url = st.text_input("", placeholder="Paste link and let the magic happen...")
fetch_button = st.button("Download")

if video_url or fetch_button:
    if not video_url:
        st.warning("Input a URL to proceed.")
    else:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }
            
            with st.spinner("🧠 Analyzing stream protocols..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'Video Content')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')

            if download_url:
                # --- The Glassmorphism Card ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.2], gap="large")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {title}")
                    st.markdown(f"**Length:** {duration}")
                    st.markdown(f'<a href="{download_url}" target="_blank" class="download-btn">OPEN RAW STREAM</a>', unsafe_allow_html=True)
                    st.caption("Right-click video player to 'Save As'")
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("#### Preview")
                st.video(download_url)
                
            else:
                st.error("Link extraction failed. Try a different URL.")

        except Exception as e:
            st.error("Access denied or invalid URL.")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center style='opacity: 0.5; font-size: 0.8rem;'>Made with not ❤️ but hate for capitalism</center>", unsafe_allow_html=True)







