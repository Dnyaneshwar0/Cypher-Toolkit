import cv2
import torch
from facenet_pytorch import MTCNN
from pathlib import Path
from typing import List
import numpy as np

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
mtcnn = MTCNN(keep_all=True, device=DEVICE, post_process=True)

def extract_frames(video_path: str, fps: float = 1.0) -> List[np.ndarray]:
    cap = cv2.VideoCapture(video_path)
    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    rate = cap.get(cv2.CAP_PROP_FPS) or 25.0
    stride = max(int(rate // fps), 1)
    idx = 0
    while cap.isOpened():
        ok = cap.grab()
        if not ok: break
        if idx % stride == 0:
            ok, frame = cap.retrieve()
            if not ok: break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(rgb)
        idx += 1
    cap.release()
    return frames

def detect_faces(frames: List[np.ndarray], min_face_size: int = 80) -> List[np.ndarray]:
    faces = []
    for frame in frames:
        boxes, _ = mtcnn.detect(frame)
        if boxes is None: continue
        for b in boxes:
            x1, y1, x2, y2 = [int(v) for v in b]
            w, h = x2-x1, y2-y1
            if min(w,h) < min_face_size: continue
            crop = frame[max(0,y1):y2, max(0,x1):x2]
            if crop.size != 0:
                faces.append(crop)
    return faces
