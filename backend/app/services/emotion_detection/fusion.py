from collections import Counter

class FusionModule:
    def combine(self, deepfake_score, facial_emotions, audio_emotions, text_emotions):
        df_weight=0.4; facial_weight=0.2; audio_weight=0.2; text_weight=0.2
        score = (deepfake_score["deepfake_score"]*df_weight +
                 facial_emotions["confidence"]*facial_weight +
                 audio_emotions["confidence"]*audio_weight +
                 text_emotions["confidence"]*text_weight)
        emotions=[facial_emotions["emotion"], audio_emotions["audio_emotion"], text_emotions["text_emotion"]]
        dominant = Counter(emotions).most_common(1)[0][0]
        return {"deepfake_confidence":float(score), "dominant_emotion":dominant}
