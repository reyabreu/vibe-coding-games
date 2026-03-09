"""Main game loop and application entry point."""

import sys

import pygame

import chicken.assets as assets
from chicken.assets import load_assets
from chicken.constants import WIDTH, HEIGHT, TITLE, FPS, DIFFICULTY_OPTIONS, TIME_LIMIT_S
from chicken.controls import player_controls
from chicken.entities import World
from chicken.settings import load_settings, save_settings, settings, current_difficulty
from chicken.ui import State, draw_hud, draw_menu, draw_game_over, draw_win


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.Clock()

    try:
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 1024)
    except Exception:
        pass

    load_settings()
    load_assets()

    try:
        pygame.mixer.music.load("music/theme.ogg")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    font_big   = pygame.font.SysFont(None, 64)
    font_mid   = pygame.font.SysFont(None, 36)
    font_small = pygame.font.SysFont(None, 24)

    state      = State.MENU
    world      = World()
    time_left  = float(TIME_LIMIT_S)

    prev_keys = pygame.key.get_pressed()

    running = True
    while running:
        dt_ms = clock.tick(FPS)
        assets.current_keys = pygame.key.get_pressed()

        def just_pressed(key: int) -> bool:
            return bool(assets.current_keys[key]) and not bool(prev_keys[key])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if just_pressed(pygame.K_ESCAPE):
            if state == State.MENU:
                running = False
            else:
                state = State.MENU

        # ---- State machine -------------------------------------------------
        if state == State.MENU:
            if just_pressed(pygame.K_SPACE):
                v_mult, l_mult = current_difficulty()
                world     = World(v_mult, l_mult)
                time_left = float(TIME_LIMIT_S)
                state     = State.PLAY
            elif just_pressed(pygame.K_d):
                settings["difficulty_idx"] = (
                    (settings["difficulty_idx"] + 1) % len(DIFFICULTY_OPTIONS)
                )
                save_settings()

        elif state == State.PLAY:
            time_left -= dt_ms / 1000.0
            player_controls(world.chicken)
            world.update(dt_ms)

            if time_left <= 0 or world.chicken.lives <= 0:
                state = State.GAME_OVER
            elif all(world.safe_slots_filled):
                state = State.WIN

        elif state == State.GAME_OVER:
            if just_pressed(pygame.K_SPACE):
                state = State.MENU

        elif state == State.WIN:
            if just_pressed(pygame.K_SPACE):
                v_mult, l_mult = current_difficulty()
                world     = World(v_mult, l_mult)
                time_left = float(TIME_LIMIT_S)
                state     = State.PLAY

        # ---- Draw ----------------------------------------------------------
        if state == State.MENU:
            draw_menu(screen, font_big, font_mid, font_small)

        else:
            world.draw(screen)
            draw_hud(screen, font_mid, world.chicken.score,
                     world.chicken.lives, time_left)

            if state == State.GAME_OVER:
                draw_game_over(screen, font_big, font_mid, world.chicken.score)
            elif state == State.WIN:
                draw_win(screen, font_big, font_mid, world.chicken.score)

        pygame.display.flip()
        prev_keys = assets.current_keys

    pygame.quit()
    sys.exit()
