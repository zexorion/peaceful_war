"""Theme tokens and UI styling primitives.

Chapter 6 point-clipping and primitive composition for UI panels.
Adheres to the 4px design grid and 640x360 internal resolution.
"""

import config as C
from algo.lines import line_bresenham

# --- Typography scale --------------------------------------------------------
FONT_SMALL = 10
FONT_MED = 14
FONT_LARGE = 18
FONT_TITLE = 26

# --- 4px Layout Grid ---------------------------------------------------------
GRID = 4
MARGIN_SM = 8
MARGIN_MD = 16
MARGIN_LG = 24

# --- UI Color Palette --------------------------------------------------------
# Text and ink
TEXT_MAIN = C.INK
TEXT_MUTED = C.DIM
TEXT_HIGHLIGHT = (255, 235, 140)

# Brand / Accent colors
ACCENT_P1 = C.P1          # Cyan (64, 224, 184)
ACCENT_P2 = C.P2          # Orange (240, 118, 62)
ACCENT_GOLD = (245, 195, 68)
ACCENT_CORAL = (235, 87, 87)

# Surface & Card backgrounds
SURFACE_DARK = (16, 10, 28)
SURFACE_CARD = (26, 18, 42)
SURFACE_LIGHT = (48, 32, 64)
BORDER_MUTED = (68, 52, 84)
BORDER_ACTIVE = (180, 160, 210)

# Health & Status indicators
HP_FULL = (64, 224, 130)
HP_MID = (240, 196, 60)
HP_LOW = (235, 75, 75)
HP_BG = (42, 24, 36)


def draw_box(cv, x, y, w, h, fill=None, border=None):
    """Draw a rectangle on Canvas with optional fill and border using Bresenham/lines."""
    x0 = int(x)
    y0 = int(y)
    x1 = int(x + w - 1)
    y1 = int(y + h - 1)

    if fill is not None and w > 0 and h > 0:
        cv.rect(x0, y0, w, h, fill)

    if border is not None and w > 0 and h > 0:
        cv.hline(x0, x1, y0, border)
        cv.hline(x0, x1, y1, border)
        cv.vline(x0, y0, y1, border)
        cv.vline(x1, y0, y1, border)


def draw_panel(cv, x, y, w, h, bg_color=SURFACE_DARK, border_color=BORDER_MUTED, alpha=200):
    """Draw a frosted/semi-transparent panel using Canvas blend_pixel."""
    x = int(x)
    y = int(y)
    w = int(w)
    h = int(h)

    # Fill with blend
    for py in range(y, y + h):
        for px in range(x, x + w):
            cv.blend_pixel(px, py, bg_color, alpha)

    # Border
    if border_color is not None:
        cv.hline(x, x + w - 1, y, border_color)
        cv.hline(x, x + w - 1, y + h - 1, border_color)
        cv.vline(x, y, y + h - 1, border_color)
        cv.vline(x + w - 1, y, y + h - 1, border_color)


def draw_horizontal_bar(cv, x, y, w, h, ratio, fill_color, bg_color=HP_BG, border_color=BORDER_MUTED):
    """Draw a progress / HP bar."""
    draw_box(cv, x, y, w, h, fill=bg_color, border=border_color)
    ratio = max(0.0, min(1.0, ratio))
    inner_w = int((w - 2) * ratio)
    if inner_w > 0 and h > 2:
        cv.rect(x + 1, y + 1, inner_w, h - 2, fill_color)
