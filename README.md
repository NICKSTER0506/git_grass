# 🌱 `git-grass` — Open-Source AI Terminal Detox & Proof-of-Nature Git Daemon

> **Hacktoberfest Week 2 ("Touch Grass") Submission**  
> *A developer wellness CLI & Git hook powered by local open-weight computer vision that pauses your Git workflow until you physically step outside and touch real grass.*

---

## 🌟 The Problem
Developers spend 10+ hours a day staring at code editors, ignoring sunshine, fresh air, and the physical world. Cloud-based AI assistants often keep developers glued to their monitors even longer.

**`git-grass` flips the script:** It turns AI into an enforcement mechanism to get you **off the screen and into nature**.

```
   ,        .      .       .         .      ,
  / \      / \    / \     / \       / \    / \
 /   \    /   \  /   \   /   \     /   \  /   \
 | | |    | | |  | | |   | | |     | | |  | | |

       _ _                                
  __ _(_) |_ ______ __ _ _ __ __ _ ___ ___
 / _` | | __|______/ _` | '__/ _` / __/ __|
| (_| | | |_      | (_| | | | (_| \__ \__ \
 \__, |_|\__|      \__, |_|  \__,_|___/___/
 |___/             |___/                   

   ~ Touch Grass to Unlock Your Commits ~
```

---

## 🧠 Why Open Innovation & Local AI Matter
1. **100% Offline & Private**: Zero data or photos of your backyard/personal life leave your machine. No cloud uploads.
2. **Zero API Cost & Unlimited Runs**: Runs on open weights (ONNX / Multi-Spectral Remote Sensing & Botanical AI) locally on CPU.
3. **No Network Latency on the Trail**: Whether you're coding off-grid in a cabin or hiking in a park, `git-grass` works with **zero internet**.
4. **Resistant to Cheating**: Open-source heuristics & vision filters detect synthetic IDE wallpapers, monitor bezels, and dark mode themes, preventing devs from "fake-touching" grass on a screen.

---

## 🚀 Quickstart

### 1. Installation
```bash
# Clone and install in editable mode
git clone git@github.com:NICKSTER0506/git_grass.git
cd git_grass
pip install -e .
```

### 2. Check Status
```bash
git-grass status
```

### 3. Protect Your Commits with Git Hook
```bash
# Install git-grass pre-commit hook into your current repository
git-grass hook install
```
Now, if your continuous coding session exceeds the limit (or if you are locked), `git commit` will automatically block:
```
❌ Git Commit Blocked by git-grass: Continuous coding session exceeded 120 minutes without touching grass.
👉 Step outside, snap a photo of nature, and run:
   git-grass verify <photo_of_grass.jpg>
```

### 4. Step Outside & Unlock
Take a photo of real grass, garden soil, or autumn foliage:
```bash
git-grass verify my_lawn.jpg
```
```
 ╔════════════════════════════════════════════════════════════╗
 ║                🌱 PROOF OF NATURE VERIFIED! 🌱              ║
 ║                                                            ║
 ║   Open-weight AI confirmed genuine outdoor nature contact! ║
 ║   Git lock released. Happy coding (with fresh air in mind) ║
 ╚════════════════════════════════════════════════════════════╝
Classification: Fresh Lawn & Green Foliage
🔥 Streak updated to 3 days! Now go ship great code.
```

---

## 🛠 Commands Reference

| Command | Description |
| :--- | :--- |
| `git-grass status` | Show current outdoor streak, session duration, and lock status |
| `git-grass verify <image>` | Run local open AI detector to verify nature and unlock commits |
| `git-grass lock [--reason ...]` | Manually lock the environment and enforce outdoor break |
| `git-grass unlock` | Manually reset session lock |
| `git-grass hook install` | Injects pre-commit hook to current Git repo |
| `git-grass hook remove` | Uninstalls pre-commit hook |
| `git-grass demo` | Runs an interactive test demonstration |

---

## 📄 License
MIT © 2026
