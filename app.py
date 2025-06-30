from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from deepfake_video import analyze_video
from deepfake_audio import analyze_audio
from werkzeug.utils import secure_filename
from utils import save_uploaded_file
import urllib.request
import os
import random

# Blockchain modules
from blockchain import Blockchain, Block

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize blockchain
blockchain = Blockchain()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    filename = None
    filepath = None
    chain_info = blockchain.get_chain()
    is_valid = blockchain.is_chain_valid()

    if request.method == "POST":
        # Check for file upload
        if "file" in request.files and request.files["file"].filename != "":
            file = request.files["file"]
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

        # Check for URL input
        elif "video_url" in request.form and request.form["video_url"]:
            url = request.form["video_url"]
            filename = secure_filename(url.split("/")[-1])
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            try:
                urllib.request.urlretrieve(url, filepath)
            except Exception as e:
                return render_template("index.html", result=None, error=f"Failed to download video: {e}", chain=chain_info, valid=is_valid)

        # Analyze based on file type
        if filepath and filename.endswith((".mp4", ".mov")):
            result = analyze_video(filepath)
        elif filepath and filename.endswith((".mp3", ".wav")):
            result = analyze_audio(filepath)

        # Register file hash on blockchain
        if filepath:
            new_block = blockchain.add_block(filename)
            chain_info = blockchain.get_chain()
            is_valid = blockchain.is_chain_valid()

    return render_template("index.html", result=result, filename=filename, chain=chain_info, valid=is_valid)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/chain")
def view_chain():
    return {
        "valid": blockchain.is_chain_valid(),
        "chain": [vars(block) for block in blockchain.get_chain()]
    }

if __name__ == "__main__":
    app.run(debug=True)