"""Chicken Crossing – a Frogger-style game built with pygame-ce.

Package layout
--------------
constants   pure numeric / string constants
settings    JSON-persisted user settings
assets      image / sound / key-state globals + loader
helpers     blit_centered, play_sound
entities    Chicken, Lane, Vehicle, Log, River, World
controls    keyboard input function
ui          State enum, HUD, menus, overlays
game_loop   main() entry-point
"""
from chicken.game_loop import main

__all__ = ["main"]
