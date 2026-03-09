"""UI utilities: State enum, HUD, menus, overlays."""

from enum import Enum

import pygame

from chicken.constants import (
    WIDTH, HEIGHT, DIFFICULTY_OPTIONS, LIVES_START,
)
from chicken.settings import settings


# ---------------------------------------------------------------------------
# Application states
# ---------------------------------------------------------------------------
class State(Enum):
    MENU      = 1
    PLAY      = 2
    PAUSED    = 3
    GAME_OVER = 4
    SETTINGS  = 5
    WIN       = 6    # all safe slots filled


# ---------------------------------------------------------------------------
# HUD
# ---------------------------------------------------------------------------
def draw_hud(
    surface: pygame.Surface,
    font: pygame.font.Font,
    score: int,
    lives: int,
    time_left: float,
) -> None:
    """Draw score, lives, and timer at the top of the screen."""
    bar = pygame.Surface((WIDTH, 36), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 160))
    surface.blit(bar, (0, 0))

    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_surf = font.render(f"Lives: {lives}", True, (255, 220, 60))
    timer_col  = (255, 80, 80) if time_left < 10 else (255, 255, 255)
    timer_surf = font.render(f"Time: {int(time_left):02d}", True, timer_col)

    surface.blit(score_surf, (12, 8))
    surface.blit(lives_surf, (WIDTH // 2 - lives_surf.get_width() // 2, 8))
    surface.blit(timer_surf, (WIDTH - timer_surf.get_width() - 12, 8))


# ---------------------------------------------------------------------------
# Menu screen
# ---------------------------------------------------------------------------
def draw_menu(
    surface: pygame.Surface,
    font_big: pygame.font.Font,
    font_mid: pygame.font.Font,
    font_small: pygame.font.Font,
) -> None:
    surface.fill((20, 80, 20))

    title = font_big.render("CHICKEN CROSSING!", True, (255, 220, 0))
    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    diff_name = DIFFICULTY_OPTIONS[settings["difficulty_idx"]][0]
    lines = [
        ("SPACE  —  Start",           (200, 255, 200)),
        (f"D  —  Difficulty: {diff_name}", (180, 220, 180)),
        ("ESC  —  Quit",              (180, 180, 180)),
    ]
    for i, (text, col) in enumerate(lines):
        surf = font_mid.render(text, True, col)
        surface.blit(surf, (WIDTH // 2 - surf.get_width() // 2,
                            HEIGHT // 2 + i * 44))

    hint = font_small.render("Arrow keys / WASD to move", True, (130, 180, 130))
    surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 34))


# ---------------------------------------------------------------------------
# Game Over overlay
# ---------------------------------------------------------------------------
def draw_game_over(
    surface: pygame.Surface,
    font_big: pygame.font.Font,
    font_mid: pygame.font.Font,
    score: int,
) -> None:
    dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 170))
    surface.blit(dim, (0, 0))

    title = font_big.render("GAME OVER", True, (220, 60, 60))
    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))

    sc = font_mid.render(f"Score: {score}", True, (255, 255, 255))
    surface.blit(sc, (WIDTH // 2 - sc.get_width() // 2, HEIGHT // 2))

    hint = font_mid.render("SPACE  —  Main Menu", True, (180, 180, 180))
    surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 52))


# ---------------------------------------------------------------------------
# Win overlay
# ---------------------------------------------------------------------------
def draw_win(
    surface: pygame.Surface,
    font_big: pygame.font.Font,
    font_mid: pygame.font.Font,
    score: int,
) -> None:
    dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 150))
    surface.blit(dim, (0, 0))

    title = font_big.render("YOU MADE IT!", True, (255, 220, 0))
    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))

    sc = font_mid.render(f"Score: {score}", True, (255, 255, 255))
    surface.blit(sc, (WIDTH // 2 - sc.get_width() // 2, HEIGHT // 2))

    hint = font_mid.render("SPACE  —  Play Again", True, (180, 220, 180))
    surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 52))
