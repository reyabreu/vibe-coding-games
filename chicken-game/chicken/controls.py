"""Keyboard input for the player chicken.

Reads from ``chicken.assets.current_keys`` (refreshed every frame by the
main loop), so import the module rather than binding the attribute.
"""

import pygame

import chicken.assets as _assets
from chicken.entities import Chicken


def player_controls(chicken: Chicken) -> None:
    """Call once per frame; triggers a hop if a direction key is just held.

    Uses current_keys (held state) gated by the chicken's hopping flag so
    only one hop fires per keypress.  For edge-triggered input the main loop
    should pass KEYDOWN events instead — replace this function as needed.
    """
    if chicken.hopping:
        return
    keys = _assets.current_keys
    if keys[pygame.K_UP]    or keys[pygame.K_w]: chicken.hop( 0, -1)
    elif keys[pygame.K_DOWN]  or keys[pygame.K_s]: chicken.hop( 0,  1)
    elif keys[pygame.K_LEFT]  or keys[pygame.K_a]: chicken.hop(-1,  0)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: chicken.hop( 1,  0)
