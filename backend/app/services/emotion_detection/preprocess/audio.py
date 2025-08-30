import librosa
import numpy as np

def extract_audio(video_path: str, sr: int = 16000) -> np.ndarray:
    import subprocess, tempfile
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        subprocess.run(["ffmpeg", "-y", "-i", video_path, tmp.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        audio, _ = librosa.load(tmp.name, sr=sr)
    return audio

def audio_to_melspec(audio: np.ndarray, sr: int = 16000, n_mels: int = 64) -> np.ndarray:
    mel = librosa.feature.melspectrogram(audio, sr=sr, n_mels=n_mels)
    log_mel = librosa.power_to_db(mel)
    return log_mel
