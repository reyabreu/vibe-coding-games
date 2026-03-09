"""Mutable user settings with JSON persistence."""

import json
import pathlib

from chicken.constants import DIFFICULTY_OPTIONS

_SETTINGS_FILE = pathlib.Path("settings.json")
_SETTINGS_DEFAULTS: dict = {
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
            if key == "difficulty_idx":
                raw = max(0, min(len(DIFFICULTY_OPTIONS) - 1, int(raw)))
            settings[key] = raw
    except Exception:
        pass


def save_settings() -> None:
    try:
        _SETTINGS_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    except Exception:
        pass


def current_difficulty() -> tuple[float, float]:
    """Return (vehicle_speed_mult, log_speed_mult) for the selected difficulty."""
    _, v, l = DIFFICULTY_OPTIONS[settings["difficulty_idx"]]
    return v, l
