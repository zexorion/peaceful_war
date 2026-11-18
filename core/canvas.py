"""Canvas — the only layer allowed to write pixels.

A plain RGB byte array, 3 bytes per pixel, row major, origin at the top-left
corner, y growing downwards (the convention of Chapters 2-6 of the book).

This module deliberately has **no pygame import**: it must stay testable
without a window. `core/display.py` is the only file that talks to pygame.

Coordinates outside the canvas are ignored — that is our cheap point-clipping
(Chapter 6) and it means no algorithm ever has to bounds-check by itself.
"""


class Canvas:
    __slots__ = ("w", "h", "buf")

    def __init__(self, w, h, fill=(0, 0, 0)):
        self.w = w
        self.h = h
        self.buf = bytearray(bytes(fill) * (w * h))

    # --- single pixel -----------------------------------------------------
    def set_pixel(self, x, y, color):
        """Write one pixel, clipped to the canvas."""
        x = int(x)
        y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            buf = self.buf
            buf[i] = color[0]
            buf[i + 1] = color[1]
            buf[i + 2] = color[2]

    def blend_pixel(self, x, y, color, alpha):
        """Write one pixel mixed with what is already there.

        `alpha` is 0 (invisible) .. 255 (solid). Used for glow, stars and
        the moon halo.
        """
        x = int(x)
        y = int(y)
        if alpha <= 0 or not (0 <= x < self.w and 0 <= y < self.h):
            return
        if alpha >= 255:
            self.set_pixel(x, y, color)
            return
        i = (y * self.w + x) * 3
        buf = self.buf
        inv = 255 - alpha
        buf[i] = (color[0] * alpha + buf[i] * inv) // 255
        buf[i + 1] = (color[1] * alpha + buf[i + 1] * inv) // 255
        buf[i + 2] = (color[2] * alpha + buf[i + 2] * inv) // 255

    # --- spans ------------------------------------------------------------
    def hline(self, x0, x1, y, color):
        """Horizontal run. The workhorse of every scan-line fill."""
        if x1 < x0:
            x0, x1 = x1, x0
        x0 = int(x0)
        x1 = int(x1)
        y = int(y)
        if not (0 <= y < self.h):
            return
        if x0 < 0:
            x0 = 0
        if x1 >= self.w:
            x1 = self.w - 1
        buf = self.buf
        i = (y * self.w + x0) * 3
        for _ in range(x1 - x0 + 1):
            buf[i] = color[0]
            buf[i + 1] = color[1]
            buf[i + 2] = color[2]
            i += 3

    def vline(self, x, y0, y1, color):
        """Vertical run — how the terrain gets filled column by column."""
        if y1 < y0:
            y0, y1 = y1, y0
        x = int(x)
        y0 = int(y0)
        y1 = int(y1)
        if not (0 <= x < self.w):
            return
        if y0 < 0:
            y0 = 0
        if y1 >= self.h:
            y1 = self.h - 1
        buf = self.buf
        for y in range(y0, y1 + 1):
            i = (y * self.w + x) * 3
            buf[i] = color[0]
            buf[i + 1] = color[1]
            buf[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        """Filled rectangle made of horizontal spans. Not a line algorithm."""
        for yy in range(int(y), int(y) + int(h)):
            self.hline(x, int(x) + int(w) - 1, yy, color)

    # --- whole canvas -----------------------------------------------------
    def clear(self, color=(0, 0, 0)):
        self.buf[:] = bytes(color) * (self.w * self.h)

    def snapshot(self):
        """Copy the current pixels. Used to cache the static background."""
        return bytes(self.buf)

    def restore(self, snap):
        """Put a snapshot back, in one C-level copy (fast)."""
        self.buf[:] = snap
