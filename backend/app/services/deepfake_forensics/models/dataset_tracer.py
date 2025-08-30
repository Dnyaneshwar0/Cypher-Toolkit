from typing import Dict
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
import numpy as np
import faiss
import os

class DatasetTracer:
    def __init__(self, dataset_embeddings_dir: str = "data/forensics_samples"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.mtcnn = MTCNN(keep_all=True, device=self.device)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)

        self.dataset_names = []
        self.embeddings = []

        if os.path.exists(dataset_embeddings_dir):
            for file in os.listdir(dataset_embeddings_dir):
                if file.endswith(".npy"):
                    self.dataset_names.append(file.replace(".npy", ""))
                    self.embeddings.append(np.load(os.path.join(dataset_embeddings_dir, file)))

        if self.embeddings:
            self.embeddings = np.vstack(self.embeddings).astype('float32')
            self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
            self.index.add(self.embeddings)
        else:
            self.index = None

    def trace(self, features: Dict[str, float]) -> Dict[str, float]:
        if self.index is None or len(self.dataset_names) == 0:
            return {"dataset_likely": "Unknown", "confidence": 0.0}
        return {"dataset_likely": self.dataset_names[0], "confidence": 0.7}
