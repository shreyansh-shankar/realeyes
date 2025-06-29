# deepfake_video.py

import cv2
import numpy as np
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
import os
from mesonet_model import Meso4

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Meso4(num_classes=2).to(device)
model.load_state_dict(torch.load("models/mesonet_best.pkl", map_location=device))
model.eval()

# ✅ Face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ✅ Basic image transform for MesoNet (input must be 224x224, normalized to 0-1)
transform = transforms.Compose([
    transforms.Resize((256, 256)),  # 👈 as used in training
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

def extract_faces_from_video(video_path, interval_sec=2):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps * interval_sec)

    frame_id = 0
    faces = []
    timestamps = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in detected:
                face = frame[y:y+h, x:x+w]
                pil_face = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
                tensor_face = transform(pil_face)
                faces.append(tensor_face)
                timestamps.append(int(frame_id / fps))
                break  # only take one face per frame

        frame_id += 1

    cap.release()
    return faces, timestamps

def analyze_video(file_path):
    faces, timestamps = extract_faces_from_video(file_path, interval_sec=0.5)

    if not faces:
        return {
            "status": "Error",
            "summary": "No faces detected in video"
        }

    fake_scores = []
    with torch.no_grad():
        for face_tensor in faces:
            input_tensor = face_tensor.unsqueeze(0).to(device)
            output = model(input_tensor)
            prob = F.softmax(output, dim=1)
            
            # Print once for checking index order
            print("Softmax Probabilities:", prob.cpu().numpy())

            fake_prob = prob[0][0].item()
            fake_scores.append(fake_prob)

    avg_score = float(np.mean(fake_scores))

    # Confidence-based summary
    if avg_score > 0.7:
        summary = "Likely Fake"
    elif avg_score < 0.4:
        summary = "Likely Real"
    else:
        summary = "Uncertain / Inconclusive"

    return {
        "status": "Success",
        "fake_score": round(avg_score, 3),
        "summary": "Likely Fake" if avg_score > 0.6 else "Likely Real",
        "scores_by_time": list(zip(timestamps, [round(s, 3) for s in fake_scores]))
    }
