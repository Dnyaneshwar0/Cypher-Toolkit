from transformers import pipeline
from ..preprocess.transcript import transcribe

class TranscriptEmotion:
    def __init__(self):
        self.model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
    
    def preprocess(self, video_path):
        return transcribe(video_path)
    
    def predict(self, text):
        if not text: return {"text_emotion":"neutral","confidence":0.5}
        result = self.model(text[:512])[0]
        return {"text_emotion":result["label"],"confidence":float(result["score"])}
