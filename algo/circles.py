"""Chapter 3 — circles and ellipses.

FALLBACK ONLY. These are the Direct (Cartesian) versions from the book. Task 1
replaces them with the Midpoint (Bresenham) algorithm, adds the ellipse, and
keeps these as the slow reference for the Algorithms Lab.

Why a fallback at all: the rule is that no task is ever blocked. If Midpoint
is late, the game still draws circles.
"""

import math


def _plot8(cv, cx, cy, x, y, color):
    cv.set_pixel(cx + x, cy + y, color)
    cv.set_pixel(cx - x, cy + y, color)
    cv.set_pixel(cx + x, cy - y, color)
    cv.set_pixel(cx - x, cy - y, color)
    cv.set_pixel(cx + y, cy + x, color)
    cv.set_pixel(cx - y, cy + x, color)
    cv.set_pixel(cx + y, cy - x, color)
    cv.set_pixel(cx - y, cy - x, color)


def circle_direct(cv, cx, cy, r, color):
    """Outline circle by the Cartesian equation, 8-way symmetry."""
    r = int(r)
    if r < 1:
        cv.set_pixel(cx, cy, color)
        return
    r2 = r * r
    for x in range(r + 1):
        y = int(math.sqrt(max(0, r2 - x * x)) + 0.5)
        _plot8(cv, int(cx), int(cy), x, y, color)


def disc_spans(cv, cx, cy, r, color):
    """Filled disc using one horizontal span per row."""
    r = int(r)
    cx = int(cx)
    cy = int(cy)
    r2 = r * r
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(max(0, r2 - dy * dy)))
        cv.hline(cx - dx, cx + dx, cy + dy, color)


def disc_blend(cv, cx, cy, r, color, alpha):
    """Filled disc drawn with transparency — glow, halos, explosions fading."""
    r = int(r)
    cx = int(cx)
    cy = int(cy)
    r2 = r * r
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(max(0, r2 - dy * dy)))
        y = cy + dy
        for x in range(cx - dx, cx + dx + 1):
            cv.blend_pixel(x, y, color, alpha)
