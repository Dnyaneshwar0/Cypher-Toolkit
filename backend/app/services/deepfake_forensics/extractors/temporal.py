import cv2
import numpy as np

def extract_temporal(video_path: str, frame_sample: int = 5):
    """
    Detect temporal inconsistencies using optical flow.

    Args:
        video_path: Path to input video
        frame_sample: Sample every nth frame

    Returns:
        dict: Temporal anomaly score
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    prev_gray = None
    flow_magnitudes = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_sample == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_gray is not None:
                flow = cv2.calcOpticalFlowFarneback(prev_gray, gray,
                                                    None,
                                                    0.5, 3, 15, 3, 5, 1.2, 0)
                mag, _ = cv2.cartToPolar(flow[...,0], flow[...,1])
                flow_magnitudes.append(np.mean(mag))
            prev_gray = gray

        frame_count += 1

    cap.release()
    return {"temporal_flow_score": float(np.mean(flow_magnitudes)) if flow_magnitudes else 0.0}
