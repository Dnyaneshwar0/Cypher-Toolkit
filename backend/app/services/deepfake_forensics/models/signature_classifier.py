from typing import Dict
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

class SignatureClassifier:
    def __init__(self, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.model.fc = nn.Linear(self.model.fc.in_features, 3)  # 3 classes: StyleGAN2, FaceSwap, DeepFaceLab
        self.model.to(self.device)
        self.model.eval()
        self.class_mapping = {0: "StyleGAN2", 1: "FaceSwap", 2: "DeepFaceLab"}

    def predict(self, frame_features: torch.Tensor) -> Dict[str, float]:
        """
        Expects frame_features: Tensor of shape [1, 3, H, W] normalized
        """
        frame_features = frame_features.to(self.device)
        with torch.no_grad():
            logits = self.model(frame_features)
            probs = F.softmax(logits, dim=1)
            conf, pred_idx = torch.max(probs, dim=1)
            model_name = self.class_mapping[int(pred_idx)]
        return {"model_likely": model_name, "confidence": float(conf), "method": "full-synthesis"}
