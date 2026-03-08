"""Game entities: Impact, Ball, Bat, Game."""

import random

import pygame

from boing.constants import HALF_WIDTH, HALF_HEIGHT, WIDTH
from boing.assets import images
from boing.helpers import blit_centered, normalised, play_sound
from boing.settings import current_winning_score, current_ai_params


class Impact:
    """Bounce-particle: plays through a 5-frame animation over 10 ticks."""

    def __init__(self, cx: float, cy: float) -> None:
        self.cx = cx
        self.cy = cy
        self.time = 0

    def update(self) -> None:
        self.time += 1

    def draw(self, surface: pygame.Surface) -> None:
        frame = self.time // 2
        if 0 <= frame <= 4:
            blit_centered(surface, f"impact{frame}", self.cx, self.cy)


class Ball:
    """Ball with sub-step physics (1 px × speed iterations per frame)."""

    def __init__(self, dx: int) -> None:
        self.x = float(HALF_WIDTH)
        self.y = float(HALF_HEIGHT)
        self.dx = float(dx)
        self.dy = 0.0
        self.speed = 5  # sub-steps per frame; grows with each paddle hit

    def update(self, game: "Game") -> None:
        for _ in range(self.speed):
            original_x = self.x
            self.x += self.dx
            self.y += self.dy

            # Paddle collision at 344 px from centre
            # (HALF_WIDTH - bat_margin - bat_half_width - ball_half_width = 400-40-9-7 = 344)
            if abs(self.x - HALF_WIDTH) >= 344 and abs(original_x - HALF_WIDTH) < 344:
                bat = game.bats[0] if self.x < HALF_WIDTH else game.bats[1]
                new_dir_x = 1 if self.x < HALF_WIDTH else -1
                diff_y = self.y - bat.y
                if abs(diff_y) < 64:
                    self.dx = -self.dx
                    self.dy += diff_y / 128
                    self.dy = max(-1.0, min(1.0, self.dy))
                    self.dx, self.dy = normalised(self.dx, self.dy)
                    game.impacts.append(Impact(self.x - new_dir_x * 10, self.y))
                    self.speed += 1
                    game.ai_offset = random.randint(
                        -game.ai_offset_range, game.ai_offset_range
                    )
                    bat.timer = 10
                    play_sound("hit", 5, bats=game.bats)
                    if self.speed <= 10:
                        play_sound("hit_slow", 1, bats=game.bats)
                    elif self.speed <= 12:
                        play_sound("hit_medium", 1, bats=game.bats)
                    elif self.speed <= 16:
                        play_sound("hit_fast", 1, bats=game.bats)
                    else:
                        play_sound("hit_veryfast", 1, bats=game.bats)

            # Top / bottom walls
            if abs(self.y - HALF_HEIGHT) > 220:
                self.dy = -self.dy
                self.y += self.dy
                game.impacts.append(Impact(self.x, self.y))
                play_sound("bounce", 5, bats=game.bats)
                play_sound("bounce_synth", 1, bats=game.bats)

    def out(self) -> bool:
        return self.x < 0 or self.x > WIDTH

    def draw(self, surface: pygame.Surface) -> None:
        blit_centered(surface, "ball", self.x, self.y)


class Bat:
    """Player paddle with optional AI movement."""

    def __init__(
        self,
        player: int,
        move_func=None,
        ai_max_speed: int = 6,
        ai_offset_range: int = 10,
    ) -> None:
        self.player = player
        self.x = 40.0 if player == 0 else 760.0
        self.y = float(HALF_HEIGHT)
        self.score = 0
        self.timer = 0
        self.is_ai = move_func is None
        self.ai_max_speed = float(ai_max_speed)
        self.move_func = self.ai if move_func is None else move_func
        self.image = f"bat{player}0"

    def update(self, game: "Game") -> None:
        self.timer -= 1
        self.y += self.move_func(game)
        self.y = max(80.0, min(400.0, self.y))
        frame = 0
        if self.timer > 0:
            frame = 2 if game.ball.out() else 1
        self.image = f"bat{self.player}{frame}"

    def ai(self, game: "Game") -> float:
        """Weighted-average tracker: centres when far, tracks ball when close."""
        x_dist = abs(game.ball.x - self.x)
        w1 = min(1.0, x_dist / HALF_WIDTH)
        target_y = w1 * HALF_HEIGHT + (1.0 - w1) * (game.ball.y + game.ai_offset)
        return max(-self.ai_max_speed, min(self.ai_max_speed, target_y - self.y))

    def draw(self, surface: pygame.Surface) -> None:
        blit_centered(surface, self.image, self.x, self.y)


class Game:
    """Top-level game state: two bats, one ball, impact particles."""

    def __init__(self, controls: tuple = (None, None)) -> None:
        spd, offset_range = current_ai_params()
        self.bats = [
            Bat(0, controls[0], spd, offset_range),
            Bat(1, controls[1], spd, offset_range),
        ]
        self.ball = Ball(-1)
        self.impacts: list[Impact] = []
        self.ai_offset = 0
        self.ai_offset_range = offset_range
        self.winning_score = current_winning_score()

    def update(self) -> None:
        for bat in self.bats:
            bat.update(self)

        # Snapshot existing impacts so ball.update() can safely append new ones
        # without them being stepped on the same frame they were born.
        pre_impacts = list(self.impacts)
        self.ball.update(self)
        for imp in pre_impacts:
            imp.update()
        self.impacts = [imp for imp in self.impacts if imp.time < 10]

        if self.ball.out():
            scoring = 1 if self.ball.x < HALF_WIDTH else 0
            losing  = 1 - scoring
            if self.bats[losing].timer < 0:
                self.bats[scoring].score += 1
                play_sound("score_goal", 1, bats=self.bats)
                self.bats[losing].timer = 20
            elif self.bats[losing].timer == 0:
                direction = -1 if losing == 0 else 1
                self.ball = Ball(direction)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(images["table"], (0, 0))

        for p in range(2):
            if self.bats[p].timer > 0 and self.ball.out():
                surface.blit(images[f"effect{p}"], (0, 0))

        for bat in self.bats:
            bat.draw(surface)
        self.ball.draw(surface)
        for imp in self.impacts:
            imp.draw(surface)

        # Sprite-based score display
        for p in range(2):
            score_str = f"{self.bats[p].score:02d}"
            for i in range(2):
                colour = "0"
                other_p = 1 - p
                if self.bats[other_p].timer > 0 and self.ball.out():
                    colour = "2" if p == 0 else "1"
                surface.blit(
                    images[f"digit{colour}{score_str[i]}"],
                    (255 + 160 * p + 55 * i, 46),
                )
