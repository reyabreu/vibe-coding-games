"""Keyboard input functions for player-controlled paddles.

These are passed as ``move_func`` callbacks to :class:`~boing.entities.Bat`.
They read from ``boing.assets.current_keys``, which the main loop refreshes
every frame, so the module must be imported (not its attribute).
"""

import pygame

import boing.assets as _assets
from boing.constants import PLAYER_SPEED


def p1_controls(game) -> float:
    """W / S keys for player 1 (left paddle)."""
    if _assets.current_keys[pygame.K_s]:
        return float(PLAYER_SPEED)
    if _assets.current_keys[pygame.K_w]:
        return float(-PLAYER_SPEED)
    return 0.0


def p2_controls(game) -> float:
    """Arrow-Up / Arrow-Down keys for player 2 (right paddle)."""
    if _assets.current_keys[pygame.K_DOWN]:
        return float(PLAYER_SPEED)
    if _assets.current_keys[pygame.K_UP]:
        return float(-PLAYER_SPEED)
    return 0.0
