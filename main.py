"""Peaceful War — Slice 0 + UI System.

Controls:
  TITLE / MENUS:
    UP / DOWN : Navigate options
    ENTER / SPACE : Select option
    ESC : Back / Exit
  MATCH:
    LEFT / RIGHT : Aim angle
    UP / DOWN : Adjust power
    TAB : Switch weapon (Shell / Laser)
    ESC : Pause menu
    F11 : Fullscreen toggle

Run:        .venv/Scripts/python.exe main.py
Screenshot: .venv/Scripts/python.exe main.py --shot out/screen.png [--screen title|play|lab|help]
"""

import math
import os
import random
import sys

import pygame

import config as C
from algo.lines import line_bresenham
from core.canvas import Canvas
from core.display import Display
from core.util import clamp, lerp_color
from world.terrain import Terrain
from ui import (
    TitleScreen,
    HowToPlayScreen,
    HUD,
    PauseOverlay,
    GameOverScreen,
    LabScreen,
)


# --- static background ----------------------------------------------------
def draw_sky(cv):
    for y in range(cv.h):
        t = (y / (cv.h - 1)) ** 1.35
        cv.hline(0, cv.w - 1, y, lerp_color(C.SKY_TOP, C.SKY_BOTTOM, t))


def draw_stars(cv, count=90, seed=3):
    rng = random.Random(seed)
    for _ in range(count):
        x = rng.randrange(cv.w)
        y = rng.randrange(int(cv.h * 0.62))
        cv.blend_pixel(x, y, C.STAR, rng.randrange(60, 220))


def build_sky(cv):
    draw_sky(cv)
    draw_stars(cv)


def rebuild_background(cv, terrain, sky):
    cv.restore(sky)
    terrain.render(cv)
    return cv.snapshot()


# --- dynamic layer --------------------------------------------------------
def draw_tank(cv, x, y, angle, color):
    x = int(x)
    y = int(y)
    cv.rect(x - 11, y - 5, 22, 5, C.TRACK)
    for tx in range(x - 10, x + 10, 4):
        cv.set_pixel(tx, y - 4, (58, 48, 56))
    cv.rect(x - 8, y - 9, 16, 4, color)
    cv.rect(x - 3, y - 12, 6, 3, color)

    rad = math.radians(angle)
    bx = x + math.cos(rad) * 12
    by = y - 12 - math.sin(rad) * 12
    line_bresenham(cv, x, y - 11, bx, by, color)


def draw_world(cv, background, terrain, tanks):
    cv.restore(background)
    for tank in tanks:
        x = tank["x"]
        y = terrain.height_at(x)
        draw_tank(cv, x, y, tank["angle"], tank["color"])


