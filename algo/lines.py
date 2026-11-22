"""Chapter 2 — line drawing.

Provides line rasterization algorithms:
  line_direct(cv, x0, y0, x1, y1, color)             # Direct equation y = mx + b
  line_dda(cv, x0, y0, x1, y1, color)                # DDA algorithm
  line_dda_dotted(cv, x0, y0, x1, y1, color, gap=4)  # Dotted aim guide
  line_bresenham(cv, x0, y0, x1, y1, color)          # Bresenham integer-only
"""


def line_direct(cv, x0, y0, x1, y1, color):
    """Direct line algorithm using y = m*x + b (Ch2).
    
    Samples along the major axis with round() to avoid gaps and div-by-zero.
    """
    set_pixel = cv.set_pixel
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

    dx = x1 - x0
    dy = y1 - y0

    # Case 0: Single point
    if dx == 0 and dy == 0:
        set_pixel(x0, y0, color)
        return

    # Case 1: Major axis is X (|dx| >= |dy|)
    if abs(dx) >= abs(dy):
        m = dy / dx
        b = y0 - m * x0
        step = 1 if x1 >= x0 else -1
        for x in range(x0, x1 + step, step):
            y = round(m * x + b)
            set_pixel(x, y, color)
    # Case 2: Major axis is Y (|dy| > |dx|)
    else:
        m_inv = dx / dy
        b = x0 - m_inv * y0
        step = 1 if y1 >= y0 else -1
        for y in range(y0, y1 + step, step):
            x = round(m_inv * y + b)
            set_pixel(x, y, color)


def line_dda(cv, x0, y0, x1, y1, color):
    """Digital Differential Analyzer (DDA) line algorithm (Ch2).

    Steps along the major axis by 1 and increments the minor axis by slope.
    """
    set_pixel = cv.set_pixel
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))
    if steps == 0:
        set_pixel(x0, y0, color)
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x = float(x0)
    y = float(y0)
    for _ in range(steps + 1):
        set_pixel(round(x), round(y), color)
        x += x_inc
        y += y_inc


def line_dda_dotted(cv, x0, y0, x1, y1, color, gap=4):
    """Dotted DDA line algorithm for aim guide preview (Ch2).

    Only plots a pixel every `gap` steps along the line trajectory.
    """
    set_pixel = cv.set_pixel
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))
    if steps == 0:
        set_pixel(x0, y0, color)
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x = float(x0)
    y = float(y0)
    for step in range(steps + 1):
        if step % gap == 0:
            set_pixel(round(x), round(y), color)
        x += x_inc
        y += y_inc




def line_bresenham(cv, x0, y0, x1, y1, color):
    """Bresenham / midpoint line, all octants (Ch2). Integer only."""
    set_pixel = cv.set_pixel
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
        set_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy

