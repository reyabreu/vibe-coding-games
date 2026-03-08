# Boing!

A classic two-player Pong-style game built in Python with [pygame-ce](https://pyga.me/), created via **vibe coding** with GitHub Copilot.

## Requirements

- Python >= 3.14
- [uv](https://github.com/astral-sh/uv) (recommended package manager)

## Setup

### Using uv (recommended)

```powershell
# Install dependencies and create the virtual environment
uv sync
```

### Manual venv

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pygame-ce
```

## Run

```powershell
# With uv
uv run python main.py

# Or activate the venv first
.venv\Scripts\Activate.ps1
python main.py
```

## Controls

| Key / Action | Effect |
|---|---|
| `W` / `S` | Player 1 paddle up / down |
| `↑` / `↓` | Player 2 paddle up / down (2P mode) |
| `↑` / `↓` on menu | Switch 1-player / 2-player mode |
| `Space` | Start game / restart after game over |
| `Escape` | Quit |
| Close window | Quit |

## Gameplay

- First player to reach **10 points** wins.
- The ball speeds up with every paddle hit (sub-step physics — no tunnelling).
- Deflection angle depends on where the ball strikes the paddle.
- **1-player mode**: play against an AI that tracks the ball with weighted prediction.
- **2-player mode**: both paddles are human-controlled.
- An **attract mode** (two AIs playing each other) runs in the background on the menu.

## Project Structure

```
main.py          # Game entrypoint and main loop
pyproject.toml   # Project metadata and dependencies
uv.lock          # Locked dependency versions
```
