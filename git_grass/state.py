"""
State manager for git-grass.
Tracks session timers, lock status, streak metrics, and nature verification history.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime, date

STATE_DIR = Path.home() / ".git-grass"
STATE_FILE = STATE_DIR / "state.json"

DEFAULT_STATE = {
    "locked": False,
    "lock_reason": "",
    "session_start_time": time.time(),
    "max_session_minutes": 120,  # Lock after 2 hours by default
    "current_streak_days": 0,
    "last_grass_timestamp": 0,
    "last_verified_date": "",
    "total_grass_verifications": 0,
    "recent_scores": []
}

def get_state_dir() -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR

def load_state() -> dict:
    get_state_dir()
    if not STATE_FILE.exists():
        save_state(DEFAULT_STATE)
        return dict(DEFAULT_STATE)
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Merge with defaults in case of new keys
            state = dict(DEFAULT_STATE)
            state.update(data)
            return state
    except Exception:
        return dict(DEFAULT_STATE)

def save_state(state: dict) -> None:
    get_state_dir()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def is_locked() -> tuple[bool, str]:
    state = load_state()
    # Check manual lock
    if state.get("locked"):
        return True, state.get("lock_reason", "Session locked manually or by policy.")
    
    # Check session duration lock
    session_start = state.get("session_start_time", time.time())
    max_minutes = state.get("max_session_minutes", 120)
    elapsed_minutes = (time.time() - session_start) / 60.0

    if elapsed_minutes >= max_minutes:
        lock_terminal(f"Exceeded continuous coding limit ({int(elapsed_minutes)}m >= {max_minutes}m).")
        return True, f"Continuous coding session exceeded {max_minutes} minutes without touching grass."

    return False, ""

def lock_terminal(reason: str = "Locked: Time to touch grass!") -> None:
    state = load_state()
    state["locked"] = True
    state["lock_reason"] = reason
    save_state(state)

def unlock_terminal(score_data: dict) -> dict:
    state = load_state()
    today_str = date.today().isoformat()

    # Update streak
    last_date = state.get("last_verified_date", "")
    if last_date:
        try:
            last_d = date.fromisoformat(last_date)
            diff = (date.today() - last_d).days
            if diff == 1:
                state["current_streak_days"] += 1
            elif diff == 0:
                pass  # already touched grass today
            else:
                state["current_streak_days"] = 1
        except Exception:
            state["current_streak_days"] = 1
    else:
        state["current_streak_days"] = 1

    state["locked"] = False
    state["lock_reason"] = ""
    state["session_start_time"] = time.time()
    state["last_grass_timestamp"] = time.time()
    state["last_verified_date"] = today_str
    state["total_grass_verifications"] = state.get("total_grass_verifications", 0) + 1

    recent = state.get("recent_scores", [])
    recent.append({
        "timestamp": datetime.now().isoformat(),
        "score": score_data.get("nature_score", 0),
        "details": score_data.get("breakdown", {})
    })
    state["recent_scores"] = recent[-10:]  # Keep last 10
    save_state(state)
    return state
