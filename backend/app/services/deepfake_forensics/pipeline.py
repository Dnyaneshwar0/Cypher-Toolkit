from .extractors import artifact, frequency, temporal
from .models.signature_classifier import SignatureClassifier
from .models.dataset_tracer import DatasetTracer

class DeepfakeForensicsPipeline:
    def __init__(self):
        self.signature_model = SignatureClassifier()
        self.dataset_tracer = DatasetTracer()

    def run(self, video_path: str):
        artifacts = artifact.extract_artifacts(video_path)
        freq = frequency.extract_frequency(video_path)
        temp = temporal.extract_temporal(video_path)

        features = {**artifacts, **freq, **temp}
        model_info = self.signature_model.predict(features)
        dataset_info = self.dataset_tracer.trace(features)

        return {**model_info, **dataset_info, "artifact_scores": features}
