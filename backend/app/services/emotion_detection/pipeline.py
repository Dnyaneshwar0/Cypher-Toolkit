from .modules.deepfake_detector import DeepfakeDetector
from .modules.facial_emotion import FacialEmotion
from .modules.audio_emotion import AudioEmotion
from .modules.transcript_emotion import TranscriptEmotion
from .fusion import FusionModule

class EmotionalManipulationPipeline:
    def __init__(self):
        self.video_model=DeepfakeDetector()
        self.facial_model=FacialEmotion()
        self.audio_model=AudioEmotion()
        self.text_model=TranscriptEmotion()
        self.fusion=FusionModule()
    
    def run(self, video_path:str):
        frames, faces=self.video_model.preprocess(video_path)
        audio_feats=self.audio_model.preprocess(video_path)
        transcript_text=self.text_model.preprocess(video_path)
        df_score=self.video_model.predict(faces)
        facial=self.facial_model.predict(faces)
        audio=self.audio_model.predict(audio_feats)
        text=self.text_model.predict(transcript_text)
        return self.fusion.combine(df_score, facial, audio, text)
