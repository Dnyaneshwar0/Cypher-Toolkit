import cv2
import numpy as np

def extract_artifacts(video_path: str, frame_sample: int = 5):
    """
    Extract spatial and temporal artifacts from a video.

    Args:
        video_path: Path to input video
        frame_sample: Process every nth frame for efficiency

    Returns:
        dict: Artifact scores including blur, blocking, temporal inconsistency
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    blur_scores = []
    frame_diffs = []
    prev_gray = None
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_sample == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Blur detection: variance of Laplacian
            blur_scores.append(cv2.Laplacian(gray, cv2.CV_64F).var())

            # Temporal consistency: frame difference
            if prev_gray is not None:
                diff = np.mean(cv2.absdiff(gray, prev_gray))
                frame_diffs.append(diff)
            prev_gray = gray

        frame_count += 1

    cap.release()

    return {
        "blur_score": float(np.mean(blur_scores)) if blur_scores else 0.0,
        "temporal_inconsistency": float(np.mean(frame_diffs)) if frame_diffs else 0.0
    }
