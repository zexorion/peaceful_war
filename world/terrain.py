"""Terrain — a heightmap: heights[x] is the surface y for column x.

Task 2 owns this file. Two things in it are placeholders for Slice 0:
  * `_placeholder_heights` must become a cubic Hermite / Cardinal spline
    through control points (Chapter 4),
  * `render` must become the scan-line polygon fill (Chapter 5), and
    `carve` (which does not exist yet) is the crater + live refill.

Everything else here is the real API the rest of the game codes against:
`height_at`, `is_solid`, `w`, `h`.
"""

import math
import random

from config import TERRAIN_DEEP, TERRAIN_EDGE, TERRAIN_NEAR
from core.util import clamp, lerp_color


class Terrain:
    def __init__(self, width, height, seed=7):
        self.w = width
        self.h = height
        self.seed = seed
        self.heights = _placeholder_heights(width, height, seed)
        self._palette = [
            lerp_color(TERRAIN_NEAR, TERRAIN_DEEP, i / 31.0) for i in range(32)
        ]

    # --- queries ----------------------------------------------------------
    def height_at(self, x):
        """Surface y of the column containing x (clamped at the edges)."""
        return self.heights[int(clamp(x, 0, self.w - 1))]

    def is_solid(self, x, y):
        """True if the point is inside the ground — the only collision test."""
        return y >= self.height_at(x)

    # --- drawing ----------------------------------------------------------
    def render(self, cv):
        """Paint the whole terrain once, into the cached background layer."""
        bottom = self.h
        palette = self._palette
        for x in range(self.w):
            top = self.heights[x]
            cv.set_pixel(x, top, TERRAIN_EDGE)
            span = bottom - top
            if span <= 0:
                continue
            for y in range(top + 1, bottom):
                idx = ((y - top) * 31) // span
                cv.set_pixel(x, y, palette[idx])


def _placeholder_heights(width, height, seed):
    """Three summed sine ridges — looks like hills, costs nothing.

    Task 2: delete this. Control points + Hermite give the real look and let
    the doctor see Chapter 4 doing the work.
    """
    rng = random.Random(seed)
    base = height * 0.60
    a1, f1, p1 = rng.uniform(26, 40), rng.uniform(1.0, 1.5), rng.uniform(0, 6.283)
    a2, f2, p2 = rng.uniform(10, 18), rng.uniform(2.4, 3.4), rng.uniform(0, 6.283)
    a3, f3, p3 = rng.uniform(3, 8), rng.uniform(5.0, 7.0), rng.uniform(0, 6.283)

    heights = []
    for x in range(width):
        u = (x / width) * 2.0 * math.pi
        y = base - (
            a1 * math.sin(f1 * u + p1)
            + a2 * math.sin(f2 * u + p2)
            + a3 * math.sin(f3 * u + p3)
        )
        heights.append(int(clamp(y, height * 0.30, height - 34)))
    return heights
