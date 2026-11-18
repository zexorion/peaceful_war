"""Chapter 2 — line drawing.

The scaffold ships two of them because Slice 0 needs them:
  * line_bresenham  — every straight edge in the game,
  * line_dda_dotted — the dotted aiming guide.

Task 1 still owns this file: it adds the Direct method, the plain DDA, the
performance table for the Algorithms Lab, and the unit tests.
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


def line_dda_dotted(cv, x0, y0, x1, y1, color, gap=4):
    """DDA stepped on the major axis, plotting one pixel every `gap` steps (Ch2).

    Used for the aim guide and the trajectory preview.
    """
    dx = int(x1) - int(x0)
    dy = int(y1) - int(y0)
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        cv.set_pixel(x0, y0, color)
        return

    xinc = dx / steps
    yinc = dy / steps
    x = float(x0)
    y = float(y0)
    for i in range(steps + 1):
        if i % gap == 0:
            cv.set_pixel(round(x), round(y), color)
        x += xinc
        y += yinc
