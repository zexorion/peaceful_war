"""Display — the only file that talks to pygame's window.

It does three things and nothing else:
  1. owns the window (windowed or fullscreen, scaled with letterboxing),
  2. shows a Canvas on it (nearest-neighbour upscale, crisp pixels),
  3. draws text at display resolution, because we agreed a ready-made font
     is acceptable for UI text only.

Everything else on screen is still our own pixels from `core/canvas.py`.
"""

import pygame


class Display:
    def __init__(self, title, width, height, scale=2):
        pygame.init()
        pygame.display.set_caption(title)
        self.w = width
        self.h = height
        self.window_scale = scale
        self.fullscreen = False
        self.scale = 1.0
        self.dest = pygame.Rect(0, 0, width, height)
        self.screen = None
        self._scaled = None
        self._fonts = {}
        self._apply_mode()

    # --- window -----------------------------------------------------------
    def _apply_mode(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                (self.w * self.window_scale, self.h * self.window_scale)
            )

        sw, sh = self.screen.get_size()
        fit = min(sw / self.w, sh / self.h)
        s = int(fit) if fit >= 1 else fit
        if s <= 0:
            s = 1
        self.scale = s
        dw = int(self.w * s)
        dh = int(self.h * s)
        self.dest = pygame.Rect((sw - dw) // 2, (sh - dh) // 2, dw, dh)
        self._scaled = None
        self._fonts.clear()
        self.screen.fill((0, 0, 0))

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self._apply_mode()

    # --- frame ------------------------------------------------------------
    def present(self, canvas, texts=()):
        """Show the canvas, then the HUD text on top."""
        frame = pygame.image.frombuffer(canvas.buf, (canvas.w, canvas.h), "RGB")
        if self.dest.size == (canvas.w, canvas.h):
            self.screen.blit(frame, self.dest.topleft)
        else:
            if self._scaled is None or self._scaled.get_size() != self.dest.size:
                self._scaled = pygame.Surface(self.dest.size).convert(frame)
            pygame.transform.scale(frame, self.dest.size, self._scaled)
            self.screen.blit(self._scaled, self.dest.topleft)

        for item in texts:
            self._draw_text(*item)
        pygame.display.flip()

    def _font(self, px):
        font = self._fonts.get(px)
        if font is None:
            font = pygame.font.SysFont("dejavusansmono,monospace", px)
            self._fonts[px] = font
        return font

    def _draw_text(self, text, x, y, color, size=10, anchor="topleft"):
        px = max(8, int(size * self.scale))
        surf = self._font(px).render(str(text), True, color)
        px_x = self.dest.x + int(x * self.scale)
        px_y = self.dest.y + int(y * self.scale)
        rect = surf.get_rect(**{anchor: (px_x, px_y)})
        self.screen.blit(surf, rect)

    def save(self, path):
        pygame.image.save(self.screen, path)

    def close(self):
        pygame.quit()
