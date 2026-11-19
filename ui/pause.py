"""Pause menu overlay for Peaceful War.

Darkens the game scene with alpha blending and shows resume/restart/quit options.
"""

from ui.theme import (
    FONT_TITLE,
    FONT_MED,
    FONT_SMALL,
    TEXT_MAIN,
    TEXT_MUTED,
    TEXT_HIGHLIGHT,
    ACCENT_GOLD,
    SURFACE_CARD,
    SURFACE_DARK,
    BORDER_MUTED,
    BORDER_ACTIVE,
    draw_box,
    draw_panel,
)


class PauseOverlay:
    OPTIONS = [
        "RESUME MATCH",
        "RESTART MATCH",
        "MAIN MENU",
    ]

    def __init__(self):
        self.selected = 0

    def next_option(self):
        self.selected = (self.selected + 1) % len(self.OPTIONS)

    def prev_option(self):
        self.selected = (self.selected - 1) % len(self.OPTIONS)

    def draw(self, cv):
        texts = []
        center_x = cv.w // 2
        center_y = cv.h // 2

        # 1. Darken entire background using Canvas blend_pixel
        for y in range(0, cv.h, 2):  # step 2 for speed
            for x in range(0, cv.w, 2):
                cv.blend_pixel(x, y, (0, 0, 0), 120)

        # 2. Pause Card Panel
        card_w = 260
        card_h = 170
        card_x = center_x - card_w // 2
        card_y = center_y - card_h // 2
        draw_panel(cv, card_x, card_y, card_w, card_h, bg_color=SURFACE_CARD, border_color=ACCENT_GOLD, alpha=235)

        texts.append(("MATCH PAUSED", center_x, card_y + 16, TEXT_MAIN, FONT_TITLE, "midtop"))

        # Options
        btn_y = card_y + 58
        btn_w = 200
        btn_h = 24
        btn_x = center_x - btn_w // 2

        for i, label in enumerate(self.OPTIONS):
            iy = btn_y + i * (btn_h + 8)
            is_active = (i == self.selected)

            if is_active:
                draw_box(cv, btn_x, iy, btn_w, btn_h, fill=(50, 36, 68), border=BORDER_ACTIVE)
                texts.append((label, center_x, iy + 5, TEXT_HIGHLIGHT, FONT_SMALL, "midtop"))
            else:
                draw_box(cv, btn_x, iy, btn_w, btn_h, fill=(24, 16, 36), border=BORDER_MUTED)
                texts.append((label, center_x, iy + 5, TEXT_MUTED, FONT_SMALL, "midtop"))

        texts.append(("UP/DOWN: Navigate   ENTER: Select", center_x, card_y + card_h - 20, (140, 125, 150), FONT_SMALL, "midtop"))

        return texts
