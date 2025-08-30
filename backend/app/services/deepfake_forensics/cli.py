import sys
from backend.app.services.deepfake_forensics.pipeline import DeepfakeForensicsPipeline

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <video_path>")
        return

    video_path = sys.argv[1]
    pipeline = DeepfakeForensicsPipeline()
    try:
        result = pipeline.run(video_path)
        print("\nDeepfake Reverse Engineering Toolkit")
        print("Objective: Identify the AI model, dataset, and generation method used to create a given deepfake.\n")
        print(f"Predicted AI Model       : {result.get('model_likely')}")
        print(f"Predicted Training Dataset: {result.get('dataset_likely')}")
        print(f"Generation Method       : {result.get('method')}")
        print(f"Artifact Scores         : {result.get('artifact_scores')}")
    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
