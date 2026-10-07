"""
Git Hook Management for git-grass.
Injects and manages pre-commit hooks to enforce outdoor time.
"""

import sys
import os
import stat
from pathlib import Path

HOOK_SCRIPT_TEMPLATE = """#!/usr/bin/env bash
# git-grass pre-commit hook
# Enforces real-world outdoor time before commits are accepted.

if command -v git-grass &> /dev/null; then
    git-grass hook-check
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        exit 1
    fi
elif [ -f "{python_exec}" ]; then
    "{python_exec}" -m git_grass.cli hook-check
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        exit 1
    fi
fi
"""

def find_git_root(start_dir: str = None) -> Path:
    current = Path(start_dir or os.getcwd()).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise FileNotFoundError("Not inside a git repository (.git directory not found).")

def install_hook(repo_dir: str = None) -> Path:
    git_root = find_git_root(repo_dir)
    hooks_dir = git_root / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_file = hooks_dir / "pre-commit"

    python_exec = sys.executable
    script_content = HOOK_SCRIPT_TEMPLATE.format(python_exec=python_exec)

    with open(hook_file, "w", encoding="utf-8") as f:
        f.write(script_content)

    # Make executable
    st = os.stat(hook_file)
    os.chmod(hook_file, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return hook_file

def remove_hook(repo_dir: str = None) -> bool:
    try:
        git_root = find_git_root(repo_dir)
        hook_file = git_root / ".git" / "hooks" / "pre-commit"
        if hook_file.exists():
            hook_file.unlink()
            return True
        return False
    except Exception:
        return False

def is_hook_installed(repo_dir: str = None) -> bool:
    try:
        git_root = find_git_root(repo_dir)
        hook_file = git_root / ".git" / "hooks" / "pre-commit"
        if not hook_file.exists():
            return False
        with open(hook_file, "r", encoding="utf-8") as f:
            return "git-grass" in f.read()
    except Exception:
        return False
