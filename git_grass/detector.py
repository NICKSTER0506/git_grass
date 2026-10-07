"""
Open-Source AI & Computer Vision Detector for Nature & Real Grass Verification.
Runs 100% locally on CPU without sending any data to external servers.
"""

import os
from pathlib import Path
from typing import Dict, Any, Tuple
import numpy as np
from PIL import Image, ImageStat, ImageFilter

class NatureDetector:
    """
    Evaluates imagery for genuine outdoor nature, botanical foliage, and lawn turf
    while penalizing artificial screens, code editors, and indoor desk environments.
    """

    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self._onnx_session = None
        if model_path and os.path.exists(model_path):
            try:
                import onnxruntime as ort
                self._onnx_session = ort.InferenceSession(model_path)
            except Exception:
                self._onnx_session = None

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Performs full local multi-spectral and botanical texture analysis on the image.
        Returns a rich breakdown of scores and a final verification boolean.
        """
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        img = Image.open(path).convert("RGB")
        img_resized = img.resize((300, 300))
        img_np = np.array(img_resized, dtype=np.float32)

        r = img_np[:, :, 0]
        g = img_np[:, :, 1]
        b = img_np[:, :, 2]

        # 1. Botanical Excess Green Index (ExG = 2G - R - B)
        # ExG is a standard agronomical remote-sensing index used to detect live turf & foliage
        denom = (r + g + b + 1e-5)
        rn = r / denom
        gn = g / denom
        bn = b / denom
        exg = 2.0 * gn - rn - bn
        green_coverage = float(np.mean(exg > 0.05))
        strong_green_ratio = float(np.mean(exg > 0.15))

        # 2. Visible Atmospherically Resistant Index (VARI = (G - R) / (G + R - B + eps))
        vari = (g - r) / (g + r - b + 1e-5)
        vari_score = float(np.clip(np.mean(vari), -1.0, 1.0))

        # 3. Autumn Foliage / Earthy Botanical Color Index
        # Detects golden/amber/red leaves, bark, soil, and fall foliage (High R, moderate G, low B)
        autumn_mask = (r > 100) & (g > 60) & (b < 100) & (r > g) & (g > b)
        autumn_foliage_ratio = float(np.mean(autumn_mask))

        # 4. Sky / Sunlight Natural Spectrum Index
        # Daylight sky and natural ambient sunlight (High B and balanced R/G, high brightness)
        sky_mask = (b > 120) & (b >= r) & (b >= g * 0.85) & (img_np.mean(axis=2) > 130)
        sky_ratio = float(np.mean(sky_mask))

        # 5. Natural Organic Texture vs Synthetic Grid / Screen Pixel Regularity
        # Natural grass and leaves have high organic high-frequency gradients without rectilinear pixel edges
        gray_img = img_resized.convert("L")
        edges = gray_img.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        texture_entropy = float(edge_stat.stddev[0]) / 128.0

        # 6. Screen / Code Editor / Indoor Detection Penalty
        # Monochromatic dark screens (IDE themes) or pure white displays with sharp horizontal lines
        dark_ratio = float(np.mean(img_np < 40))
        gray_diff = np.mean(np.abs(r - g) + np.abs(g - b) + np.abs(r - b)) / 3.0  # Monochromaticity
        screen_penalty = 0.0

        if gray_diff < 15.0 and green_coverage < 0.1:
            # Monochromatic grey/black/white indicates text editor, terminal, or indoor walls
            screen_penalty += 0.45

        if dark_ratio > 0.6 and green_coverage < 0.1:
            # Dark mode IDE / terminal screen
            screen_penalty += 0.5

        # 7. Composite Nature Score Computation
        nature_score_raw = (
            green_coverage * 45.0 +
            strong_green_ratio * 20.0 +
            autumn_foliage_ratio * 45.0 +
            sky_ratio * 20.0 +
            texture_entropy * 15.0 +
            max(0.0, vari_score) * 20.0
        )

        nature_score_penalized = max(0.0, nature_score_raw - (screen_penalty * 100.0))
        final_nature_score = min(100.0, round(nature_score_penalized, 1))

        # Threshold for verification: 50.0%
        is_verified = final_nature_score >= 50.0

        # Classification label
        if is_verified:
            if green_coverage > 0.3:
                label = "Fresh Lawn & Green Foliage"
            elif autumn_foliage_ratio > 0.2:
                label = "Autumn Leaves & Fall Foliage"
            elif sky_ratio > 0.25:
                label = "Outdoor Sky & Natural Sunlight"
            else:
                label = "Botanical Nature Environment"
        else:
            if screen_penalty > 0.3:
                label = "Indoor Screen / IDE Display (Not Nature!)"
            else:
                label = "Insufficient Nature / Indoor Environment"

        return {
            "verified": is_verified,
            "nature_score": final_nature_score,
            "category": label,
            "breakdown": {
                "green_turf_index": round(green_coverage * 100, 1),
                "foliage_canopy_index": round(autumn_foliage_ratio * 100, 1),
                "daylight_sky_index": round(sky_ratio * 100, 1),
                "organic_texture_index": round(texture_entropy * 100, 1),
                "indoor_screen_penalty": round(screen_penalty * 100, 1)
            }
        }
