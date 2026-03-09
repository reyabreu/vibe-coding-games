"""Persistent Hall of Fame — last 5 human-beats-AI victories."""

import datetime
import json
import pathlib

from boing.constants import DIFFICULTY_OPTIONS

_WINNERS_FILE = pathlib.Path("winners.json")
MAX_ENTRIES   = 5

winners: list[dict] = []


def load_winners() -> None:
    """Populate the in-memory list from the JSON file."""
    global winners
    if not _WINNERS_FILE.exists():
        return
    try:
        data = json.loads(_WINNERS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            winners = [
                {
                    "name":       str(e.get("name", "???"))[:12],
                    "date":       str(e.get("date", "")),
                    "difficulty": str(e.get("difficulty", "")),
                }
                for e in data
                if isinstance(e, dict)
            ][:MAX_ENTRIES]
    except Exception:
        pass


def save_winners() -> None:
    try:
        _WINNERS_FILE.write_text(json.dumps(winners, indent=2), encoding="utf-8")
    except Exception:
        pass


def add_winner(name: str, difficulty_idx: int) -> None:
    """Prepend a new entry, trim to MAX_ENTRIES, then persist."""
    entry = {
        "name":       (name.strip() or "???")[:12],
        "date":       datetime.date.today().isoformat(),
        "difficulty": DIFFICULTY_OPTIONS[difficulty_idx][0],
    }
    winners.insert(0, entry)
    del winners[MAX_ENTRIES:]
    save_winners()
