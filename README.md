# Multi-Format Deepfake and Emotion Analysis Toolkit

## Overview

This project is a comprehensive platform for deepfake analysis, emotional manipulation detection, and data security techniques. It combines advanced AI models, deep learning pipelines, and encryption/steganography tools to provide a research-grade system.  

The project has three core objectives:

1. **Deepfake Reverse Engineering Toolkit**  
   - **Objective:** Identify the AI model, dataset, and generation method used to create a deepfake.  
   - **Approach:**  
     - Extract digital fingerprints from videos (artifacts, compression patterns).  
     - Train classifiers to recognize GAN model “signatures” (StyleGAN, FaceSwap, DeepFaceLab).  
     - Trace potential training dataset features.

2. **Emotional Manipulation Detection in Deepfakes**  
   - **Objective:** Detect not just if a video is fake, but whether it is designed to evoke strong emotions like fear, anger, or sympathy.  
   - **Approach:**  
     - Deepfake detection using CNNs and XceptionNet.  
     - Sentiment analysis on transcripts using BERT / RoBERTa.  
     - Facial emotion recognition using OpenFace / AffectNet.  
     - Correlate detected deepfakes with emotional intensity scores.

3. **Multi-Format Cipher Generator and Cracker System**  
   - **Objective:** Explore and demonstrate data encoding, encryption, and obfuscation techniques.  
   - **Approach:**  
     - Generate CAPTCHAs for verification and obfuscation.  
     - Embed and extract data within images using steganography.  
     - Encode and decode information using SHA-256, Base64, AES, and ASCII.  
     - Attempt cracking to analyze security and reversibility.  

---

## Project Structure & Technology Stack

| Module / Directory                       | Description / Purpose                                                                 | Key Technologies / Models Used                     |
|-----------------------------------------|--------------------------------------------------------------------------------------|---------------------------------------------------|
| `backend/app/routes`                     | API endpoints for all services                                                       | Flask                                             |
| `backend/app/services/deepfake_forensics` | Deepfake detection and reverse engineering                                          | XceptionNet, CNN, ResNet, PyTorch, OpenCV         |
| `backend/app/services/emotion_detection` | Emotional manipulation detection pipeline                                           | BERT, RoBERTa, OpenFace, AffectNet, PyTorch      |
| `backend/app/services/crypto_utils`      | Data encoding, encryption, and cracking utilities                                   | AES, SHA-256, Base64, ASCII                       |
| `backend/app/services/steganography`     | Hide and extract data from images                                                   | Pillow, OpenCV                                   |
| `backend/app/services/captcha_gen`       | CAPTCHA generation and solving                                                      | Pillow, OpenCV                                   |
| `backend/app/utils`                      | Helper functions for file handling, hashing, and format detection                   | NumPy, Python standard libraries                  |
| `backend/tests`                          | Unit and CLI tests for all modules                                                  | Pytest                                           |
| `frontend`                               | Web interface for visualization and interaction                                     | React, TailwindCSS, JavaScript                   |
| `data/forensics_samples/videos`         | Sample deepfake videos for testing                                                  | FF++ dataset                                     |
| `data/images`                            | Images for CAPTCHA, encryption, and steganography testing                            | Pillow, OpenCV                                   |
| `data/texts`                             | Text files for transcripts, cipher samples, and CAPTCHA solutions                   | Standard text files                               |
| `requirements.txt`                        | Python dependencies                                                                 | Flask, PyTorch, facenet-pytorch, faiss, NumPy    |

---

## Requirements

```txt
# Web framework
Flask==3.1.1
click==8.2.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
Werkzeug==3.1.3
blinker==1.9.0
colorama==0.4.6

# Data processing & images
numpy==2.3.1
pillow==11.3.0
opencv-python==4.8.0

# Deep learning
torch==2.1.0
torchvision==0.16.1
facenet-pytorch==2.8.2
faiss-cpu==1.7.4
```

