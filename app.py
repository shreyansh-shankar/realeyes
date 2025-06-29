from flask import Flask, render_template, request, send_from_directory
from deepfake_video import analyze_video
from deepfake_audio import analyze_audio
from werkzeug.utils import secure_filename
from utils import save_uploaded_file
import random
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    filename = None
    filepath = None

    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        if filename.endswith((".mp4", ".mov")):
            result = analyze_video(filepath)
        elif filename.endswith((".mp3", ".wav")):
            result = analyze_audio(filepath)

    return render_template("index.html", result=result, filename=filename)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)