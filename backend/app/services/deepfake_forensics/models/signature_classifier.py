from typing import Dict
import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F

class SignatureClassifier:
    def __init__(self, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        self.model = models.xception(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, 3)
        self.model.to(self.device)
        self.model.eval()
        self.class_mapping = {0: "StyleGAN2", 1: "FaceSwap", 2: "DeepFaceLab"}

    def predict(self, features: Dict[str, float]) -> Dict[str, float]:
        x = torch.tensor([list(features.values())], dtype=torch.float32, device=self.device)
        with torch.no_grad():
            logits = self.model(x)
            probs = F.softmax(logits, dim=1)
            conf, pred_idx = torch.max(probs, dim=1)
            model_name = self.class_mapping[int(pred_idx)]
        return {"model_likely": model_name, "confidence": float(conf), "method": "full-synthesis"}
