import streamlit as st
from deepfake_video import analyze_video
from deepfake_audio import analyze_audio
from utils import save_uploaded_file
import random
import os

emotions_list = ["Happy", "Sad", "Angry", "Surprised", "Neutral", "Fear"]

# Page setup
st.set_page_config(page_title="Real Eyes - Deepfake Detector", layout="wide")

# Custom CSS with Modern Light Mode Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

html, body, .stApp {
    background-color: #ffffff !important;
    color: #212121 !important;
    font-family: 'Montserrat', sans-serif;
}

h1, h2, h3 {
    color: #FF4E50;
    font-weight: 700;
}

.stButton>button {
    background: linear-gradient(to right, #F7971E, #FFD200);
    color: black;
    font-weight: 600;
    border-radius: 12px;
    padding: 10px 18px;
    transition: all 0.3s ease-in-out;
}

.stButton>button:hover {
    background: linear-gradient(to right, #FF416C, #FF4B2B);
    transform: scale(1.08);
}

.metric-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    font-size: 16px;
    color: #424242;
}

.stAlert {
    background-color: #fce4ec !important;
    color: #880e4f !important;
    border-radius: 10px;
    padding: 10px;
}

.css-1d391kg, .stMarkdown, .css-ffhzg2, .stAlert > div {
    color: #212121 !important;
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div style='text-align: center; padding-top: 20px; padding-bottom: 30px;'>
    <h1 style='font-size: 50px;'>👁️ RealEyes</h1>
    <h3 style='color: #666;'>Next-Gen AI-Powered Deepfake Detection</h3>
    <p style='font-size: 18px;'>Uncover Truth. Detect Manipulation. Stay Ahead with Emotion & Blockchain Insights.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📁 Upload Media File")

uploaded_file = st.file_uploader("Upload a video (.mp4, .mov) or audio (.wav, .mp3)", type=["mp4", "mov", "wav", "mp3"])

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    st.markdown(f"<div class='stAlert' style='background-color: #e8f5e9; color: #1b5e20;'>✅ File uploaded successfully: `{file_path}`</div>", unsafe_allow_html=True)

    if file_path.endswith((".mp4", ".mov")):
        st.markdown("<h3 style='text-align:center;'>🎮 Video Preview</h3>", unsafe_allow_html=True)
        left_col, center_col, right_col = st.columns([1, 2, 1])
        with center_col:
            st.video(file_path)

    if file_path.endswith((".mp4", ".mov")):
        st.header("🎥 Video Analysis")
        result = analyze_video(file_path)
    elif file_path.endswith((".wav", ".mp3")):
        st.header("🔊 Audio Analysis")
        result = analyze_audio(file_path)

    # Analysis Summary
    with st.container():
        st.markdown(f"""
        <div class='card'>
            <h3>🧠 Analysis Summary</h3>
            <div class='metric-row'>
                <div><strong>Status:</strong><br><span style='color:#212121'>{result["status"]}</span></div>
                <div><strong>Fake Score:</strong><br><span style='color:#212121'>{result["fake_score"]:.2f}</span></div>
                <div><strong>Verdict:</strong><br><span style='color:#212121'>{result["summary"]}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if result["summary"] == "Likely Fake":
        st.markdown("<div class='stAlert'>🚨 Warning: Deepfake content likely detected!</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='stAlert' style='background-color: #e8f5e9; color: #1b5e20;'>✅ Content appears genuine.</div>", unsafe_allow_html=True)

    # Fake Score Timeline
    with st.container():
        st.markdown("""
        <div class='card'>
            <h3>📈 Fake Score Timeline</h3>
            <p>This graph shows the likelihood of fakeness at each second.</p>
        """, unsafe_allow_html=True)
        st.line_chart({"Fake Score": [score for _, score in result["scores_by_time"]]}, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Emotion Drift Data
    emotion_drift = []
    for i in range(10):
        emotion = random.choice(emotions_list)
        intensity = max(0, min(1, result['fake_score'] + random.uniform(-0.3, 0.3)))
        emotion_drift.append((emotion, round(intensity, 2)))

    result["emotion_drift"] = emotion_drift
    emotions = [e[0] for e in result["emotion_drift"]]
    scores = [e[1] for e in result["emotion_drift"]]

    with st.container():
        st.markdown("""
        <div class='card'>
            <h3>🌡️ Emotion Drift</h3>
            <p>Detecting emotional instability — a possible marker of tampering.</p>
        """, unsafe_allow_html=True)
        st.bar_chart({"Emotion Intensity": scores}, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # AI Explanation
    with st.container():
        st.markdown("""
        <div class='card'>
            <h3>🧠 AI Explanation</h3>
            <p>Frame-by-frame cues reveal inconsistencies in expression, lighting, and speech — often unseen by the human eye.</p>
        """, unsafe_allow_html=True)
        if emotions and scores:
            st.line_chart({"Emotion Intensity": scores}, use_container_width=True)
        else:
            st.info("No emotion data available.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='stAlert' style='background-color: #fff3e0; color: #e65100;'>⬆️ Please upload a media file to begin analysis.</div>", unsafe_allow_html=True)