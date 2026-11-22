"""Chapter 4 — parametric curves and splines.

Provides curve evaluation algorithms:
  hermite(p0, p1, t0, t1, steps) -> [(x, y), ...]        # Cubic Hermite spline
  bezier(p0, p1, p2, steps) -> [(x, y), ...]             # Quadratic Bezier curve
  cardinal(points, tension, steps) -> [(x, y), ...]      # Cardinal / Catmull-Rom spline
  curve_screen(cv, points, color)                        # Render curve using Bresenham
"""

from algo.lines import line_bresenham


def hermite(p0, p1, t0, t1, steps):
    """Cubic Hermite curve segment between two points with tangent vectors (Ch4).

    Interpolates using the four Hermite cubic basis functions.
    """
    steps = max(1, int(steps))
    x0, y0 = float(p0[0]), float(p0[1])
    x1, y1 = float(p1[0]), float(p1[1])
    dx0, dy0 = float(t0[0]), float(t0[1])
    dx1, dy1 = float(t1[0]), float(t1[1])

    points = []
    for i in range(steps + 1):
        t = i / steps
        t2 = t * t
        t3 = t2 * t

        h00 = 2.0 * t3 - 3.0 * t2 + 1.0
        h10 = t3 - 2.0 * t2 + t
        h01 = -2.0 * t3 + 3.0 * t2
        h11 = t3 - t2

        x = h00 * x0 + h10 * dx0 + h01 * x1 + h11 * dx1
        y = h00 * y0 + h10 * dy0 + h01 * y1 + h11 * dy1
        points.append((round(x), round(y)))

    return points


def bezier(p0, p1, p2, steps):
    """Quadratic Bezier curve defined by three control points (Ch4).

    Evaluates the Bernstein polynomial B(t) = (1-t)^2*P0 + 2(1-t)t*P1 + t^2*P2.
    """
    steps = max(1, int(steps))
    x0, y0 = float(p0[0]), float(p0[1])
    x1, y1 = float(p1[0]), float(p1[1])
    x2, y2 = float(p2[0]), float(p2[1])

    points = []
    for i in range(steps + 1):
        t = i / steps
        u = 1.0 - t
        u2 = u * u
        t2 = t * t

        x = u2 * x0 + 2.0 * u * t * x1 + t2 * x2
        y = u2 * y0 + 2.0 * u * t * y1 + t2 * y2
        points.append((round(x), round(y)))

    return points


def cardinal(points, tension=0.0, steps=20):
    """Cardinal spline interpolating a list of control points (Ch4).

    Computes tangents via Catmull-Rom finite differences with optional tension.
    """
    n = len(points)
    if n == 0:
        return []
    if n == 1:
        return [(round(points[0][0]), round(points[0][1]))]
    if n == 2:
        dx = float(points[1][0] - points[0][0])
        dy = float(points[1][1] - points[0][1])
        return hermite(points[0], points[1], (dx, dy), (dx, dy), steps)

    s = (1.0 - float(tension)) * 0.5
    tangents = []
    for i in range(n):
        if i == 0:
            # Forward difference for start endpoint
            tx = (points[1][0] - points[0][0]) * (1.0 - float(tension))
            ty = (points[1][1] - points[0][1]) * (1.0 - float(tension))
        elif i == n - 1:
            # Backward difference for end endpoint
            tx = (points[n - 1][0] - points[n - 2][0]) * (1.0 - float(tension))
            ty = (points[n - 1][1] - points[n - 2][1]) * (1.0 - float(tension))
        else:
            # Central difference (Catmull-Rom when tension=0)
            tx = (points[i + 1][0] - points[i - 1][0]) * s
            ty = (points[i + 1][1] - points[i - 1][1]) * s
        tangents.append((tx, ty))

    result = []
    for i in range(n - 1):
        seg = hermite(points[i], points[i + 1], tangents[i], tangents[i + 1], steps)
        if i > 0:
            result.extend(seg[1:])
        else:
            result.extend(seg)

    return result


def curve_screen(cv, points, color):
    """Render a sequence of discrete curve vertices using Bresenham lines (Ch4).

    Ties consecutive curve points on the canvas buffer.
    """
    if len(points) < 2:
        if len(points) == 1:
            cv.set_pixel(points[0][0], points[0][1], color)
        return

    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        line_bresenham(cv, x0, y0, x1, y1, color)
