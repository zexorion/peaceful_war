"""Chapter 5 & 6 — polygon rasterization, gradient fills, and clipping.

Provides filling and clipping algorithms:
  fill_polygon(cv, points, color)                             # General scan-line polygon fill
  vertical_gradient(cv, y0, y1, c0, c1)                       # 1D Gouraud-style vertical gradient
  flood_fill(cv, x, y, color)                                 # 4-way iterative stack flood fill
  clip_line_cohen_sutherland(x0, y0, x1, y1, xmin, ymin, ...) # Cohen-Sutherland line clipping
"""

from collections import deque


def fill_polygon(cv, points, color):
    """General scan-line polygon fill algorithm using even-odd parity (Ch5).

    Computes edge intersections per scan-line, sorts them, and draws horizontal spans.
    """
    n = len(points)
    if n < 3:
        return

    # Extract polygon edges, ignoring horizontal ones
    edges = []
    min_y = cv.h
    max_y = -1

    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        x1, y1 = float(p1[0]), float(p1[1])
        x2, y2 = float(p2[0]), float(p2[1])

        if y1 == y2:
            continue

        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        iy1 = int(round(y1))
        iy2 = int(round(y2))
        min_y = min(min_y, iy1)
        max_y = max(max_y, iy2)
        edges.append((x1, y1, x2, y2, (x2 - x1) / (y2 - y1)))

    min_y = max(0, min_y)
    max_y = min(cv.h - 1, max_y)

    hline = cv.hline
    for y in range(min_y, max_y + 1):
        intersections = []
        fy = float(y)
        for x1, y1, x2, y2, inv_m in edges:
            # Half-open scanline interval [y1, y2) to avoid vertex double counting
            if y1 <= fy < y2 or (fy == max_y and y1 <= fy <= y2):
                x_int = x1 + (fy - y1) * inv_m
                intersections.append(x_int)

        intersections.sort()
        for k in range(0, len(intersections) - 1, 2):
            x_start = round(intersections[k])
            x_end = round(intersections[k + 1])
            hline(x_start, x_end, y, color)


def vertical_gradient(cv, y0, y1, c0, c1):
    """Vertical Gouraud-style gradient across the full canvas width (Ch5).

    Interpolates colors per row and writes each span with hline.
    """
    y0, y1 = int(y0), int(y1)
    if y1 < y0:
        y0, y1 = y1, y0
        c0, c1 = c1, c0

    y0 = max(0, y0)
    y1 = min(cv.h - 1, y1)
    if y0 > y1:
        return

    span = max(1, y1 - y0)
    hline = cv.hline
    w_end = cv.w - 1

    r0, g0, b0 = c0
    dr = c1[0] - r0
    dg = c1[1] - g0
    db = c1[2] - b0

    for y in range(y0, y1 + 1):
        t = (y - y0) / span
        cr = int(round(r0 + dr * t))
        cg = int(round(g0 + dg * t))
        cb = int(round(b0 + db * t))
        hline(0, w_end, y, (cr, cg, cb))


def flood_fill(cv, x, y, color):
    """Iterative 4-way flood fill algorithm using an explicit stack (Ch5).

    Replaces connected pixels of the target color without recursion overflow.
    """
    x, y = int(x), int(y)
    if not (0 <= x < cv.w and 0 <= y < cv.h):
        return

    buf = cv.buf
    w = cv.w
    idx = (y * w + x) * 3
    target_color = (buf[idx], buf[idx + 1], buf[idx + 2])

    if target_color == color:
        return

    set_pixel = cv.set_pixel
    stack = [(x, y)]
    visited = set()

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))

        if not (0 <= cx < cv.w and 0 <= cy < cv.h):
            continue

        c_idx = (cy * w + cx) * 3
        if (buf[c_idx], buf[c_idx + 1], buf[c_idx + 2]) != target_color:
            continue

        set_pixel(cx, cy, color)
        stack.append((cx + 1, cy))
        stack.append((cx - 1, cy))
        stack.append((cx, cy + 1))
        stack.append((cx, cy - 1))


# --- Cohen-Sutherland Line Clipping (Ch6) ---------------------------------
_INSIDE = 0  # 0000
_LEFT = 1    # 0001
_RIGHT = 2   # 0010
_BOTTOM = 4  # 0100
_TOP = 8     # 1000


def _compute_code(x, y, xmin, ymin, xmax, ymax):
    code = _INSIDE
    if x < xmin:
        code |= _LEFT
    elif x > xmax:
        code |= _RIGHT
    if y < ymin:
        code |= _BOTTOM
    elif y > ymax:
        code |= _TOP
    return code


def clip_line_cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    """Cohen-Sutherland line clipping algorithm against a rectangle window (Ch6).

    Returns (x0, y0, x1, y1) clipped coordinates, or None if completely outside.
    """
    x0, y0 = float(x0), float(y0)
    x1, y1 = float(x1), float(y1)
    code0 = _compute_code(x0, y0, xmin, ymin, xmax, ymax)
    code1 = _compute_code(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        # Both endpoints inside clipping window
        if code0 == 0 and code1 == 0:
            return round(x0), round(y0), round(x1), round(y1)

        # Both endpoints in the same outside region (trivial reject)
        if (code0 & code1) != 0:
            return None

        # Line needs clipping: pick an outside point
        code_out = code0 if code0 != 0 else code1

        if code_out & _TOP:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
            y = ymax
        elif code_out & _BOTTOM:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
            y = ymin
        elif code_out & _RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            x = xmax
        elif code_out & _LEFT:
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            x = xmin

        # Replace outside endpoint with intersection
        if code_out == code0:
            x0, y0 = x, y
            code0 = _compute_code(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            code1 = _compute_code(x1, y1, xmin, ymin, xmax, ymax)
