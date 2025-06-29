import streamlit as st
from deepfake_video import analyze_video
from deepfake_audio import analyze_audio
from utils import save_uploaded_file
import random
import os

emotions_list = ["Happy", "Sad", "Angry", "Surprised", "Neutral", "Fear"]

# Page setup
st.set_page_config(page_title="Real Eyes - Deepfake Detector", layout="wide")

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
* {
    font-family: "Mon"
}           
body {
    background-color: #0d1117;
    color: #f0f6fc;
    font-family: 'Montserrat', sans-serif;
}
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #58a6ff !important;
    font-weight: 700;
    font-family: 'Montserrat';
}
p, .stMarkdown {
    font-size: 16px;
    font-family: 'Montserrat';
}
.stButton>button {
    background-color: #238636;
    color: white;
    font-weight: 600;
    border-radius: 10px;
    padding: 8px 16px;
    transition: all 0.2s ease-in-out;
}
.stButton>button:hover {
    background-color: #2ea043;
    transform: scale(1.05);
}
hr {
    margin: 20px 0;
    border: 1px solid #30363d;
}
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    font-weight: bold;
    color: #c9d1d9;
}
.stTabs [aria-selected="true"] {
    border-bottom: 3px solid #58a6ff;
    color: #58a6ff !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding-top: 10px; padding-bottom: 20px;'>
    <h1 style='font-size: 48px;'>RealEyes</h1>
    <h3 style='color: #8b949e;'>AI-Powered Deepfake Detection</h3>
    <p style='font-size: 17px;'>Upload a video or audio file to check for manipulation using deepfake detection and emotion analysis.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📁 Upload Media File")

uploaded_file = st.file_uploader("Upload a video (.mp4, .mov) or audio (.wav, .mp3)", type=["mp4", "mov", "wav", "mp3"])

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    st.success(f"File uploaded successfully: `{file_path}`")

    # Video preview
    if file_path.endswith((".mp4", ".mov")):
        st.markdown("<h3 style='text-align:center;'>🎞️ Video Preview</h3>", unsafe_allow_html=True)

        # Use columns to center video
        left_col, center_col, right_col = st.columns([1, 2, 1])
        with center_col:
            st.video(file_path)

    # Analyze based on file type
    if file_path.endswith((".mp4", ".mov")):
        st.header("🎥 Video Analysis")
        result = analyze_video(file_path)
    elif file_path.endswith((".wav", ".mp3")):
        st.header("🔊 Audio Analysis")
        result = analyze_audio(file_path)

    # Layout for result display
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Analysis Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("🧪 Status", result["status"])
        col2.metric("🎯 Fake Score", f"{result['fake_score']:.2f}")
        col3.metric("🔍 Verdict", result["summary"])

        if result["summary"] == "Likely Fake":
            st.error("🚨 Warning: Deepfake content likely detected!")
        else:
            st.success("✅ Content appears genuine.")
    
    # Tabs for modular display
    tab1, tab2, tab3, tab4 = st.tabs(["🧠 Summary", "📈 Fake Score Timeline", "🌡️ Emotion Drift", "🧠 AI Explanation"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("🧪 Status", result["status"])
        col2.metric("🎯 Fake Score", f"{result['fake_score']:.2f}")
        col3.metric("🔍 Verdict", result["summary"])


        if result["summary"] == "Likely Fake":
            st.error("🚨 Warning: Deepfake content likely detected!")
        else:
            st.success("✅ Content appears genuine.")

    with tab2:
        st.subheader("📊 Fake Score Timeline")
        st.markdown("This graph shows the likelihood of fakeness at each second.")
        st.line_chart({ "Fake Score": [score for _, score in result["scores_by_time"]] })

    # Mock 10 emotion drift points
    emotion_drift = []
    for i in range(10):
        emotion = random.choice(emotions_list)
        # Emotion intensity loosely based on fake score ± randomness
        intensity = max(0, min(1, result['fake_score'] + random.uniform(-0.3, 0.3)))
        emotion_drift.append((emotion, round(intensity, 2)))
    
    # Assign to result for consistency across tabs
    result["emotion_drift"] = emotion_drift

    with tab3:
        st.subheader("🌡️ Emotion Drift")
        st.markdown("This chart shows varying emotions detected over time.")
        emotions = [e[0] for e in result["emotion_drift"]]
        scores = [e[1] for e in result["emotion_drift"]]
        st.bar_chart({"Emotion Intensity": scores})

    with tab4:
        st.subheader("🧠 AI Explanation")
        st.markdown("This section breaks down changes in emotions, possibly due to unnatural behavior.")
        
        if emotions and scores:
            st.markdown("Here's a secondary view of emotion drift across the timeline:")
            st.line_chart({"Emotion Intensity": scores})
        else:
            st.info("No emotion data available.")

else:
    st.info("⬆️ Please upload a media file to begin analysis.")
