# Bounce Redux

A 2D platformer built with Python and **Pygame** — a spiritual remake of the classic **Nokia Bounce** game, reimagined for PC. Guide a bouncing ball through obstacle-filled levels, collect rings, dodge enemies, and reach checkpoints to complete each stage.

## 🎮 Features

- Smooth jump and gravity physics reminiscent of the original Nokia classic
- Multiple levels with horizontal and vertical scrolling
- Static and moving enemies
- Life system with pickups that grant extra lives
- Checkpoints to respawn from after taking damage
- Coins/rings with **customizable sizes** (width and height can be adjusted independently)
- Level select menu with pagination
- Dynamic background that scales with level size

## 📁 Project Structure
├── main.py # Entry point, main menu and level select menu
├── game.py # Core game loop and level logic
├── player.py # Player class (physics, collisions, lives)
├── enemy.py # Enemy classes: static and moving
├── coin.py # Coin class with customizable dimensions
├── checkpoint.py # Checkpoint class
├── button.py # UI buttons (text, image, background-image)
├── level_manager.py # Loads levels from files or built-in maps
├── game_constants.py # Game constants, colors, image loading
├── levels/ # (optional) level map .txt files
└── img/ # Sprites and UI images

## 🕹 Controls

| Key                   | Action        |
|-----------------------|---------------|
| `A` / `←`             | Move left     |
| `D` / `→`             | Move right    |
| `Space` / `W` / `↑`   | Jump          |
| `Esc`                 | Pause         |

## 🚀 Installation & Running

1. Make sure Python 3.8+ is installed.
2. Install dependencies:
```bash
   pip install pygame
```
3. Run the game:
```bash
   python main.py
```

## 🖼 Images

If the sprite files in `img/` are missing, the game automatically falls back to colored placeholder shapes, so the project runs even without the original assets.
