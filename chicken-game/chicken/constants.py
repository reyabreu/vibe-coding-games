"""Global constants — no imports from this package."""

# Display
WIDTH  = 800
HEIGHT = 600
TITLE  = "Chicken Crossing!"
FPS    = 60

# Grid — the world is divided into equal-height lanes
LANE_HEIGHT = 60          # pixels per lane
GRID_COLS   = 14          # number of grid columns
CELL_W      = WIDTH // GRID_COLS

# Player
PLAYER_SPEED    = CELL_W  # one cell per hop (pixels)
PLAYER_HOP_MS   = 120     # animation duration of a single hop (milliseconds)

# Game rules
NUM_SAFE_SLOTS  = 5       # lily-pad / home slots at the top of the screen
LIVES_START     = 3

# Score
SCORE_HOP         =   10   # points per hop forward
SCORE_SAFE        =  200   # points for reaching a safe slot
SCORE_ALL_SAFE    = 1000   # bonus for filling all safe slots
SCORE_TIME_BONUS  =   10   # multiplied by remaining time per safe arrival
TIME_LIMIT_S      =   60   # seconds to fill all slots

# Difficulty presets  (label, vehicle_speed_mult, log_speed_mult)
DIFFICULTY_OPTIONS = [
    ("Easy",   0.7, 0.6),
    ("Medium", 1.0, 1.0),
    ("Hard",   1.4, 1.4),
]
