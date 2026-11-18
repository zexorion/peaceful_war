"""Chapter 2 — line drawing.

Only Bresenham ships here, because the tanks need *some* line to be visible on
day one.

Task 1 owns this file and writes the rest — from the book, not from memory:
  line_direct(cv, x0, y0, x1, y1, color)             # naive y = mx + b
  line_dda(cv, x0, y0, x1, y1, color)                # DDA
  line_dda_dotted(cv, x0, y0, x1, y1, color, gap=4)  # dotted aim guide
plus their tests and their rows in the benchmark table.
"""


def line_bresenham(cv, x0, y0, x1, y1, color):
    """Bresenham / midpoint line, all octants (Ch2). Integer only."""
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)

    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    while True:
        cv.set_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
