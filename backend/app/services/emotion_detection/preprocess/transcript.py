from transformers import pipeline
import re
import whisper

def transcribe(video_path: str) -> str:
    model = whisper.load_model("small")
    result = model.transcribe(video_path)
    text = result.get("text", "")
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.lower()
