import streamlit as st
import yt_dlp

# --- Page Config ---
st.set_page_config(
    page_title="TubeLoader", 
    page_icon="📥",
    layout="centered"
)

# --- Smart UI Styling ---
st.markdown("""
    <style>
    /* Smart Mesh Gradient Background */
    .stApp {
        background: radial-gradient(at 0% 0%, rgba(64, 93, 230, 0.15) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(193, 53, 132, 0.15) 0px, transparent 50%),
                    #0f172a;
    }
    
    /* Frosted Glass Input Box */
    .stTextInput>div>div>input {
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    /* Instagram Gradient Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(45deg, #405DE6, #833AB4, #E1306C, #FD1D1D);
        color: white;
        border: none;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(225, 48, 108, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(225, 48, 108, 0.5);
        color: white;
    }

    /* Glassmorphism Card for Video Info */
    .video-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 25px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        margin-top: 20px;
    }

    /* Download Button - Gold Gradient */
    .download-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.8em;
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #000 !important;
        text-decoration: none !important;
        border-radius: 12px;
        font-weight: 700;
        text-align: center;
        margin-top: 15px;
        transition: opacity 0.2s;
    }
    .download-btn:hover {
        opacity: 0.9;
    }

    /* Gradient Title */
    h1 {
        background: -webkit-linear-gradient(45deg, #FFD700, #E1306C, #833AB4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    
    .stMarkdown h5 {
        color: #94a3b8;
        font-weight: 400;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.title("TubeLoader")
st.markdown("##### Smart metadata & high-speed stream extraction")

# --- Input Section ---
with st.container():
    video_url = st.text_input("", placeholder="Paste your link here...")
    fetch_button = st.button("Fetch Media")

if video_url or fetch_button:
    if not video_url:
        st.warning("Please enter a URL first!")
    else:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }
            
            with st.spinner("✨ Deciphering stream..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    download_url = info.get('url')
                    title = info.get('title', 'Video Content')
                    thumbnail = info.get('thumbnail')
                    duration = info.get('duration_string')
                    views = info.get('view_count', 0)

            if download_url:
                # --- Result UI with Glass Card ---
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.3], gap="large")
                
                with col1:
                    st.image(thumbnail, use_container_width=True)
                
                with col2:
                    st.subheader(title)
                    st.write(f"⏱️ **Duration:** {duration}")
                    st.write(f"👁️ **Views:** {views:,}")
                    
                    st.markdown(f"""
                        <a href="{download_url}" target="_blank" class="download-btn">📥 DOWNLOAD FILE</a>
                        <p style="font-size: 0.8rem; color: #64748b; margin-top: 15px;">
                        <b>Tip:</b> If the link opens a player, right-click and 'Save Video As'.
                        </p>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Preview
                with st.expander("📺 Show Video Preview", expanded=True):
                    st.video(download_url)
                
            else:
                st.error("Could not find a streamable link.")

        except Exception as e:
            st.error(f"Something went wrong. This video might be protected.")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<center style='color: #475569; font-size: 0.8rem;'>Made with not ❤️ but hate for capitalism</center>", unsafe_allow_html=True)
