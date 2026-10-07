"""
Unit & Integration Tests for git-grass.
"""

import os
import unittest
from pathlib import Path
from git_grass.detector import NatureDetector
from git_grass.state import load_state, save_state, lock_terminal, unlock_terminal, is_locked

class TestGitGrass(unittest.TestCase):
    def setUp(self):
        self.detector = NatureDetector()
        self.samples_dir = Path(__file__).parent.parent / "test_samples"

    def test_outdoor_lawn_verification(self):
        lawn_path = self.samples_dir / "real_lawn.jpg"
        if lawn_path.exists():
            res = self.detector.analyze_image(str(lawn_path))
            self.assertTrue(res["verified"])
            self.assertGreaterEqual(res["nature_score"], 50.0)

    def test_indoor_screen_rejection(self):
        screen_path = self.samples_dir / "indoor_screen.jpg"
        if screen_path.exists():
            res = self.detector.analyze_image(str(screen_path))
            self.assertFalse(res["verified"])
            self.assertLess(res["nature_score"], 50.0)

    def test_lock_and_unlock_lifecycle(self):
        lock_terminal("Testing detox lock")
        locked, reason = is_locked()
        self.assertTrue(locked)
        self.assertIn("Testing detox lock", reason)

        # Unlock with verified nature data
        state = unlock_terminal({"nature_score": 85.0, "category": "Fresh Lawn"})
        locked_after, _ = is_locked()
        self.assertFalse(locked_after)
        self.assertGreaterEqual(state["current_streak_days"], 1)

if __name__ == "__main__":
    unittest.main()
