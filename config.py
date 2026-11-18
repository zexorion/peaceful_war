"""Global constants.

One source of truth for every number that more than one module needs.
If you need a new shared constant, add it here — do not duplicate it elsewhere.
"""

# --- internal resolution (16:9) -------------------------------------------
# 640x360 scaled x3 = 1920x1080 exactly, so fullscreen is pixel-perfect on a
# 1080p screen. x2 = 1280x720 for windowed play.
WIDTH = 640
HEIGHT = 360
FPS = 60
WINDOW_SCALE = 2

# --- palette: night desert ------------------------------------------------
SKY_TOP = (22, 14, 44)
SKY_BOTTOM = (116, 40, 88)
STAR = (236, 222, 255)

MOON = (255, 205, 128)
MOON_RING = (226, 130, 78)

TERRAIN_EDGE = (236, 152, 80)   # rim light on the surface
TERRAIN_NEAR = (120, 56, 44)    # dirt just under the surface
TERRAIN_DEEP = (32, 16, 28)     # dirt at the bottom of the screen

P1 = (64, 224, 184)             # player one
P2 = (240, 118, 62)             # player two
TRACK = (30, 24, 32)

INK = (240, 238, 230)
DIM = (150, 132, 150)
AIM = (222, 214, 226)

# --- gameplay tuning ------------------------------------------------------
GRAVITY = 0.18                  # px per frame^2
WIND_ACC = 0.004                # px per frame^2 per wind unit
POWER_SPEED = 0.085             # launch speed per power unit
