"""UI utilities: game-state enum, animated countdown, settings screen."""

import math
from enum import Enum

import pygame

from boing.constants import (
    WIDTH, HEIGHT, HALF_WIDTH, HALF_HEIGHT,
    FPS, SCORE_OPTIONS, DIFFICULTY_OPTIONS,
)
from boing.assets import images
from boing.settings import settings


# ---------------------------------------------------------------------------
# Application state
# ---------------------------------------------------------------------------
class State(Enum):
    MENU       = 1
    PLAY       = 2
    GAME_OVER  = 3
    SETTINGS   = 4
    COUNTDOWN  = 5


# ---------------------------------------------------------------------------
# Countdown overlay
# ---------------------------------------------------------------------------
_CD_DIGITS  = [3, 2, 1]
_CD_TICKS   = FPS                          # frames per digit
_CD_TOTAL   = len(_CD_DIGITS) * _CD_TICKS  # total frames for the whole countdown
_CD_BASE_PX = 75                           # source sprite size
_CD_MAX_PX  = 420                          # size at end of grow
_CD_MIN_PX  = 60                           # size at start of grow
_GLOW_STEPS = 6                            # number of contour-shadow rings


def draw_countdown(surface: pygame.Surface, ticks: int) -> None:
    """Overlay an animated growing digit centred on screen."""
    idx      = ticks // _CD_TICKS
    progress = (ticks % _CD_TICKS) / _CD_TICKS
    digit    = _CD_DIGITS[idx]

    # Ease-out: fast start, slows near full size
    eased   = 1.0 - (1.0 - progress) ** 2
    px_size = max(1, int(_CD_MIN_PX + (_CD_MAX_PX - _CD_MIN_PX) * eased))

    # Fade: bright at start, dims toward the end of each digit
    fade_alpha = int(255 * (1.0 - progress * 0.55))

    src = images[f"digit0{digit}"]

    # Contour-following glow: mask each ring to the digit silhouette
    for step in range(_GLOW_STEPS, 0, -1):
        ring_size   = px_size + step * 10
        ring_scaled = pygame.transform.smoothscale(src, (ring_size, ring_size))
        mask        = pygame.mask.from_surface(ring_scaled, threshold=30)
        glow_surf   = mask.to_surface(
            setcolor=(0, 0, 0, int(40 + step * 22)),
            unsetcolor=(0, 0, 0, 0),
        )
        glow_surf.set_alpha(int(fade_alpha * 0.75 * (1.0 - step / (_GLOW_STEPS + 1))))
        surface.blit(glow_surf, (HALF_WIDTH - ring_size // 2, HALF_HEIGHT - ring_size // 2))

    # Thin bright outline just outside the digit edge
    outline_sz     = px_size + 5
    outline_scaled = pygame.transform.smoothscale(src, (outline_sz, outline_sz))
    outline_mask   = pygame.mask.from_surface(outline_scaled, threshold=30)
    outline_surf   = outline_mask.to_surface(
        setcolor=(210, 210, 210, 90),
        unsetcolor=(0, 0, 0, 0),
    )
    outline_surf.set_alpha(fade_alpha // 3)
    surface.blit(outline_surf, (HALF_WIDTH - outline_sz // 2, HALF_HEIGHT - outline_sz // 2))

    # Main digit
    big = pygame.transform.smoothscale(src, (px_size, px_size))
    big.set_alpha(fade_alpha)
    surface.blit(big, (HALF_WIDTH - px_size // 2, HALF_HEIGHT - px_size // 2))


# ---------------------------------------------------------------------------
# Settings screen
# ---------------------------------------------------------------------------
_PNL_W, _PNL_H = 460, 270
_PNL_X = (WIDTH  - _PNL_W) // 2
_PNL_Y = (HEIGHT - _PNL_H) // 2


def draw_settings_screen(
    surface: pygame.Surface,
    font_big: pygame.font.Font,
    font_mid: pygame.font.Font,
    font_small: pygame.font.Font,
    sel_row: int,
) -> None:
    """Draw the translucent settings panel over whatever is already on screen."""
    # Dim the game behind the panel
    dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 175))
    surface.blit(dim, (0, 0))

    # Panel background
    panel = pygame.Surface((_PNL_W, _PNL_H), pygame.SRCALPHA)
    panel.fill((18, 18, 55, 235))
    pygame.draw.rect(panel, (90, 90, 200), panel.get_rect(), 2, border_radius=10)
    surface.blit(panel, (_PNL_X, _PNL_Y))

    # Title + gear icon
    title_surf = font_big.render("SETTINGS", True, (190, 190, 255))
    tx = _PNL_X + (_PNL_W - title_surf.get_width()) // 2
    surface.blit(title_surf, (tx, _PNL_Y + 18))
    gear = images["settings"]
    surface.blit(gear, (tx - gear.get_width() - 8, _PNL_Y + 14))

    # Option rows
    rows = [
        ("Match Points",  str(SCORE_OPTIONS[settings["score_idx"]])),
        ("AI Difficulty", DIFFICULTY_OPTIONS[settings["difficulty_idx"]][0]),
    ]
    for i, (label, value) in enumerate(rows):
        ry       = _PNL_Y + 100 + i * 72
        selected = i == sel_row
        row_bg   = pygame.Surface((_PNL_W - 32, 54), pygame.SRCALPHA)
        row_bg.fill((70, 70, 150, 200) if selected else (35, 35, 75, 160))
        if selected:
            pygame.draw.rect(row_bg, (140, 140, 255), row_bg.get_rect(), 1, border_radius=5)
        surface.blit(row_bg, (_PNL_X + 16, ry))
        lbl_col = (255, 255, 255) if selected else (190, 190, 190)
        surface.blit(font_mid.render(label, True, lbl_col), (_PNL_X + 28, ry + 14))
        arrow_col = (255, 215, 60) if selected else (140, 140, 140)
        val_surf  = font_mid.render(f"\u25c4  {value}  \u25ba", True, arrow_col)
        surface.blit(val_surf, (_PNL_X + _PNL_W - 16 - val_surf.get_width(), ry + 14))

    # Nav hint
    hint = font_small.render(
        "\u2191\u2193  select      \u2190\u2192  change      SPACE / ESC  back",
        True, (120, 120, 165),
    )
    surface.blit(hint, (_PNL_X + (_PNL_W - hint.get_width()) // 2, _PNL_Y + _PNL_H - 28))
