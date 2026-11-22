"""Terrain — a heightmap: heights[x] is the surface y for column x (Ch4 & Ch5).

Task 2 owns this file:
  * Procedural terrain heightmap generated via cubic Hermite / Catmull-Rom spline (Ch4),
  * Dynamic crater destruction via carve() (Ch4),
  * Vertical span rendering with 32-level procedural color palette and surface rim light (Ch5).
"""

import math
import random

from algo.curves import hermite
from config import TERRAIN_DEEP, TERRAIN_EDGE, TERRAIN_NEAR
from core.util import clamp, lerp_color


def generate_spline_heights(width, height, seed=7):
    """Generate smooth continuous heightmap using Hermite spline through control points (Ch4).

    Controls terrain roughness and amplitude with deterministic random seed.
    """
    rng = random.Random(seed)
    num_points = 8

    # Generate evenly spaced control points across the width
    xs = [int(round(i * (width - 1) / (num_points - 1))) for i in range(num_points)]
    ys = [
        int(round(rng.uniform(height * 0.35, height * 0.70)))
        for _ in range(num_points)
    ]
    control_points = list(zip(xs, ys))

    # Calculate Catmull-Rom tangents at control points: T = 0.5 * (P[i+1] - P[i-1])
    tangents = []
    for i in range(num_points):
        if i == 0:
            tx = (control_points[1][0] - control_points[0][0]) * 0.8
            ty = (control_points[1][1] - control_points[0][1]) * 0.8
        elif i == num_points - 1:
            tx = (control_points[num_points - 1][0] - control_points[num_points - 2][0]) * 0.8
            ty = (control_points[num_points - 1][1] - control_points[num_points - 2][1]) * 0.8
        else:
            tx = (control_points[i + 1][0] - control_points[i - 1][0]) * 0.5
            ty = (control_points[i + 1][1] - control_points[i - 1][1]) * 0.5
        tangents.append((tx, ty))

    heights = [0] * width
    for i in range(num_points - 1):
        p0 = control_points[i]
        p1 = control_points[i + 1]
        t0 = tangents[i]
        t1 = tangents[i + 1]

        seg_width = p1[0] - p0[0]
        pts = hermite(p0, p1, t0, t1, steps=seg_width)

        for px, py in pts:
            if 0 <= px < width:
                clamped_y = int(clamp(py, height * 0.25, height - 34))
                heights[px] = clamped_y

    # Ensure every single column from 0 to width - 1 is filled
    for x in range(1, width):
        if heights[x] == 0:
            heights[x] = heights[x - 1]

    return heights


class Terrain:
    def __init__(self, width, height, seed=7):
        self.w = width
        self.h = height
        self.seed = seed
        self.heights = generate_spline_heights(width, height, seed)
        self._palette = [
            lerp_color(TERRAIN_NEAR, TERRAIN_DEEP, i / 31.0) for i in range(32)
        ]

    # --- queries ----------------------------------------------------------
    def height_at(self, x):
        """Surface y of the column containing x (clamped at the edges)."""
        idx = int(clamp(x, 0, self.w - 1))
        return self.heights[idx]

    def is_solid(self, x, y):
        """True if the point is inside the ground — the fundamental collision test."""
        return y >= self.height_at(x)

    # --- destruction ------------------------------------------------------
    def carve(self, cx, cy, r):
        """Carve a circular crater into the terrain (Ch4/Ch5).

        Lowers the surface height down to the bottom of the circle for affected columns.
        Clamped at height - 2 so no column disappears. Returns affected (x0, x1) range.
        """
        cx, cy, r = int(cx), int(cy), int(r)
        x0 = max(0, cx - r)
        x1 = min(self.w - 1, cx + r)
        r2 = r * r
        max_y = self.h - 2

        for x in range(x0, x1 + 1):
            dx = x - cx
            dy = int(math.isqrt(r2 - dx * dx))
            # If the circle intersects or overlaps above the ground surface
            if cy - dy <= self.heights[x]:
                crater_bottom = min(max_y, cy + dy)
                self.heights[x] = max(self.heights[x], crater_bottom)

        return x0, x1

    # --- drawing ----------------------------------------------------------
    def render(self, cv):
        """Paint the entire terrain into the cached background layer (Ch5).

        Draws the rim light along the surface and fills downward with 32-level palette.
        """
        bottom = self.h
        palette = self._palette
        set_pixel = cv.set_pixel
        rim_color = TERRAIN_EDGE

        for x in range(self.w):
            top = self.heights[x]
            set_pixel(x, top, rim_color)
            span = bottom - top
            if span <= 1:
                continue
            for y in range(top + 1, bottom):
                idx = ((y - top) * 31) // span
                set_pixel(x, y, palette[idx])
