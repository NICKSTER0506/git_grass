"""
CLI Interface for git-grass.
"""

import sys
import time
import os
from pathlib import Path
from datetime import datetime, timedelta
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align

from git_grass.ascii_art import BANNER, GRASS_FIELD, LOCKED_BADGE, UNLOCKED_BADGE, INDOOR_REJECTED
from git_grass.state import load_state, save_state, is_locked, lock_terminal, unlock_terminal
from git_grass.detector import NatureDetector
from git_grass.hook import install_hook, remove_hook, is_hook_installed

console = Console()

@click.group()
def main():
    """🌱 git-grass: Terminal Detox & Proof-of-Nature Git Daemon."""
    pass

@main.command()
def banner():
    """Display the git-grass banner."""
    console.print(BANNER)
    console.print(GRASS_FIELD)

@main.command()
def status():
    """Check current outdoor streak, session duration, and lock status."""
    console.print(BANNER)
    state = load_state()
    locked, reason = is_locked()

    table = Table(title="🌱 Developer Vitality & Nature Status", border_style="green")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="bold white")

    # Lock status
    if locked:
        lock_val = "[bold red]🔒 LOCKED (Commits Paused)[/bold red]"
    else:
        lock_val = "[bold green]✅ ACTIVE (Clean Air Verified)[/bold green]"
    table.add_row("System Status", lock_val)

    if locked:
        table.add_row("Lock Reason", f"[italic red]{reason}[/italic red]")

    # Session Time
    elapsed = int((time.time() - state.get("session_start_time", time.time())) / 60)
    max_min = state.get("max_session_minutes", 120)
    time_color = "green" if elapsed < max_min * 0.75 else ("yellow" if elapsed < max_min else "red")
    table.add_row("Continuous Screen Time", f"[{time_color}]{elapsed} min[/{time_color}] (Limit: {max_min} min)")

    # Streak
    streak = state.get("current_streak_days", 0)
    streak_badge = "🌱" * min(streak, 5) if streak > 0 else "🥀 No active streak"
    table.add_row("Daily Outdoor Streak", f"[bold yellow]{streak} days[/bold yellow] {streak_badge}")

    # Total verifications
    table.add_row("Total Nature Proofs", str(state.get("total_grass_verifications", 0)))

    # Last verified
    last_ts = state.get("last_grass_timestamp", 0)
    if last_ts > 0:
        last_str = datetime.fromtimestamp(last_ts).strftime("%Y-%m-%d %H:%M:%S")
    else:
        last_str = "Never"
    table.add_row("Last Grass Touched", last_str)

    console.print(table)

    # Git hook info
    try:
        hook_active = is_hook_installed()
        if hook_active:
            console.print("[dim green]✔ Git pre-commit hook active in current repository.[/dim green]")
        else:
            console.print("[dim yellow]ℹ Git hook not installed in current repo. Run 'git-grass hook install' to protect commits.[/dim yellow]")
    except Exception:
        pass

@main.command()
@click.argument("image_path", type=click.Path(exists=True))
def verify(image_path: str):
    """Verify an outdoor photo with local open-weight AI to unlock commits."""
    console.print(BANNER)
    console.print(f"[bold cyan]🔍 Inspecting Image with Local Open-Weight AI Detector...[/bold cyan]")
    console.print(f"[dim]Image: {image_path}[/dim]\n")

    detector = NatureDetector()

    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[green]Analyzing botanical pigments & organic textures...", total=None)
        time.sleep(0.5)
        res = detector.analyze_image(image_path)
        progress.update(task, completed=True)

    score = res["nature_score"]
    category = res["category"]
    breakdown = res["breakdown"]

    # Table breakdown
    b_table = Table(title="🧪 Multi-Spectral Botanical Analysis", border_style="cyan")
    b_table.add_column("Biometric / Environmental Index", style="white")
    b_table.add_column("Score", justify="right", style="bold green")

    b_table.add_row("Green Turf & Lawn Index", f"{breakdown['green_turf_index']}%")
    b_table.add_row("Foliage & Tree Canopy Index", f"{breakdown['foliage_canopy_index']}%")
    b_table.add_row("Natural Daylight / Sky Index", f"{breakdown['daylight_sky_index']}%")
    b_table.add_row("Organic Texture Entropy", f"{breakdown['organic_texture_index']}%")
    if breakdown["indoor_screen_penalty"] > 0:
        b_table.add_row("Indoor Screen Penalty", f"[bold red]-{breakdown['indoor_screen_penalty']}%[/bold red]")

    b_table.add_row("[bold]Composite Nature Score[/bold]", f"[bold yellow]{score}%[/bold yellow]")
    console.print(b_table)

    if res["verified"]:
        state = unlock_terminal(res)
        console.print(UNLOCKED_BADGE)
        console.print(f"[bold green]Classification:[/bold green] {category}")
        console.print(f"[bold bright_green]🔥 Streak updated to {state['current_streak_days']} days! Now go ship great code.[/bold bright_green]\n")
        console.print(GRASS_FIELD)
    else:
        console.print(INDOOR_REJECTED)
        console.print(f"[bold red]Detection Result:[/bold red] {category} (Score: {score}%)")
        console.print("[italic yellow]Minimum 55% nature score required to verify grass contact.[/italic yellow]\n")

