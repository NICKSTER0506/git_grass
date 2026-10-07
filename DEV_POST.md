*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built

**`git-grass`** is a developer wellness CLI tool and Git pre-commit daemon powered by local open-weight computer vision. It actively prevents developer burnout by tracking continuous screen time and **locking Git commits** until you physically step away from your desk, go outside, and provide camera/photo proof that you touched real grass, garden turf, or autumn foliage.

### Key Features:
- **Git Commit Nature Lock**: Automatically halts `git commit` / `git push` if you code continuously for over 2 hours without an outdoor break.
- **On-Device Proof of Nature**: Evaluates outdoor photos using local open-weight multi-spectral botanical vision models.
- **Anti-Cheating Filter**: Employs spatial and spectral entropy algorithms to penalize and reject IDE screenshots, monitors, and wallpaper cheats (-95% penalty).
- **Streak & Wellness Tracker**: Tracks daily outdoor streaks, total nature contacts, and session durations with terminal ASCII art.

---

## Demo

Here is `git-grass` in action when trying to commit code while locked:

```bash
$ git commit -m "fix: important bug"

 ╔════════════════════════════════════════════════════════════╗
 ║                     🔒 GIT COMMITS LOCKED                   ║
 ║                                                            ║
 ║   You have been coding for too long without outdoors time! ║
 ║   Git commits are paused until you touch real grass.       ║
 ║                                                            ║
 ║   Run: git-grass verify <photo_of_grass.jpg>            ║
 ╚════════════════════════════════════════════════════════════╝

❌ Git Commit Blocked by git-grass: Continuous coding session exceeded 120 minutes without touching grass.
👉 Step outside, snap a photo of nature, and run:
   git-grass verify <photo_of_grass.jpg>
```

When you step outside, snap a photo of a lawn or autumn leaves, and verify:

```bash
$ git-grass verify my_lawn.jpg

🔍 Inspecting Image with Local Open-Weight AI Detector...
Image: my_lawn.jpg

   🧪 Multi-Spectral Botanical Analysis    
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Biometric / Environmental Index ┃ Score ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Green Turf & Lawn Index         │ 86.7% │
│ Foliage & Tree Canopy Index     │  0.0% │
│ Natural Daylight / Sky Index    │ 22.3% │
│ Organic Texture Entropy         │ 34.3% │
│ Composite Nature Score          │ 80.8% │
└─────────────────────────────────┴───────┘

 ╔════════════════════════════════════════════════════════════╗
 ║                🌱 PROOF OF NATURE VERIFIED! 🌱              ║
 ║                                                            ║
 ║   Open-weight AI confirmed genuine outdoor nature contact! ║
 ║   Git lock released. Happy coding (with fresh air in mind) ║
 ╚════════════════════════════════════════════════════════════╝

Classification: Fresh Lawn & Green Foliage
🔥 Streak updated to 1 days! Now go ship great code.
```

---

## Code

The complete source code is open-source and available on GitHub:

{% github https://github.com/NICKSTER0506/git_grass %}

### Repository Architecture:
- `git_grass/detector.py`: Multi-spectral botanical and texture vision classifier (Excess Green Index, VARI, organic entropy, and anti-screen filters).
- `git_grass/hook.py`: Git pre-commit hook injector and validator.
- `git_grass/cli.py`: Rich terminal interface and commands (`status`, `verify`, `lock`, `hook`, `demo`).
- `git_grass/state.py`: Local streak and lockout state manager (`~/.git-grass/state.json`).

---

## How I Built It

`git-grass` is built with Python 3, Click, Rich, Pillow, NumPy, and ONNX Runtime.

The core AI engine uses a hybrid local open-weight multi-spectral vision pipeline:
1. **Botanical Remote Sensing Indices**: Computes the **Excess Green Index ($2\text{G} - \text{R} - \text{B}$)** and **Visible Atmospherically Resistant Index (VARI)** to detect live biological chlorophyll.
2. **Organic Gradient Entropy**: Applies edge frequency filters to differentiate natural, fractal organic textures (grass blades, bark, leaf veins) from pixel grids and flat monitor panels.
3. **Anti-Synthetic Heuristics**: Detects monochromatic dark theme palettes and high-frequency code line rectangles to reject IDE screenshots with a high penalty score.
4. **Sub-100ms Local Execution**: The entire pipeline runs 100% on CPU in approximately 80 milliseconds.

---

## Why Does Open Innovation Matter?

Open innovation is the single reason `git-grass` works:

1. **100% Offline with Zero Connectivity**: Closed cloud APIs (like OpenAI or Anthropic) require an internet connection. If you're on a hiking trail, in a park, or in an off-grid cabin with no cellular signal, cloud AI fails completely. `git-grass` runs fully locally on your laptop without sending a single byte over the wire.
2. **Absolute Privacy**: Photos of your backyard, garden, or personal life should never be sent to third-party cloud servers. Local open AI keeps all personal data strictly on your device.
3. **Zero Cost & Infinite Runs**: You don't need API keys, credit cards, or token quotas to verify your wellness breaks.
4. **Transparent & Hackable**: Because it's open-source, developers can inspect the weights, calibrate thresholds for their local regional flora (e.g. desert succulent vs. autumn deciduous trees), and contribute custom hooks.

---

## Prize Categories
- **Hacktoberfest Open-Source AI Challenge: Touch Grass**

---

<!-- Thanks for participating! -->
