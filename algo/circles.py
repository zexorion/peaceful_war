"""Chapter 3 — circles and ellipses.

Provides circle and ellipse rasterization algorithms:
  circle_midpoint(cv, cx, cy, r, color)            # outline, 8-way symmetry (Ch3)
  disc_midpoint(cv, cx, cy, r, color)              # filled disc for moon & crater (Ch3)
  ellipse_midpoint(cv, cx, cy, rx, ry, color)      # tank shadow, HUD (Ch3)
  circle_polar(cv, cx, cy, r, color)               # trigonometric polar comparison (Ch3)
  bench() / lab_report()                           # performance benchmark API
"""

import math
import time


def circle_midpoint(cv, cx, cy, r, color):
    """Midpoint circle algorithm using 8-way symmetry (Ch3).

    Plots the circle perimeter using integer-only decision arithmetic.
    """
    set_pixel = cv.set_pixel
    cx, cy, r = int(cx), int(cy), int(r)
    if r < 0:
        return
    if r == 0:
        set_pixel(cx, cy, color)
        return

    x = 0
    y = r
    d = 1 - r

    def _plot8(x, y):
        set_pixel(cx + x, cy + y, color)
        set_pixel(cx - x, cy + y, color)
        set_pixel(cx + x, cy - y, color)
        set_pixel(cx - x, cy - y, color)
        set_pixel(cx + y, cy + x, color)
        set_pixel(cx - y, cy + x, color)
        set_pixel(cx + y, cy - x, color)
        set_pixel(cx - y, cy - x, color)

    _plot8(x, y)
    while x < y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
        _plot8(x, y)


def disc_midpoint(cv, cx, cy, r, color):
    """Filled circle / disc algorithm using horizontal scan spans (Ch3).

    Fills the interior using cv.hline across symmetric octants.
    """
    hline = cv.hline
    cx, cy, r = int(cx), int(cy), int(r)
    if r < 0:
        return
    if r == 0:
        cv.set_pixel(cx, cy, color)
        return

    x = 0
    y = r
    d = 1 - r

    def _fill_spans(x, y):
        hline(cx - x, cx + x, cy + y, color)
        hline(cx - x, cx + x, cy - y, color)
        hline(cx - y, cx + y, cy + x, color)
        hline(cx - y, cx + y, cy - x, color)

    _fill_spans(x, y)
    while x < y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
        _fill_spans(x, y)


def ellipse_midpoint(cv, cx, cy, rx, ry, color):
    """Midpoint ellipse algorithm using 4-way symmetry (Ch3).

    Splits rasterization into Region 1 (slope > -1) and Region 2 (slope < -1).
    """
    set_pixel = cv.set_pixel
    cx, cy, rx, ry = int(cx), int(cy), int(rx), int(ry)
    if rx < 0 or ry < 0:
        return
    if rx == 0 and ry == 0:
        set_pixel(cx, cy, color)
        return
    if rx == 0:
        cv.vline(cx, cy - ry, cy + ry, color)
        return
    if ry == 0:
        cv.hline(cx - rx, cx + rx, cy, color)
        return

    def _plot4(x, y):
        set_pixel(cx + x, cy + y, color)
        set_pixel(cx - x, cy + y, color)
        set_pixel(cx + x, cy - y, color)
        set_pixel(cx - x, cy - y, color)

    rx2 = rx * rx
    ry2 = ry * ry
    two_rx2 = 2 * rx2
    two_ry2 = 2 * ry2

    # Region 1: start at (0, ry), step x
    x = 0
    y = ry
    px = 0
    py = two_rx2 * y
    p1 = ry2 - (rx2 * ry) + 0.25 * rx2

    _plot4(x, y)
    while px < py:
        x += 1
        px += two_ry2
        if p1 < 0:
            p1 += ry2 + px
        else:
            y -= 1
            py -= two_rx2
            p1 += ry2 + px - py
        _plot4(x, y)

    # Region 2: start from end of Region 1, step y
    p2 = ry2 * (x + 0.5) ** 2 + rx2 * (y - 1) ** 2 - rx2 * ry2
    while y > 0:
        y -= 1
        py -= two_rx2
        if p2 > 0:
            p2 += rx2 - py
        else:
            x += 1
            px += two_ry2
            p2 += rx2 - py + px
        _plot4(x, y)


def circle_polar(cv, cx, cy, r, color):
    """Polar circle algorithm using cos/sin trigonometry (Ch3).

    Steps angle theta by ~1/r radians. Used for Lab benchmarks.
    """
    set_pixel = cv.set_pixel
    cx, cy, r = int(cx), int(cy), int(r)
    if r < 0:
        return
    if r == 0:
        set_pixel(cx, cy, color)
        return

    step = 1.0 / r
    theta = 0.0
    two_pi = 2.0 * math.pi
    while theta <= two_pi + step:
        x = round(cx + r * math.cos(theta))
        y = round(cy + r * math.sin(theta))
        set_pixel(x, y, color)
        theta += step


# --- Benchmark & Lab API --------------------------------------------------
class _PixelCounter:
    """Mock canvas to count unique pixels plotted and verify algorithms."""
    def __init__(self):
        self.points = set()

    def set_pixel(self, x, y, color):
        self.points.add((int(x), int(y)))

    def hline(self, x0, x1, y, color):
        if x1 < x0:
            x0, x1 = x1, x0
        for x in range(int(x0), int(x1) + 1):
            self.points.add((x, int(y)))

    def vline(self, x, y0, y1, color):
        if y1 < y0:
            y0, y1 = y1, y0
        for y in range(int(y0), int(y1) + 1):
            self.points.add((int(x), y))


def bench(runs=100):
    """Benchmark all line and circle algorithms and return statistics."""
    from algo.lines import line_bresenham, line_dda, line_direct

    results = []
    # Test cases:
    # 1. 400px diagonal line: (0, 0) to (320, 240) -> length = 400px
    x0, y0, x1, y1 = 0, 0, 320, 240
    color = (255, 255, 255)

    line_algos = [
        ("Direct line", line_direct),
        ("DDA", line_dda),
        ("Bresenham", line_bresenham),
    ]

    for name, fn in line_algos:
        counter = _PixelCounter()
        fn(counter, x0, y0, x1, y1, color)
        pixels = len(counter.points)

        t0 = time.perf_counter()
        for _ in range(runs):
            fn(counter, x0, y0, x1, y1, color)
        t1 = time.perf_counter()
        ms = ((t1 - t0) / runs) * 1000.0
        results.append({"name": name, "pixels": pixels, "ms": round(ms, 4)})

    # 2. Circle radius = 40
    cx, cy, r = 100, 100, 40
    circle_algos = [
        ("Midpoint Circle", circle_midpoint),
        ("Polar Circle", circle_polar),
    ]

    for name, fn in circle_algos:
        counter = _PixelCounter()
        fn(counter, cx, cy, r, color)
        pixels = len(counter.points)

        t0 = time.perf_counter()
        for _ in range(runs):
            fn(counter, cx, cy, r, color)
        t1 = time.perf_counter()
        ms = ((t1 - t0) / runs) * 1000.0
        results.append({"name": name, "pixels": pixels, "ms": round(ms, 4)})

    return results


def lab_report():
    """Return benchmark data for Task 4 Algorithms Lab."""
    return bench(runs=100)
