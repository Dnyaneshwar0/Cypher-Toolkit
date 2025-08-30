import cv2
import torch
from torchvision import transforms

def extract_artifacts(video_path: str) -> torch.Tensor:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    frames = []
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((224, 224)),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    success, frame = cap.read()
    while success:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tensor = transform(frame_rgb)
        frames.append(tensor)
        success, frame = cap.read()
    cap.release()

    if not frames:
        raise ValueError("No frames extracted from video")
    batch = torch.stack(frames)  # [batch, 3, 224, 224]
    return batch