@main.command()
@click.option("--reason", default="Manual detox session initiated.", help="Reason for lock")
def lock(reason: str):
    """Manually lock the environment and enforce outdoor time."""
    lock_terminal(reason)
    console.print(LOCKED_BADGE)
    console.print(f"[bold red]System Locked:[/bold red] {reason}")
    console.print("[dim]Run 'git-grass verify <photo_of_grass.jpg>' after stepping outside to unlock.[/dim]")

@main.command()
def unlock():
    """Manually unlock terminal and reset session timer."""
    state = load_state()
    state["locked"] = False
    state["lock_reason"] = ""
    state["session_start_time"] = time.time()
    save_state(state)
    console.print("[bold green]✔ Git-grass lock manually cleared. Session timer reset.[/bold green]")

@main.command("hook-check")
def hook_check():
    """Internal command called by Git pre-commit hook."""
    locked, reason = is_locked()
    if locked:
        console.print(LOCKED_BADGE)
        console.print(f"[bold red]❌ Git Commit Blocked by git-grass:[/bold red] {reason}")
        console.print("[yellow]👉 Step outside, snap a photo of nature, and run:[/yellow]")
        console.print("   [bold white]git-grass verify <photo_of_grass.jpg>[/bold white]\n")
        sys.exit(1)
    else:
        # Healthy commit
        sys.exit(0)

@main.group()
def hook():
    """Manage Git pre-commit hooks."""
    pass

@hook.command("install")
@click.option("--repo", default=None, help="Path to repository")
def hook_install_cmd(repo: str):
    """Install git-grass pre-commit hook in current repo."""
    try:
        hook_path = install_hook(repo)
        console.print(f"[bold green]✔ git-grass pre-commit hook successfully installed at:[/bold green]\n  {hook_path}")
    except Exception as e:
        console.print(f"[bold red]Error installing hook:[/bold red] {e}")
        sys.exit(1)

@hook.command("remove")
@click.option("--repo", default=None, help="Path to repository")
def hook_remove_cmd(repo: str):
    """Remove git-grass pre-commit hook from current repo."""
    if remove_hook(repo):
        console.print("[bold green]✔ git-grass pre-commit hook removed.[/bold green]")
    else:
        console.print("[yellow]No git-grass hook found to remove.[/yellow]")

@main.command()
def demo():
    """Run an interactive demonstration of git-grass."""
    from git_grass.detector import NatureDetector
    import tempfile
    from PIL import Image, ImageDraw

    console.print(BANNER)
    console.print("[bold yellow]🎬 Running git-grass Interactive Demonstration...[/bold yellow]\n")

    detector = NatureDetector()

    # Create a synthetic outdoor grass/nature sample image
    grass_img = Image.new("RGB", (300, 300), color=(40, 160, 45))
    draw = ImageDraw.Draw(grass_img)
    for i in range(0, 300, 4):
        # Draw grass blades and organic variation
        draw.line([(i, 300), (i + (i % 7) - 3, 50 + (i % 40))], fill=(30 + (i % 30), 180 + (i % 40), 35 + (i % 25)), width=2)
    # Sky in top area
    for y in range(0, 70):
        draw.line([(0, y), (300, y)], fill=(120, 180, 240 - y), width=1)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f_grass:
        grass_path = f_grass.name
        grass_img.save(grass_path)

    # Create a synthetic indoor screen / code editor sample image
    screen_img = Image.new("RGB", (300, 300), color=(30, 30, 30))
    draw_s = ImageDraw.Draw(screen_img)
    # Draw code lines
    for y in range(30, 270, 15):
        draw_s.line([(20, y), (80 + (y * 3 % 150), y)], fill=(180, 180, 180), width=3)
        draw_s.line([(25, y+4), (60 + (y * 2 % 100), y+4)], fill=(100, 150, 200), width=2)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f_screen:
        screen_path = f_screen.name
        screen_img.save(screen_path)

    console.print("[bold cyan]Test 1: Simulating an Indoor IDE Screen Capture...[/bold cyan]")
    res_screen = detector.analyze_image(screen_path)
    console.print(f"Result: {res_screen['category']} (Score: {res_screen['nature_score']}%, Verified: {res_screen['verified']})")
    console.print("[red]❌ Rejection confirmed: Screen detected.[/red]\n")

    console.print("[bold cyan]Test 2: Simulating an Outdoor Grass & Sky Capture...[/bold cyan]")
    res_grass = detector.analyze_image(grass_path)
    console.print(f"Result: {res_grass['category']} (Score: {res_grass['nature_score']}%, Verified: {res_grass['verified']})")
    console.print("[green]✅ Verification confirmed: Real Nature detected![/green]\n")

    # Clean up
    try:
        os.unlink(grass_path)
        os.unlink(screen_path)
    except Exception:
        pass

    console.print(UNLOCKED_BADGE)
    console.print("[bold green]✔ Interactive Demo Complete![/bold green]")

if __name__ == "__main__":
    main()
