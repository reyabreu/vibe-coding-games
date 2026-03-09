# vibe-coding-games

A collection of arcade games built with **vibe-coding** — an AI-assisted development workflow where ideas are described in natural language and GitHub Copilot iteratively generates, refines, and restructures the code.

All games use **[pygame-ce](https://pyga.me/)** (the community edition of pygame) and **Python 3.14+**, managed with **[uv](https://docs.astral.sh/uv/)**.

---

## Games

| Folder | Game | Description |
|--------|------|-------------|
| [`boing-game/`](boing-game/) | **Boing!** | A Pong-style game with sprite rendering, AI opponent, animated countdown, settings persistence, and victory music. |
| [`chicken-game/`](chicken-game/) | **Chicken Crossing!** | A Frogger-style game where a chicken dodges traffic and rides logs across a river. _(in development)_ |

---

## What is vibe-coding?

Vibe-coding is a development style where you describe *what* you want in plain language and let an AI coding assistant do the heavy lifting. The workflow looks like this:

1. **Describe** — express a feature or game idea conversationally ("add a 3-second animated countdown before each match")
2. **Generate** — the AI produces working code inline
3. **Play & iterate** — run the game, notice what feels off, describe the fix
4. **Refactor** — once features stabilise, ask the AI to restructure the code to professional standards

The result is fast prototyping without sacrificing quality, since refactoring and best-practice enforcement are part of the loop.

---

## Good practices for future games

### Project structure
Each game lives in its own subfolder (e.g. `snake-game/`, `asteroids-game/`). Inside, follow the same proven layout used in `boing-game/`:

```u
my-game/
    main.py              ← thin entry point (< 10 lines)
    pyproject.toml       ← uv/pip metadata and dependencies
    .python-version      ← pins the Python version for uv
    uv.lock              ← locked dependency tree for reproducibility
    images/              ← PNG sprites
    sounds/              ← OGG sound effects
    music/               ← OGG music tracks
    my_game/             ← Python package
        __init__.py
        constants.py     ← pure numeric / string constants
        settings.py      ← user settings with JSON persistence
        assets.py        ← image/sound globals + loader
        helpers.py       ← shared rendering & audio utilities
        entities.py      ← game objects (player, enemies, projectiles…)
        controls.py      ← keyboard / gamepad input functions
        ui.py            ← state enum, HUD, overlays, menus
        game_loop.py     ← main() and the state machine
```

### Assets and licensing
- Prefer **CC0 or MIT-licensed** assets so the whole repo stays redistributable.
- Document the asset source and licence in the game's own `README.md`.
- Keep raw/source files (e.g. `.xcf`, `.flp`) out of the repo — commit only the final exported files.

### Code conventions
- **One responsibility per module** — constants never import from the rest of the package; the dependency arrow flows one way.
- **No magic globals** — mutable shared state (e.g. `current_keys`) lives in a named module attribute, not a bare global reassigned across files.
- **Sub-step physics** for fast-moving objects — iterate `speed` times per frame advancing 1 px each step to prevent tunnelling through walls or paddles.
- **Delta-time or fixed sub-steps** — pick one and be consistent; mixing both leads to speed inconsistencies across frame rates.

### Settings persistence
- Store user preferences (volume, difficulty, keybinds) in a `settings.json` next to the executable.
- Always clamp / validate values on load so a corrupt file can't crash the game.
- List `settings.json` in `.gitignore` — it's user data, not source code.

### Git workflow
```bash
# Start a new game
mkdir snake-game && cd snake-game
uv init --python 3.14
uv add pygame-ce

# During development — commit often, in logical chunks
git add snake-game/
git commit -m "feat: add player movement and wrapping"
git push
```

- Commit **per feature**, not per session.
- Use the `feat:`, `fix:`, `refactor:`, `chore:` prefix convention for commit messages.
- Keep assets in the same commit as the code that first uses them.
