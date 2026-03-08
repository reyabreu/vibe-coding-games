"""Global constants – no imports from this package."""

# 800×480 matches the original background-sprite dimensions
WIDTH = 800
HEIGHT = 480
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

TITLE = "Boing!"
FPS = 60

PLAYER_SPEED = 6  # pixels per physics sub-step

# Settings menus
SCORE_OPTIONS = [5, 7, 10, 15, 20]

# (label, max_ai_speed_per_substep, ai_offset_range)
DIFFICULTY_OPTIONS = [("Easy", 3, 40), ("Medium", 6, 10), ("Hard", 9, 3)]