def main(argv):
    shot = None
    target_screen = "title"
    if "--shot" in argv:
        shot = argv[argv.index("--shot") + 1]
    if "--screen" in argv:
        target_screen = argv[argv.index("--screen") + 1].lower()

    display = Display("Peaceful War", C.WIDTH, C.HEIGHT, C.WINDOW_SCALE)
    canvas = Canvas(C.WIDTH, C.HEIGHT)
    terrain = Terrain(C.WIDTH, C.HEIGHT)

    build_sky(canvas)
    sky = canvas.snapshot()
    background = rebuild_background(canvas, terrain, sky)

    # UI Screens
    title_screen = TitleScreen()
    how_to_play_screen = HowToPlayScreen()
    lab_screen = LabScreen()
    hud_overlay = HUD()
    pause_overlay = PauseOverlay()

    tanks = [
        {"x": 118, "angle": 45.0, "color": C.P1, "hp": 100},
        {"x": 522, "angle": 135.0, "color": C.P2, "hp": 100},
    ]
    power = 55
    weapon = "SHELL"
    wind = 4
    state_mode = "TITLE"  # TITLE | HOW_TO_PLAY | LAB | MATCH | PAUSE

    # Headless screenshot generator
    if shot:
        if target_screen == "title":
            canvas.restore(sky)
            texts = title_screen.draw(canvas)
        elif target_screen == "help":
            canvas.restore(background)
            texts = how_to_play_screen.draw(canvas)
        elif target_screen == "lab":
            canvas.restore(background)
            texts = lab_screen.draw(canvas)
        else:  # hud / play
            draw_world(canvas, background, terrain, tanks)
            hud_data = {
                "turn": 0,
                "p1_hp": tanks[0]["hp"],
                "p2_hp": tanks[1]["hp"],
                "angle": tanks[0]["angle"],
                "power": power,
                "wind": wind,
                "weapon": weapon,
            }
            texts = hud_overlay.draw(canvas, hud_data)

        display.present(canvas, texts)
        os.makedirs(os.path.dirname(shot) or ".", exist_ok=True)
        display.save(shot)
        display.close()
        print("saved", shot)
        return 0

    print("Title Screen active: UP/DOWN navigate, ENTER select, ESC exit.")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    display.toggle_fullscreen()

                # Title Screen Controls
                elif state_mode == "TITLE":
                    if event.key == pygame.K_UP:
                        title_screen.prev_option()
                    elif event.key == pygame.K_DOWN:
                        title_screen.next_option()
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        chosen = title_screen.OPTIONS[title_screen.selected][0]
                        if chosen == "PLAY":
                            state_mode = "MATCH"
                        elif chosen == "HOW TO PLAY":
                            state_mode = "HOW_TO_PLAY"
                        elif chosen == "ALGORITHMS LAB":
                            state_mode = "LAB"
                        elif chosen == "QUIT":
                            running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                # How to Play Controls
                elif state_mode == "HOW_TO_PLAY":
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                        state_mode = "TITLE"

                # Algorithms Lab Controls
                elif state_mode == "LAB":
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                        state_mode = "TITLE"

                # Match Controls
                elif state_mode == "MATCH":
                    if event.key == pygame.K_ESCAPE:
                        state_mode = "PAUSE"
                    elif event.key == pygame.K_TAB:
                        weapon = "LASER" if weapon == "SHELL" else "SHELL"

                # Pause Controls
                elif state_mode == "PAUSE":
                    if event.key == pygame.K_UP:
                        pause_overlay.prev_option()
                    elif event.key == pygame.K_DOWN:
                        pause_overlay.next_option()
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        chosen = pause_overlay.OPTIONS[pause_overlay.selected]
                        if chosen == "RESUME MATCH":
                            state_mode = "MATCH"
                        elif chosen == "RESTART MATCH":
                            tanks[0]["hp"] = 100
                            tanks[1]["hp"] = 100
                            power = 55
                            state_mode = "MATCH"
                        elif chosen == "MAIN MENU":
                            state_mode = "TITLE"
                    elif event.key == pygame.K_ESCAPE:
                        state_mode = "MATCH"

        # Continuous keys (in MATCH)
        if state_mode == "MATCH":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                tanks[0]["angle"] = clamp(tanks[0]["angle"] + 2, 1, 179)
            if keys[pygame.K_RIGHT]:
                tanks[0]["angle"] = clamp(tanks[0]["angle"] - 2, 1, 179)
            if keys[pygame.K_UP]:
                power = int(clamp(power + 1, 10, 100))
            if keys[pygame.K_DOWN]:
                power = int(clamp(power - 1, 10, 100))

        # Render current state
        if state_mode == "TITLE":
            canvas.restore(sky)
            title_screen.update()
            texts = title_screen.draw(canvas)
            display.present(canvas, texts)

        elif state_mode == "HOW_TO_PLAY":
            canvas.restore(background)
            texts = how_to_play_screen.draw(canvas)
            display.present(canvas, texts)

        elif state_mode == "LAB":
            canvas.restore(background)
            texts = lab_screen.draw(canvas)
            display.present(canvas, texts)

        elif state_mode == "MATCH":
            draw_world(canvas, background, terrain, tanks)
            hud_data = {
                "turn": 0,
                "p1_hp": tanks[0]["hp"],
                "p2_hp": tanks[1]["hp"],
                "angle": tanks[0]["angle"],
                "power": power,
                "wind": wind,
                "weapon": weapon,
            }
            texts = hud_overlay.draw(canvas, hud_data)
            display.present(canvas, texts)

        elif state_mode == "PAUSE":
            draw_world(canvas, background, terrain, tanks)
            hud_data = {
                "turn": 0,
                "p1_hp": tanks[0]["hp"],
                "p2_hp": tanks[1]["hp"],
                "angle": tanks[0]["angle"],
                "power": power,
                "wind": wind,
                "weapon": weapon,
            }
            hud_texts = hud_overlay.draw(canvas, hud_data)
            pause_texts = pause_overlay.draw(canvas)
            display.present(canvas, hud_texts + pause_texts)

        clock.tick(C.FPS)

    display.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
