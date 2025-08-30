# backend/tests/forensics/test_forensics_cli.py

import unittest
import os
from io import StringIO
import sys
from backend.app.services.deepfake_forensics.cli import main as forensic_cli

class TestDeepfakeCLI(unittest.TestCase):
    def setUp(self):
        # Path to a sample video for testing
        self.sample_video = os.path.join(
            os.path.dirname(__file__),
            "../../../data/forensics_samples/videos/sample.mp4"
        )
        # Backup stdout
        self._stdout_backup = sys.stdout

    def tearDown(self):
        sys.stdout = self._stdout_backup

    def test_forensics_cli(self):
        """Run CLI and capture output for a sample video"""
        sys.stdout = StringIO()  # Redirect stdout to capture prints

        # Simulate CLI argument
        sys.argv = ['cli.py', self.sample_video]

        # Run CLI
        forensic_cli()

        # Read captured output
        output = sys.stdout.getvalue()
        
        # Check key phrases exist in output
        self.assertIn("Deepfake Reverse Engineering Toolkit", output)
        self.assertIn("Predicted AI Model", output)
        self.assertIn("Predicted Training Dataset", output)
        self.assertIn("Generation Method", output)
        self.assertIn("Artifact Scores", output)

        # Optionally print output during testing
        print(output)

if __name__ == "__main__":
    unittest.main()
