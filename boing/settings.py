"""Mutable user settings with JSON persistence."""

import json
import pathlib

from boing.constants import SCORE_OPTIONS, DIFFICULTY_OPTIONS

_SETTINGS_FILE = pathlib.Path("settings.json")
_SETTINGS_DEFAULTS: dict = {
    "score_idx":      2,   # SCORE_OPTIONS[2] = 10
    "difficulty_idx": 1,   # DIFFICULTY_OPTIONS[1] = Medium
}

settings: dict = dict(_SETTINGS_DEFAULTS)


def load_settings() -> None:
    """Overwrite the in-memory settings dict from the JSON file (if it exists)."""
    if not _SETTINGS_FILE.exists():
        return
    try:
        data = json.loads(_SETTINGS_FILE.read_text(encoding="utf-8"))
        for key, default in _SETTINGS_DEFAULTS.items():
            raw = data.get(key, default)
            # Clamp indices so a corrupt file can't crash us
            if key == "score_idx":
                raw = max(0, min(len(SCORE_OPTIONS) - 1, int(raw)))
            elif key == "difficulty_idx":
                raw = max(0, min(len(DIFFICULTY_OPTIONS) - 1, int(raw)))
            settings[key] = raw
    except Exception:
        pass  # silently keep defaults if the file is malformed


def save_settings() -> None:
    """Write the current in-memory settings dict to the JSON file."""
    try:
        _SETTINGS_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    except Exception:
        pass


def current_winning_score() -> int:
    return SCORE_OPTIONS[settings["score_idx"]]


def current_ai_params() -> tuple[int, int]:
    """Return (max_speed, offset_range) for the selected difficulty."""
    _, spd, offset = DIFFICULTY_OPTIONS[settings["difficulty_idx"]]
    return spd, offset
