"""How to Play screen explaining gameplay controls and mechanics.

Uses pure Canvas primitives to illustrate controls and tanks.
"""

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
    SURFACE_DARK,
    BORDER_MUTED,
    draw_box,
    draw_panel,
    draw_horizontal_bar,
)


class HowToPlayScreen:
    """Explains game mechanics, controls, and turns."""

    def __init__(self):
        pass

    def draw(self, cv):
        texts = []
        center_x = cv.w // 2

        # Header card
        draw_panel(cv, 80, 20, cv.w - 160, 42, bg_color=SURFACE_DARK, border_color=ACCENT_GOLD, alpha=220)
        texts.append(("HOW TO PLAY", center_x, 26, TEXT_MAIN, FONT_TITLE, "midtop"))
        texts.append(("MASTER THE ARTILLERY AND DESTROY ENEMY TERRAIN", center_x, 48, ACCENT_P1, FONT_SMALL, "midtop"))

        # Main instructions box
        box_w = 480
        box_h = 220
        box_x = center_x - box_w // 2
        box_y = 74
        draw_panel(cv, box_x, box_y, box_w, box_h, bg_color=SURFACE_CARD, border_color=BORDER_MUTED, alpha=225)

        # Controls list
        controls = [
            ("LEFT / RIGHT ARROWS", "Adjust Aim Angle (0 to 180 degrees)"),
            ("UP / DOWN ARROWS", "Adjust Launch Power (10 to 100%)"),
            ("SPACEBAR", "Fire Active Weapon"),
            ("TAB", "Switch Weapon: Shell (Explosive) <-> Laser (Beam)"),
            ("F11", "Toggle Fullscreen (Pixel-Perfect Scaling)"),
            ("ESC", "Pause Game / Return to Menu"),
        ]

        row_y = box_y + 16
        for key_name, action in controls:
            # Key tag box
            tag_w = 140
            tag_h = 22
            draw_box(cv, box_x + 20, row_y, tag_w, tag_h, fill=(36, 26, 52), border=ACCENT_GOLD)
            texts.append((key_name, box_x + 20 + tag_w // 2, row_y + 5, TEXT_HIGHLIGHT, FONT_SMALL, "midtop"))
            texts.append((action, box_x + 175, row_y + 5, TEXT_MAIN, FONT_SMALL, "topleft"))
            row_y += 30

        # Mini gameplay rules note inside box bottom
        cv.hline(box_x + 16, box_x + box_w - 16, box_y + box_h - 38, BORDER_MUTED)
        texts.append(
            ("Turn-based: Each hit creates craters in the terrain. Drop enemy HP to 0 to win!",
             center_x, box_y + box_h - 26, ACCENT_P2, FONT_SMALL, "midtop")
        )

        # Footer
        texts.append(("Press ESC or ENTER to return to Menu", center_x, cv.h - 26, TEXT_MUTED, FONT_SMALL, "midtop"))

        return texts
