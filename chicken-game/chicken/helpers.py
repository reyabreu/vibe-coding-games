"""Shared rendering and audio utility functions."""

import random

import pygame

from chicken.assets import images, sounds


def blit_centered(surface: pygame.Surface, name: str, cx: float, cy: float) -> None:
    """Blit sprite *name* so its centre is at (cx, cy)."""
    img = images[name]
    surface.blit(img, (round(cx) - img.get_width() // 2,
                       round(cy) - img.get_height() // 2))


def play_sound(name: str, count: int = 1) -> None:
    """Play a random variant of *name* (silently ignores missing sounds)."""
    try:
        sounds[name + str(random.randint(0, count - 1))].play()
    except Exception:
        pass
