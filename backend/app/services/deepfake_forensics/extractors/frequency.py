import cv2
import numpy as np

def extract_frequency(video_path: str, frame_sample: int = 5):
    """
    Extract frequency-domain artifacts from video frames using FFT.

    Args:
        video_path: Path to input video
        frame_sample: Sample every nth frame

    Returns:
        dict: Frequency-domain anomaly score
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    freq_scores = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_sample == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            f = np.fft.fft2(gray)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-8)
            freq_scores.append(np.mean(magnitude_spectrum))

        frame_count += 1

    cap.release()

    return {"frequency_artifact_score": float(np.mean(freq_scores)) if freq_scores else 0.0}
