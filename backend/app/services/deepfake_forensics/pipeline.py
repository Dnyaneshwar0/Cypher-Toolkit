import cv2
import torch
from torchvision import transforms
from .models.signature_classifier import SignatureClassifier
from .models.dataset_tracer import DatasetTracer
import numpy as np

class DeepfakeForensicsPipeline:
    def __init__(self, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.signature_model = SignatureClassifier(self.device)
        self.dataset_tracer = DatasetTracer()
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize(256, antialias=True),
            transforms.CenterCrop(224),
            transforms.Normalize(mean=(0.485,0.456,0.406), std=(0.229,0.224,0.225)),
        ])

    def run(self, video_path: str, max_frames: int = 16):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")

        frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        step = max(1, total_frames // max_frames)

        for i in range(0, total_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                continue
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_tensor = self.transform(frame_rgb).unsqueeze(0)  # [1,3,224,224]
            frames.append(frame_tensor)

        cap.release()
        if not frames:
            raise ValueError("No frames could be read from video.")

        frames_batch = torch.cat(frames, dim=0)  # [B,3,224,224]

        # CNN prediction
        model_info = self.signature_model.predict(frames_batch)

        # Dataset tracing (placeholder)
        dataset_info = self.dataset_tracer.trace({})

        # Artifact scores (placeholder)
        artifact_scores = {"artifact_score": 0.9}

        return {**model_info, **dataset_info, "artifact_scores": artifact_scores}
