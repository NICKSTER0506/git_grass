"""
Utility to generate test sample fixtures for git-grass.
"""

from pathlib import Path
from PIL import Image, ImageDraw

SAMPLES_DIR = Path(__file__).parent.parent / "test_samples"
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

def generate_samples():
    # 1. Real Lawn
    lawn = Image.new("RGB", (400, 400), color=(35, 145, 40))
    d = ImageDraw.Draw(lawn)
    for i in range(0, 400, 3):
        blade_h = 220 + (i * 7 % 140)
        d.line([(i, 400), (i + (i % 5) - 2, 400 - blade_h)], fill=(25 + (i % 35), 170 + (i % 45), 30 + (i % 25)), width=2)
    # Sky header
    for y in range(0, 90):
        d.line([(0, y), (400, y)], fill=(110, 175, 235 - int(y * 0.4)), width=1)
    lawn.save(SAMPLES_DIR / "real_lawn.jpg")

    # 2. Autumn Foliage
    autumn = Image.new("RGB", (400, 400), color=(180, 85, 25))
    d_a = ImageDraw.Draw(autumn)
    for x in range(0, 400, 15):
        for y in range(0, 400, 15):
            d_a.ellipse([x, y, x + 25, y + 25], fill=(190 + (x % 50), 90 + (y % 60), 20 + ((x+y) % 30)))
    autumn.save(SAMPLES_DIR / "autumn_foliage.jpg")

    # 3. Indoor Screen / IDE
    screen = Image.new("RGB", (400, 400), color=(25, 28, 35))
    d_s = ImageDraw.Draw(screen)
    # Draw dark IDE code lines
    for y in range(30, 370, 14):
        d_s.rectangle([30, y, 120 + (y * 4 % 180), y + 6], fill=(200, 200, 210))
        d_s.rectangle([45, y + 2, 90 + (y * 2 % 100), y + 4], fill=(90, 160, 230))
    screen.save(SAMPLES_DIR / "indoor_screen.jpg")

    print(f"Generated samples in: {SAMPLES_DIR}")

if __name__ == "__main__":
    generate_samples()
