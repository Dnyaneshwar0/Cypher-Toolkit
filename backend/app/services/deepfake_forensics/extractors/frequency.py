import cv2
import numpy as np

def extract_frequency_features(video_path: str):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    freq_score = 0.0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for _ in range(min(frame_count, 50)):
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-8)
        freq_score += np.mean(magnitude_spectrum)

    cap.release()
    return {"frequency_score": freq_score / max(frame_count, 1)}
