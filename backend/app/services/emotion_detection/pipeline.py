from .preprocess.video import extract_frames, extract_audio
from .modules.facial_emotion import detect_facial_emotions
from .modules.transcript_emotion import analyze_transcript
from .modules.audio_emotion import analyze_audio_emotion
from .fusion import fuse_emotions

class EmotionDetectionPipeline:
    def run(self, video_path: str, transcript_text: str = "") -> dict:
        frames = extract_frames(video_path)
        audio_path = extract_audio(video_path)

        facial = detect_facial_emotions(frames)
        transcript = analyze_transcript(transcript_text)
        audio = analyze_audio_emotion({}) if audio_path else None

        return fuse_emotions(facial, transcript, audio)
