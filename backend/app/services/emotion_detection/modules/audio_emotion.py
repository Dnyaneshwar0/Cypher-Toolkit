import torch, torch.nn as nn
import numpy as np
from ..preprocess.audio import extract_audio, audio_to_melspec
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class AudioEmotion:
    def __init__(self):
        self.device=DEVICE
        self.model = nn.Sequential(
            nn.Conv2d(1,16,3,padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(16,4), nn.Softmax(dim=1)
        )
        self.model.to(self.device).eval()
    
    def preprocess(self, video_path):
        audio = extract_audio(video_path)
        mel = audio_to_melspec(audio)
        return mel[np.newaxis,:,:,np.newaxis]
    
    def predict(self, mel_spec):
        tensor=torch.tensor(mel_spec,dtype=torch.float).permute(0,3,1,2).to(self.device)
        with torch.no_grad():
            probs = self.model(tensor)
        idx=probs.argmax(dim=1).item()
        return {"audio_emotion":["angry","happy","sad","neutral"][idx],"confidence":float(probs[0,idx])}
