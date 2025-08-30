import cv2
import torch
from .models.signature_classifier import SignatureClassifier
from .models.dataset_tracer import DatasetTracer

class DeepfakeForensicsPipeline:
    def __init__(self, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.signature_model = SignatureClassifier(self.device)
        self.dataset_tracer = DatasetTracer()

    def run(self, video_path: str):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")

        ret, frame = cap.read()
        if not ret:
            raise ValueError("Video has no frames")
        
        # Resize frame and normalize for ResNet
        frame_resized = cv2.resize(frame, (224, 224))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        frame_tensor = torch.tensor(frame_rgb).permute(2, 0, 1).unsqueeze(0).float() / 255.0

        # Predict model
        model_info = self.signature_model.predict(frame_tensor)

        # Dummy dataset trace (high-level)
        dataset_info = self.dataset_tracer.trace({})

        # Dummy artifact scores (could integrate your artifact extractor later)
        artifact_scores = {"artifact_score": 0.9}

        cap.release()
        return {**model_info, **dataset_info, "artifact_scores": artifact_scores}
