"""
ASCII Art and visual themes for git-grass.
"""

BANNER = r"""
[bold green]
   ,        .      .       .         .      ,
  / \      / \    / \     / \       / \    / \
 /   \    /   \  /   \   /   \     /   \  /   \
 | | |    | | |  | | |   | | |     | | |  | | |
[/bold green][bold bright_green]
       _ _                                
  __ _(_) |_ ______ __ _ _ __ __ _ ___ ___
 / _` | | __|______/ _` | '__/ _` / __/ __|
| (_| | | |_      | (_| | | | (_| \__ \__ \
 \__, |_|\__|      \__, |_|  \__,_|___/___/
 |___/             |___/                   
[/bold bright_green]
[dim green]   ~ Touch Grass to Unlock Your Commits ~[/dim green]
"""

GRASS_FIELD = r"""[green]
        \|/        /|/       \|/            \|/        /|/
       \\|//      //|\\     \\|//          \\|//      //|\\
      \\\\|////  ///|\\\\  \\\\|////      \\\\|////  ///|\\\\
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[/green]"""

LOCKED_BADGE = r"""[bold red]
 ╔════════════════════════════════════════════════════════════╗
 ║                     🔒 GIT COMMITS LOCKED                   ║
 ║                                                            ║
 ║   You have been coding for too long without outdoors time! ║
 ║   Git commits are paused until you touch real grass.       ║
 ║                                                            ║
 ║   Run: [bold white]git-grass verify <photo_of_grass.jpg>[/bold white]            ║
 ╚════════════════════════════════════════════════════════════╝
[/bold red]"""

UNLOCKED_BADGE = r"""[bold green]
 ╔════════════════════════════════════════════════════════════╗
 ║                🌱 PROOF OF NATURE VERIFIED! 🌱              ║
 ║                                                            ║
 ║   Open-weight AI confirmed genuine outdoor nature contact! ║
 ║   Git lock released. Happy coding (with fresh air in mind) ║
 ╚════════════════════════════════════════════════════════════╝
[/bold green]"""

INDOOR_REJECTED = r"""[bold yellow]
 ╔════════════════════════════════════════════════════════════╗
 ║                  🚫 NICE TRY, DEVELOPER!                   ║
 ║                                                            ║
 ║   Our local vision model detected indoor screen/desk       ║
 ║   artifacts. Staring at an IDE wallpaper doesn't count.   ║
 ║                                                            ║
 ║   Step away from the keyboard and find REAL greenery!      ║
 ╚════════════════════════════════════════════════════════════╝
[/bold yellow]"""
