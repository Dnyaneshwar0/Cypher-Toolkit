from pydantic import BaseModel
from typing import Dict

class ForensicResult(BaseModel):
    model_likely: str
    model_confidence: float
    method: str
    dataset_likely: str
    dataset_confidence: float
    artifact_scores: Dict[str, float]
