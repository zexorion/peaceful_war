"""Game Over / Match Results screen.

Displays winner banner, match statistics (turns, hits), and rematch prompt.
"""

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
    SURFACE_DARK,
    BORDER_MUTED,
    BORDER_ACTIVE,
    draw_box,
    draw_panel,
)


class GameOverScreen:
    """Displays victory outcome and match stats."""

    def __init__(self, winner=0, total_turns=12):
        self.winner = winner  # 0 for P1, 1 for P2
        self.total_turns = total_turns
        self.selected = 0
        self.options = ["PLAY AGAIN", "RETURN TO MENU"]

    def next_option(self):
        self.selected = (self.selected + 1) % len(self.options)

    def prev_option(self):
        self.selected = (self.selected - 1) % len(self.options)

    def draw(self, cv):
        texts = []
        center_x = cv.w // 2
        center_y = cv.h // 2

        # Dim background
        for y in range(0, cv.h, 2):
            for x in range(0, cv.w, 2):
                cv.blend_pixel(x, y, (10, 6, 16), 140)

        # Card
        card_w = 340
        card_h = 210
        card_x = center_x - card_w // 2
        card_y = center_y - card_h // 2

        winner_color = ACCENT_P1 if self.winner == 0 else ACCENT_P2
        winner_name = "PLAYER 1" if self.winner == 0 else "PLAYER 2"

        draw_panel(cv, card_x, card_y, card_w, card_h, bg_color=SURFACE_CARD, border_color=winner_color, alpha=235)

        # Banner
        texts.append(("VICTORY!", center_x, card_y + 16, ACCENT_GOLD, FONT_TITLE, "midtop"))
        texts.append(("%s DOMINATES THE BATTLEFIELD" % winner_name, center_x, card_y + 48, winner_color, FONT_MED, "midtop"))

        # Match Stats Box
        stats_y = card_y + 76
        draw_box(cv, card_x + 24, stats_y, card_w - 48, 42, fill=(20, 14, 30), border=BORDER_MUTED)
        texts.append(("TOTAL TURNS: %d" % self.total_turns, center_x, stats_y + 8, TEXT_MAIN, FONT_SMALL, "midtop"))
        texts.append(("HONORABLE COMBAT CONCLUDED", center_x, stats_y + 24, TEXT_MUTED, FONT_SMALL, "midtop"))

        # Rematch buttons
        btn_y = card_y + 130
        btn_w = 180
        btn_h = 24
        btn_x = center_x - btn_w // 2

        for i, opt in enumerate(self.options):
            iy = btn_y + i * (btn_h + 8)
            is_active = (i == self.selected)

            if is_active:
                draw_box(cv, btn_x, iy, btn_w, btn_h, fill=(50, 36, 68), border=BORDER_ACTIVE)
                texts.append((opt, center_x, iy + 5, TEXT_HIGHLIGHT, FONT_SMALL, "midtop"))
            else:
                draw_box(cv, btn_x, iy, btn_w, btn_h, fill=(24, 16, 36), border=BORDER_MUTED)
                texts.append((opt, center_x, iy + 5, TEXT_MUTED, FONT_SMALL, "midtop"))

        texts.append(("UP/DOWN: Navigate   ENTER: Select", center_x, card_y + card_h - 18, (140, 125, 150), FONT_SMALL, "midtop"))

        return texts
