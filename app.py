import streamlit as st
from deepfake_video import analyze_video
from deepfake_audio import analyze_audio
from utils import save_uploaded_file
import os

# Page setup
st.set_page_config(page_title="Real Eyes - Deepfake Detector", layout="wide")

# Custom CSS
st.markdown("""
<style>
body {
    background-color: #0d1117;
    color: #f0f6fc;
}
.stButton>button {
    background-color: #58a6ff;
    color: black;
    font-weight: bold;
    border-radius: 10px;
}
.stButton>button:hover {
    background-color: #7ecbff;
    transform: scale(1.05);
}
h1, h2, h3 {
    color: #58a6ff;
}
hr {
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>👁️ RealEyes - Deepfake Detection</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload a video or audio to verify its authenticity using our AI-based analysis.</p>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📁 Upload Media File")

uploaded_file = st.file_uploader("Upload a video (.mp4, .mov) or audio (.wav, .mp3)", type=["mp4", "mov", "wav", "mp3"])

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    st.success(f"File uploaded successfully: `{file_path}`")

    # Video preview
    if file_path.endswith((".mp4", ".mov")):
        st.subheader("🎞️ Preview")
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
        st.markdown(f"**Status:** `{result['status']}`")
        st.markdown(f"**Fake Score:** `{result['fake_score']:.3f}`")
        st.markdown(f"**Summary:** **{result['summary']}**")

        if result["summary"] == "Likely Fake":
            st.error("🚨 Warning: Deepfake content likely detected!")
        else:
            st.success("✅ Content appears genuine.")

    with col2:
        st.subheader("📊 Scores by Time")
        scores_table = { "Time (sec)": [], "Fake Score": [] }
        for time, score in result["scores_by_time"]:
            scores_table["Time (sec)"].append(time)
            scores_table["Fake Score"].append(round(score, 3))
        st.table(scores_table)

else:
    st.info("⬆️ Please upload a media file to begin analysis.")
