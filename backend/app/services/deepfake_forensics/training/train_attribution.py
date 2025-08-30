import os
from pathlib import Path
import torch, torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from typing import List

DATA_ROOT = Path("data/processed/ffpp")
CKPT_DIR = Path("data/checkpoints"); CKPT_DIR.mkdir(parents=True, exist_ok=True)
CLASSES: List[str] = ["DeepFakes","FaceSwap","Face2Face","NeuralTextures"]
BATCH_SIZE=32; EPOCHS=5; LR=1e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def make_loaders():
    tfm_train = transforms.Compose([
        transforms.Resize(256),
        transforms.RandomResizedCrop(224, scale=(0.7,1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.485,0.456,0.406), std=(0.229,0.224,0.225)),
    ])
    tfm_eval = transforms.Compose([
        transforms.Resize(256), transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.485,0.456,0.406), std=(0.229,0.224,0.225)),
    ])
    ds_train = datasets.ImageFolder(DATA_ROOT/"train", transform=tfm_train)
    ds_val   = datasets.ImageFolder(DATA_ROOT/"val",   transform=tfm_eval)
    dl_train = DataLoader(ds_train, batch_size=BATCH_SIZE, shuffle=True, num_workers=4, pin_memory=True)
    dl_val   = DataLoader(ds_val,   batch_size=BATCH_SIZE, shuffle=False, num_workers=4, pin_memory=True)
    return dl_train, dl_val

def make_model(num_classes: int):
    m = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    m.fc = nn.Linear(m.fc.in_features, num_classes)
    return m

def evaluate(model, dl):
    model.eval(); correct=0; total=0
    with torch.no_grad():
        for x,y in dl:
            x=x.to(DEVICE); y=y.to(DEVICE)
            logits = model(x); pred = logits.argmax(1)
            correct += (pred==y).sum().item(); total += y.numel()
    return correct/total if total>0 else 0.0

def train():
    dl_train, dl_val = make_loaders()
    model = make_model(len(CLASSES)).to(DEVICE)
    opt = torch.optim.AdamW(model.parameters(), lr=LR)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=EPOCHS)
    ce = nn.CrossEntropyLoss()
    best = 0.0

    for epoch in range(1, EPOCHS+1):
        model.train()
        for x,y in dl_train:
            x=x.to(DEVICE); y=y.to(DEVICE)
            opt.zero_grad()
            loss = ce(model(x), y)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
        acc = evaluate(model, dl_val); sched.step()
        print(f"epoch {epoch}/{EPOCHS}  val_acc={acc:.4f}")
        if acc > best:
            best = acc
            torch.save({
                "state_dict": model.state_dict(),
                "classes": CLASSES
            }, CKPT_DIR/"resnet50_ffpp_attribution.pt")
    print(f"best_val_acc={best:.4f}")

if __name__ == "__main__":
    train()
