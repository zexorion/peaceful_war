"""Title screen for Peaceful War.

Displays the main game title, animated menu choices, and version banner.
Uses pure Canvas primitive operations (Bresenham lines, rectangles, blend_pixel)
and emits text tuples for the display layer.
"""

import math
import config as C
from algo.lines import line_bresenham
from ui.theme import (
    FONT_TITLE,
    FONT_MED,
    FONT_SMALL,
    TEXT_MAIN,
    TEXT_MUTED,
    TEXT_HIGHLIGHT,
    ACCENT_P1,
    ACCENT_P2,
    ACCENT_GOLD,
    SURFACE_CARD,
    BORDER_MUTED,
    BORDER_ACTIVE,
    draw_box,
    draw_panel,
)


class TitleScreen:
    """Main menu and title screen."""

    OPTIONS = [
        ("PLAY", "Start 2-Player Match"),
        ("HOW TO PLAY", "Controls & Mechanics"),
        ("ALGORITHMS LAB", "Ch2-Ch5 Benchmark & Visualizer"),
        ("QUIT", "Exit Game"),
    ]

    def __init__(self):
        self.selected = 0
        self.tick = 0

    def next_option(self):
        self.selected = (self.selected + 1) % len(self.OPTIONS)

    def prev_option(self):
        self.selected = (self.selected - 1) % len(self.OPTIONS)

    def update(self, dt=1.0):
        self.tick += 1

    def draw(self, cv):
        """Render title screen graphics onto cv and return text tuples for Display."""
        texts = []
        center_x = cv.w // 2

        # 1. Subtle decorative grid / border around screen
        cv.hline(16, cv.w - 17, 16, BORDER_MUTED)
        cv.hline(16, cv.w - 17, cv.h - 17, BORDER_MUTED)
        cv.vline(16, 16, cv.h - 17, BORDER_MUTED)
        cv.vline(cv.w - 17, 16, cv.h - 17, BORDER_MUTED)

        # 2. Title Card / Logo Frame
        card_w = 420
        card_h = 60
        card_x = center_x - card_w // 2
        card_y = 36
        draw_panel(cv, card_x, card_y, card_w, card_h, bg_color=(18, 12, 32), border_color=ACCENT_GOLD, alpha=210)

        # Decorative corner accents on Title frame
        corner_len = 8
        # Top-left
        cv.hline(card_x - 2, card_x + corner_len, card_y - 2, ACCENT_P1)
        cv.vline(card_x - 2, card_y - 2, card_y + corner_len, ACCENT_P1)
        # Top-right
        cv.hline(card_x + card_w - corner_len, card_x + card_w + 1, card_y - 2, ACCENT_P2)
        cv.vline(card_x + card_w + 1, card_y - 2, card_y + corner_len, ACCENT_P2)
        # Bottom-left
        cv.hline(card_x - 2, card_x + corner_len, card_y + card_h + 1, ACCENT_P1)
        cv.vline(card_x - 2, card_y + card_h - corner_len, card_y + card_h + 1, ACCENT_P1)
        # Bottom-right
        cv.hline(card_x + card_w - corner_len, card_x + card_w + 1, card_y + card_h + 1, ACCENT_P2)
        cv.vline(card_x + card_w + 1, card_y + card_h - corner_len, card_y + card_h + 1, ACCENT_P2)

        # Title text
        texts.append(("PEACEFUL WAR", center_x, card_y + 12, TEXT_MAIN, FONT_TITLE, "midtop"))
        texts.append(("TURNS  *  ARTILLERY  *  DESTRUCTIBLE TERRAIN", center_x, card_y + 42, ACCENT_P1, FONT_SMALL, "midtop"))

        # 3. Menu Options List
        menu_y_start = 130
        item_h = 32
        item_w = 280
        item_x = center_x - item_w // 2

        pulse = int(math.sin(self.tick * 0.1) * 25)

        for i, (label, desc) in enumerate(self.OPTIONS):
            iy = menu_y_start + i * (item_h + 8)
            is_active = (i == self.selected)

            if is_active:
                # Highlight active option panel
                border_col = (min(255, BORDER_ACTIVE[0] + pulse),
                              min(255, BORDER_ACTIVE[1] + pulse),
                              min(255, BORDER_ACTIVE[2] + pulse))
                draw_panel(cv, item_x, iy, item_w, item_h, bg_color=SURFACE_CARD, border_color=border_col, alpha=230)

                # Cursor marker on left
                arrow_x = item_x + 12
                arrow_y = iy + item_h // 2
                line_bresenham(cv, arrow_x, arrow_y - 4, arrow_x + 6, arrow_y, ACCENT_GOLD)
                line_bresenham(cv, arrow_x, arrow_y + 4, arrow_x + 6, arrow_y, ACCENT_GOLD)

                # Text with highlight
                texts.append((label, item_x + 28, iy + 6, TEXT_HIGHLIGHT, FONT_MED, "topleft"))
                texts.append((desc, item_x + 28, iy + 19, TEXT_MUTED, FONT_SMALL, "topleft"))
            else:
                # Inactive button
                draw_box(cv, item_x, iy, item_w, item_h, fill=(20, 14, 30), border=BORDER_MUTED)
                texts.append((label, item_x + 28, iy + 9, TEXT_MAIN, FONT_MED, "topleft"))

        # 4. Footer controls reminder
        footer_y = cv.h - 32
        texts.append(("UP/DOWN: Navigate   ENTER/SPACE: Select   ESC: Back", center_x, footer_y, TEXT_MUTED, FONT_SMALL, "midtop"))
        texts.append(("IT311 Computer Graphics Project - 100% Software Renderer", center_x, footer_y + 12, (110, 95, 125), FONT_SMALL, "midtop"))

        return texts
