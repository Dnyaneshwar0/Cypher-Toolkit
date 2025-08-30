import torch
from torchvision import models, transforms
import torch.nn as nn
import numpy as np
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class DeepfakeDetector:
    def __init__(self, device=DEVICE):
        self.device = device
        self.model = models.xception(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features,2)
        self.model.to(self.device).eval()
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((299,299)),
            transforms.ToTensor(),
            transforms.Normalize([0.5]*3,[0.5]*3)
        ])

    def preprocess(self, video_path):
        from ..preprocess.video import extract_frames, detect_faces
        frames = extract_frames(video_path)
        faces = detect_faces(frames)
        return frames, faces

    def predict(self, faces):
        if len(faces)==0: return {"deepfake_score":0.5}
        tensor = torch.stack([self.transform(f) for f in faces]).to(self.device)
        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=1)
        return {"deepfake_score": float(probs[:,1].mean())}
