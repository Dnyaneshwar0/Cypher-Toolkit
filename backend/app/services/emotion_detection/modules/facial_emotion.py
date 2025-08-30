import torch
import torch.nn as nn
from torchvision import models, transforms
import numpy as np
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class FacialEmotion:
    def __init__(self, device=DEVICE):
        self.device=device
        self.model=models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features,7)
        self.model.to(self.device).eval()
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
        ])
    
    def predict(self, faces):
        if len(faces)==0: return {"emotion":"neutral","confidence":0.5}
        tensor = torch.stack([self.transform(f) for f in faces]).to(self.device)
        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=1)
        avg = probs.mean(0)
        idx = avg.argmax().item()
        return {"emotion":["angry","disgust","fear","happy","sad","surprise","neutral"][idx],"confidence":float(avg[idx])}
