"""Game entities: Chicken (player), Vehicle, Log, Lane, World.

All classes are stubs — flesh them out as each feature is vibe-coded in.
"""

from __future__ import annotations

import pygame

from chicken.constants import (
    WIDTH, HEIGHT, LANE_HEIGHT, CELL_W, GRID_COLS,
    PLAYER_SPEED, PLAYER_HOP_MS, LIVES_START, NUM_SAFE_SLOTS,
)


class Chicken:
    """The player character.

    Moves one grid cell per hop; animates for PLAYER_HOP_MS milliseconds.
    Carried horizontally by logs when standing on them.
    """

    def __init__(self) -> None:
        self.col: int   = GRID_COLS // 2      # current grid column (0-based)
        self.row: int   = 0                   # 0 = bottom safe zone
        self.x: float   = self.col * CELL_W + CELL_W / 2
        self.y: float   = HEIGHT - LANE_HEIGHT / 2
        self.lives: int = LIVES_START
        self.score: int = 0
        self.hopping: bool   = False
        self.hop_timer: float = 0.0           # ms remaining in hop animation
        self.facing: str = "up"               # "up" | "down" | "left" | "right"

    def hop(self, dx: int, dy: int) -> None:
        """Initiate a hop in a grid direction (dx/dy each -1, 0 or 1)."""
        if self.hopping:
            return
        self.col = max(0, min(GRID_COLS - 1, self.col + dx))
        self.row = self.row + dy
        self.x   = self.col * CELL_W + CELL_W / 2
        self.hopping   = True
        self.hop_timer = float(PLAYER_HOP_MS)
        if dx > 0:   self.facing = "right"
        elif dx < 0: self.facing = "left"
        elif dy < 0: self.facing = "up"
        else:        self.facing = "down"

    def update(self, dt_ms: float) -> None:
        if self.hopping:
            self.hop_timer -= dt_ms
            if self.hop_timer <= 0:
                self.hopping = False

    def draw(self, surface: pygame.Surface) -> None:
        # TODO: replace with sprite once assets exist
        col = (255, 220, 0)
        rect = pygame.Rect(0, 0, CELL_W - 4, LANE_HEIGHT - 4)
        rect.center = (round(self.x), round(self.y))
        pygame.draw.rect(surface, col, rect, border_radius=6)


class Vehicle:
    """A car or truck that moves horizontally across a road lane."""

    def __init__(self, x: float, y: float, speed: float, width: int,
                 color: tuple) -> None:
        self.x     = x
        self.y     = y
        self.speed = speed    # px/frame, negative = moving left
        self.w     = width
        self.color = color

    def update(self) -> None:
        self.x += self.speed
        # Wrap around when fully off-screen
        if self.speed > 0 and self.x > WIDTH + self.w:
            self.x = -self.w
        elif self.speed < 0 and self.x < -self.w:
            self.x = WIDTH + self.w

    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x) - self.w // 2,
                           round(self.y) - LANE_HEIGHT // 2 + 4,
                           self.w, LANE_HEIGHT - 8)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect(), border_radius=5)


class Log:
    """A floating log the chicken can ride across the river."""

    def __init__(self, x: float, y: float, speed: float, length: int) -> None:
        self.x      = x
        self.y      = y
        self.speed  = speed
        self.length = length

    def update(self) -> None:
        self.x += self.speed
        if self.speed > 0 and self.x > WIDTH + self.length:
            self.x = -self.length
        elif self.speed < 0 and self.x < -self.length:
            self.x = WIDTH + self.length

    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x) - self.length // 2,
                           round(self.y) - LANE_HEIGHT // 2 + 6,
                           self.length, LANE_HEIGHT - 12)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (139, 90, 43), self.rect(), border_radius=8)


class World:
    """Holds all lanes, vehicles, logs, and the player.

    TODO: build lanes from a level definition dict once the design is settled.
    """

    def __init__(self, vehicle_mult: float = 1.0, log_mult: float = 1.0) -> None:
        self.chicken  = Chicken()
        self.vehicles: list[Vehicle] = []
        self.logs:     list[Log]     = []
        self.safe_slots_filled: list[bool] = [False] * NUM_SAFE_SLOTS
        self.vehicle_mult = vehicle_mult
        self.log_mult     = log_mult
        # TODO: populate lanes with vehicles and logs

    def update(self, dt_ms: float) -> None:
        self.chicken.update(dt_ms)
        for v in self.vehicles:
            v.update()
        for log in self.logs:
            log.update()
        # TODO: collision detection, log-riding, death checks, scoring

    def draw(self, surface: pygame.Surface) -> None:
        # TODO: draw background lanes properly once art is ready
        surface.fill((34, 139, 34))   # placeholder green background
        for log in self.logs:
            log.draw(surface)
        for v in self.vehicles:
            v.draw(surface)
        self.chicken.draw(surface)
