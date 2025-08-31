# backend/app/services/deepfake_forensics/models/feature_scaler.py
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class FeatureScaler:
    """
    Extracts and scales features from deepfake videos for model training.
    Can handle temporal, frequency, or artifact-based features.
    """

    def __init__(self, method='standard'):
        """
        Initialize the scaler.
        method: 'standard' for StandardScaler, 'minmax' for MinMaxScaler
        """
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            raise ValueError("method must be 'standard' or 'minmax'")

    def fit(self, X):
        """
        Fit the scaler on training features.
        X: np.ndarray of shape (num_samples, num_features)
        """
        self.scaler.fit(X)
        return self

    def transform(self, X):
        """
        Transform features using the fitted scaler.
        X: np.ndarray of shape (num_samples, num_features)
        """
        return self.scaler.transform(X)

    def fit_transform(self, X):
        """
        Fit and transform in a single step.
        """
        return self.scaler.fit_transform(X)

    @staticmethod
    def extract_features(video_path):
        """
        Stub: Extract numerical features from a video.
        Replace this with actual artifact, compression, or GAN features.
        """
        # Example: fake 10-dimensional feature vector
        return np.random.rand(10)
