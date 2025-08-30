import cv2
import numpy as np

def extract_temporal_features(video_path: str):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    ret, prev_frame = cap.read()
    if not ret:
        cap.release()
        return {"temporal_score": 0.0}

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    temporal_score = 0.0
    frame_count = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray, prev_gray)
        temporal_score += np.mean(diff)
        prev_gray = gray
        frame_count += 1

    cap.release()
    return {"temporal_score": temporal_score / max(frame_count, 1)}
