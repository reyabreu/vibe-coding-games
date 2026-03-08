"""Shared rendering and audio utility functions."""

import math
import random

import pygame

from boing.assets import images, sounds


def blit_centered(surface: pygame.Surface, name: str, cx: float, cy: float) -> None:
    """Blit sprite *name* so its centre is at (cx, cy)."""
    img = images[name]
    surface.blit(img, (round(cx) - img.get_width() // 2,
                       round(cy) - img.get_height() // 2))


def normalised(x: float, y: float) -> tuple[float, float]:
    length = math.hypot(x, y)
    return (x / length, y / length) if length else (x, y)


def play_sound(
    name: str,
    count: int = 1,
    is_menu: bool = False,
    bats: list | None = None,
) -> None:
    """Play a random variant of *name*.

    In-game sounds are suppressed during attract mode (both paddles AI).
    """
    if bats is not None and not is_menu and bats[0].is_ai:
        return
    try:
        sounds[name + str(random.randint(0, count - 1))].play()
    except Exception:
        pass
