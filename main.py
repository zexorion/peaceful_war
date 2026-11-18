"""Peaceful War — Slice 0 (boot scene).

This is a smoke test for the architecture, not the game yet:

    one window  ->  one Canvas  ->  our own pixels  ->  Display

It proves four things on day one:
  1. the Canvas is the only thing writing pixels,
  2. the static background (sky, stars, terrain) can be cached and
     restored in one copy, so per-frame cost stays tiny,
  3. 640x360 scales x2 windowed and x3 fullscreen with no blur,
  4. text is the single agreed exception (pygame.font, at display size).

There is no moon and no aim guide yet: those are circles and dotted lines,
and Task 1 writes every circle and every DDA line in this project. Slice 0
deliberately does not ship them.

Owner: Task 3 (game core + integration). Task 1 and Task 2 replace the
drawing calls inside it as their modules land.

Controls:  LEFT / RIGHT aim  ·  F11 fullscreen  ·  ESC quit
Run:       .venv/bin/python main.py
Screenshot: .venv/bin/python main.py --shot out/slice0.png
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
    """Rebuild the cached background after the terrain changed.

    Restoring the sky first matters: without it the old terrain would still be
    underneath and painting the new one on top would leave a ghost of the
    crater. Called once per explosion, never per frame (~45 ms).
    """
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


def hud(tanks, power):
    return [
        ("P1", 12, 10, C.DIM, 10, "topleft"),
        ("P2", C.WIDTH - 12, 10, C.DIM, 10, "topright"),
        ("WIND 9", C.WIDTH // 2, 10, C.INK, 10, "midtop"),
        (
            "ANG %d  POW %d" % (int(tanks[0]["angle"]), power),
            12,
            C.HEIGHT - 10,
            C.INK,
            10,
            "bottomleft",
        ),
        ("SHELL", C.WIDTH - 12, C.HEIGHT - 10, C.INK, 10, "bottomright"),
    ]


def main(argv):
    shot = None
    if "--shot" in argv:
        shot = argv[argv.index("--shot") + 1]

    display = Display("Peaceful War — Slice 0", C.WIDTH, C.HEIGHT, C.WINDOW_SCALE)
    canvas = Canvas(C.WIDTH, C.HEIGHT)
    terrain = Terrain(C.WIDTH, C.HEIGHT)

    build_sky(canvas)
    sky = canvas.snapshot()
    background = rebuild_background(canvas, terrain, sky)

    tanks = [
        {"x": 118, "angle": 45.0, "color": C.P1},
        {"x": 522, "angle": 135.0, "color": C.P2},
    ]
    power = 55

    if shot:
        draw_world(canvas, background, terrain, tanks)
        display.present(canvas, hud(tanks, power))
        os.makedirs(os.path.dirname(shot) or ".", exist_ok=True)
        display.save(shot)
        display.close()
        print("saved", shot)
        return 0

    print("LEFT/RIGHT aim · F11 fullscreen · ESC quit")
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F11:
                    display.toggle_fullscreen()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            tanks[0]["angle"] = clamp(tanks[0]["angle"] + 2, 1, 179)
        if keys[pygame.K_RIGHT]:
            tanks[0]["angle"] = clamp(tanks[0]["angle"] - 2, 1, 179)

        draw_world(canvas, background, terrain, tanks)
        display.present(canvas, hud(tanks, power))
        clock.tick(C.FPS)

    display.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
