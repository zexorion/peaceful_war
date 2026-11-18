"""Small shared helpers. No drawing in here, only maths.

Owned by Task 1. Everyone may import from it.
"""

import math


def clamp(value, low, high):
    """Keep `value` inside [low, high]."""
    if value < low:
        return low
    if value > high:
        return high
    return value


def lerp(a, b, t):
    """Linear interpolation: t=0 gives a, t=1 gives b."""
    return a + (b - a) * t


def lerp_color(c0, c1, t):
    """Mix two RGB colors. t is clamped to 0..1."""
    t = clamp(t, 0.0, 1.0)
    return (
        int(lerp(c0[0], c1[0], t)),
        int(lerp(c0[1], c1[1], t)),
        int(lerp(c0[2], c1[2], t)),
    )


def rotate(x, y, degrees):
    """Rotate a point around the origin. Screen coords: y grows down.

    Positive degrees turn counter-clockwise on screen, which is what an
    aiming barrel wants when the angle goes up.
    """
    rad = math.radians(degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    return (x * c - y * s, x * s + y * c)


def rotate_about(x, y, ox, oy, degrees):
    """Rotate a point around a pivot (ox, oy)."""
    rx, ry = rotate(x - ox, y - oy, degrees)
    return (ox + rx, oy + ry)
