import os, cv2, random, shutil
from pathlib import Path
from typing import List, Tuple
import torch
from facenet_pytorch import MTCNN

# Expected raw layout (you place FF++ here after download):
# data/raw/ffpp/{DeepFakes,FaceSwap,Face2Face,NeuralTextures}/*/*.mp4
RAW_ROOT = Path("data/raw/ffpp")
OUT_ROOT = Path("data/processed/ffpp")
SPLITS = ("train", "val", "test")
CLASSES = ["DeepFakes", "FaceSwap", "Face2Face", "NeuralTextures"]

def _videos(cls: str) -> List[Path]:
    return sorted(list((RAW_ROOT/cls).rglob("*.mp4")))

def _split_indices(n: int, seed: int = 42) -> Tuple[List[int], List[int], List[int]]:
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    t = int(0.8*n); v = int(0.1*n)
    return idx[:t], idx[t:t+v], idx[t+v:]

def extract_faces_to_imgfolder(
    fps: float = 2.0,   # sample 2 frames/sec per video
    max_faces_per_video: int = 40,
    min_face_size: int = 80,
    device: str = "cuda" if torch.cuda.is_available() else "cpu",
):
    mtcnn = MTCNN(keep_all=True, device=device, post_process=True)
    for split in SPLITS:
        for cls in CLASSES:
            (OUT_ROOT/split/cls).mkdir(parents=True, exist_ok=True)

    for cls in CLASSES:
        vids = _videos(cls)
        tr, va, te = _split_indices(len(vids))
        assign = {"train": tr, "val": va, "test": te}

        for split, indices in assign.items():
            for i in indices:
                vpath = vids[i]
                cap = cv2.VideoCapture(str(vpath))
                if not cap.isOpened():
                    print(f"[skip] cannot open {vpath}")
                    continue

                total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                rate = cap.get(cv2.CAP_PROP_FPS) or 25.0
                stride = max(int(rate // fps), 1)

                saved = 0; frame_idx = 0
                while saved < max_faces_per_video and cap.isOpened():
                    ok = cap.grab()
                    if not ok: break
                    if frame_idx % stride == 0:
                        ok, frame = cap.retrieve()
                        if not ok: break
                        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        boxes, _ = mtcnn.detect(rgb)
                        if boxes is None: 
                            frame_idx += 1
                            continue
                        for bi, b in enumerate(boxes):
                            x1,y1,x2,y2 = [int(v) for v in b]
                            w,h = x2-x1, y2-y1
                            if min(w,h) < min_face_size: 
                                continue
                            crop = rgb[max(0,y1):y2, max(0,x1):x2]
                            if crop.size == 0: 
                                continue
                            out_dir = OUT_ROOT/split/cls
                            stem = f"{vpath.stem}_{frame_idx:06d}_{bi}.jpg"
                            cv2.imwrite(str(out_dir/stem), cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))
                            saved += 1
                            if saved >= max_faces_per_video: break
                    frame_idx += 1
                cap.release()

if __name__ == "__main__":
    extract_faces_to_imgfolder()
