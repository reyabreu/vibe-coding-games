"""Main game loop and application entry point."""

import sys

import pygame

import boing.assets as assets
from boing.assets import load_assets, images
from boing.constants import WIDTH, HEIGHT, TITLE, FPS, SCORE_OPTIONS, DIFFICULTY_OPTIONS
from boing.controls import p1_controls, p2_controls
from boing.entities import Game
from boing.helpers import play_sound
from boing.settings import load_settings, save_settings, settings
from boing.ui import (
    State,
    draw_countdown,
    draw_settings_screen,
    _CD_TOTAL,
)


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
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    font_big   = pygame.font.SysFont(None, 44)
    font_mid   = pygame.font.SysFont(None, 30)
    font_small = pygame.font.SysFont(None, 22)

    state            = State.MENU
    num_players      = 1
    settings_row     = 0     # 0 = Match Points row, 1 = AI Difficulty row
    game             = Game()  # attract-mode: both paddles are AI
    game_result      = "over"  # "over" | "you_won" | "player1_won" | "player2_won"
    countdown_ticks  = 0

    prev_keys = pygame.key.get_pressed()

    running = True
    while running:
        assets.current_keys = pygame.key.get_pressed()

        def just_pressed(key: int) -> bool:
            return bool(assets.current_keys[key]) and not bool(prev_keys[key])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ESC on menu = quit; ESC anywhere else = back to menu
        if just_pressed(pygame.K_ESCAPE):
            if state == State.MENU:
                running = False
            else:
                state = State.MENU
                game  = Game()
                game_result = "over"
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("music/theme.ogg")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
                except Exception:
                    pass

        # ---- State machine -------------------------------------------------
        if state == State.MENU:
            if just_pressed(pygame.K_SPACE):
                controls = (p1_controls, p2_controls if num_players == 2 else None)
                game = Game(controls)
                countdown_ticks = 0
                state = State.COUNTDOWN
            elif just_pressed(pygame.K_o):
                settings_row = 0
                state = State.SETTINGS
            else:
                if just_pressed(pygame.K_UP) and num_players == 2:
                    play_sound("up", 1, is_menu=True)
                    num_players = 1
                elif just_pressed(pygame.K_DOWN) and num_players == 1:
                    play_sound("down", 1, is_menu=True)
                    num_players = 2
                game.update()  # keep attract mode running in background

        elif state == State.COUNTDOWN:
            countdown_ticks += 1
            # Let both paddles respond to input so players can test their keys
            for bat in game.bats:
                bat.update(game)
            if countdown_ticks >= _CD_TOTAL:
                state = State.PLAY

        elif state == State.PLAY:
            if max(game.bats[0].score, game.bats[1].score) >= game.winning_score:
                two_player = not game.bats[0].is_ai and not game.bats[1].is_ai
                human_won  = (
                    not game.bats[0].is_ai
                    and game.bats[1].is_ai
                    and game.bats[0].score >= game.winning_score
                )
                if two_player:
                    game_result = (
                        "player1_won"
                        if game.bats[0].score >= game.winning_score
                        else "player2_won"
                    )
                elif human_won:
                    game_result = "you_won"
                else:
                    game_result = "over"

                if human_won:
                    try:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("music/victory.ogg")
                        pygame.mixer.music.set_volume(0.7)
                        pygame.mixer.music.play(0)
                    except Exception:
                        pass
                state = State.GAME_OVER
            else:
                game.update()

        elif state == State.GAME_OVER:
            if just_pressed(pygame.K_SPACE):
                state = State.MENU
                num_players = 1
                game = Game()
                game_result = "over"
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("music/theme.ogg")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
                except Exception:
                    pass

        elif state == State.SETTINGS:
            if just_pressed(pygame.K_SPACE):
                state = State.MENU
            elif just_pressed(pygame.K_UP):
                settings_row = (settings_row - 1) % 2
                play_sound("up", 1, is_menu=True)
            elif just_pressed(pygame.K_DOWN):
                settings_row = (settings_row + 1) % 2
                play_sound("down", 1, is_menu=True)
            elif just_pressed(pygame.K_LEFT):
                if settings_row == 0:
                    settings["score_idx"] = max(0, settings["score_idx"] - 1)
                else:
                    settings["difficulty_idx"] = max(0, settings["difficulty_idx"] - 1)
                save_settings()
                play_sound("up", 1, is_menu=True)
            elif just_pressed(pygame.K_RIGHT):
                if settings_row == 0:
                    settings["score_idx"] = min(
                        len(SCORE_OPTIONS) - 1, settings["score_idx"] + 1
                    )
                else:
                    settings["difficulty_idx"] = min(
                        len(DIFFICULTY_OPTIONS) - 1, settings["difficulty_idx"] + 1
                    )
                save_settings()
                play_sound("down", 1, is_menu=True)

        # ---- Draw ----------------------------------------------------------
        game.draw(screen)

        if state == State.MENU:
            screen.blit(images[f"menu{num_players - 1}"], (0, 0))
            gear = images["settings"]
            gx = WIDTH  - gear.get_width()  - 12
            gy = HEIGHT - gear.get_height() - 10
            screen.blit(gear, (gx, gy))
            hint = font_small.render("O = Settings", True, (170, 170, 170))
            screen.blit(hint, (gx - hint.get_width() - 8,
                               gy + (gear.get_height() - hint.get_height()) // 2))

        elif state == State.GAME_OVER:
            screen.blit(images[game_result], (0, 0))

        elif state == State.SETTINGS:
            draw_settings_screen(screen, font_big, font_mid, font_small, settings_row)

        elif state == State.COUNTDOWN:
            draw_countdown(screen, countdown_ticks)

        pygame.display.flip()
        clock.tick(FPS)
        prev_keys = assets.current_keys

    pygame.quit()
    sys.exit()
