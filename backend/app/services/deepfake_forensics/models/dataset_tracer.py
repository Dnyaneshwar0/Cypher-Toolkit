class DatasetTracer:
    def trace(self, features: dict) -> dict:
        """Return dummy dataset likelihood"""
        return {"dataset_likely": "FFHQ", "dataset_confidence": 0.42}
