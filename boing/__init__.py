"""Boing! – a Pong-style game built with pygame-ce.

Package layout
--------------
constants   pure numeric / string constants
settings    JSON-persisted user settings
assets      image / sound / key-state globals + loader
helpers     blit_centered, normalised, play_sound
entities    Impact, Ball, Bat, Game
controls    p1_controls, p2_controls  (keyboard input)
ui          State enum, draw_countdown, draw_settings_screen
game_loop   main() entry-point
"""
from boing.game_loop import main

__all__ = ["main"]
