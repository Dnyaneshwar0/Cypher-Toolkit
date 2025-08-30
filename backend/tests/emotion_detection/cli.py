import sys
from backend.app.services.emotion_detection.pipeline import EmotionalManipulationPipeline

def main():
    if len(sys.argv)<2:
        print("Usage: python cli.py <video_path>")
        return
    video_path=sys.argv[1]
    pipeline=EmotionalManipulationPipeline()
    try:
        result=pipeline.run(video_path)
        print("\nEmotional Deepfake Detection")
        print(f"Predicted Deepfake Confidence: {result['deepfake_confidence']:.4f}")
        print(f"Predominant Emotional Manipulation: {result['dominant_emotion']}")
    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__=="__main__":
    main()
