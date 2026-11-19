"""HUD (Heads-Up Display) overlay for Peaceful War.

Draws player HP bars, active turn indicator, wind direction indicator,
aim angle, power meter, and selected weapon badge.
Uses Canvas primitives and emits display text tuples.
"""

import math
import config as C
from algo.lines import line_bresenham
from ui.theme import (
    FONT_SMALL,
    FONT_MED,
    TEXT_MAIN,
    TEXT_MUTED,
    TEXT_HIGHLIGHT,
    ACCENT_P1,
    ACCENT_P2,
    ACCENT_GOLD,
    HP_FULL,
    HP_MID,
    HP_LOW,
    HP_BG,
    BORDER_MUTED,
    BORDER_ACTIVE,
    draw_box,
    draw_horizontal_bar,
    draw_panel,
)


def get_hp_color(ratio):
    """Return green, yellow, or red depending on remaining HP percentage."""
    if ratio > 0.5:
        return HP_FULL
    if ratio > 0.25:
        return HP_MID
    return HP_LOW


class HUD:
    """Renders the game HUD during match play."""

    def __init__(self):
        pass

    def draw(self, cv, state_data):
        """Draw HUD elements onto canvas and return text tuples for display.

        state_data is a dict containing:
          - turn: 0 or 1
          - p1_hp: int (0..100)
          - p2_hp: int (0..100)
          - angle: float (0..180)
          - power: int (10..100)
          - wind: int (-10..10)
          - weapon: str ("SHELL" | "LASER")
        """
        texts = []
        turn = state_data.get("turn", 0)
        p1_hp = state_data.get("p1_hp", 100)
        p2_hp = state_data.get("p2_hp", 100)
        angle = state_data.get("angle", 45.0)
        power = state_data.get("power", 55)
        wind = state_data.get("wind", 0)
        weapon = state_data.get("weapon", "SHELL")

        # ---------------------------------------------------------------------
        # 1. Player 1 HP Panel (Top-Left)
        # ---------------------------------------------------------------------
        p1_bar_w = 110
        p1_bar_h = 10
        p1_x = 16
        p1_y = 12

        # Highlight active turn
        p1_border = ACCENT_P1 if turn == 0 else BORDER_MUTED
        draw_panel(cv, p1_x - 4, p1_y - 3, p1_bar_w + 38, p1_bar_h + 16, bg_color=(18, 12, 28), border_color=p1_border, alpha=180)

        # Name and HP text
        p1_label = "P1 [ACTIVE]" if turn == 0 else "P1"
        p1_text_color = ACCENT_P1 if turn == 0 else TEXT_MUTED
        texts.append((p1_label, p1_x, p1_y, p1_text_color, FONT_SMALL, "topleft"))
        texts.append(("%d HP" % p1_hp, p1_x + p1_bar_w + 28, p1_y + 11, TEXT_MAIN, FONT_SMALL, "topright"))

        # Health bar
        p1_ratio = p1_hp / 100.0
        draw_horizontal_bar(cv, p1_x, p1_y + 12, p1_bar_w, p1_bar_h, p1_ratio, get_hp_color(p1_ratio))

        # ---------------------------------------------------------------------
        # 2. Player 2 HP Panel (Top-Right)
        # ---------------------------------------------------------------------
        p2_bar_w = 110
        p2_bar_h = 10
        p2_x = cv.w - 16 - p2_bar_w
        p2_y = 12

        p2_border = ACCENT_P2 if turn == 1 else BORDER_MUTED
        draw_panel(cv, p2_x - 34, p2_y - 3, p2_bar_w + 38, p2_bar_h + 16, bg_color=(18, 12, 28), border_color=p2_border, alpha=180)

        p2_label = "P2 [ACTIVE]" if turn == 1 else "P2"
        p2_text_color = ACCENT_P2 if turn == 1 else TEXT_MUTED
        texts.append((p2_label, cv.w - 16, p2_y, p2_text_color, FONT_SMALL, "topright"))
        texts.append(("%d HP" % p2_hp, p2_x - 28, p2_y + 11, TEXT_MAIN, FONT_SMALL, "topleft"))

        # Health bar
        p2_ratio = p2_hp / 100.0
        draw_horizontal_bar(cv, p2_x, p2_y + 12, p2_bar_w, p2_bar_h, p2_ratio, get_hp_color(p2_ratio))

        # ---------------------------------------------------------------------
        # 3. Wind Indicator (Top-Center)
        # ---------------------------------------------------------------------
        center_x = cv.w // 2
        wind_card_w = 100
        wind_card_h = 24
        wind_x = center_x - wind_card_w // 2
        wind_y = 10
        draw_panel(cv, wind_x, wind_y, wind_card_w, wind_card_h, bg_color=(20, 14, 32), border_color=BORDER_MUTED, alpha=190)

        # Wind arrow drawn with line_bresenham
        arrow_cy = wind_y + 16
        if wind != 0:
            arrow_len = min(28, int(abs(wind) * 2.8))
            if wind > 0:  # blowing right
                ax0 = center_x - arrow_len // 2
                ax1 = center_x + arrow_len // 2
                line_bresenham(cv, ax0, arrow_cy, ax1, arrow_cy, ACCENT_GOLD)
                line_bresenham(cv, ax1 - 4, arrow_cy - 3, ax1, arrow_cy, ACCENT_GOLD)
                line_bresenham(cv, ax1 - 4, arrow_cy + 3, ax1, arrow_cy, ACCENT_GOLD)
            else:  # blowing left
                ax0 = center_x + arrow_len // 2
                ax1 = center_x - arrow_len // 2
                line_bresenham(cv, ax0, arrow_cy, ax1, arrow_cy, ACCENT_GOLD)
                line_bresenham(cv, ax1 + 4, arrow_cy - 3, ax1, arrow_cy, ACCENT_GOLD)
                line_bresenham(cv, ax1 + 4, arrow_cy + 3, ax1, arrow_cy, ACCENT_GOLD)

            wind_desc = "WIND %s%d" % ("+" if wind > 0 else "", wind)
        else:
            wind_desc = "WIND CALM"
            cv.set_pixel(center_x, arrow_cy, ACCENT_GOLD)

        texts.append((wind_desc, center_x, wind_y + 3, TEXT_MAIN, FONT_SMALL, "midtop"))

        # ---------------------------------------------------------------------
        # 4. Aim & Controls Bar (Bottom)
        # ---------------------------------------------------------------------
        bot_y = cv.h - 26

        # Angle (Bottom-Left)
        draw_panel(cv, 16, bot_y - 2, 85, 20, bg_color=(20, 14, 32), border_color=BORDER_MUTED, alpha=190)
        texts.append(("ANG: %d°" % int(angle), 22, bot_y + 2, TEXT_HIGHLIGHT, FONT_SMALL, "topleft"))

        # Power Meter (Bottom-Center)
        power_box_w = 140
        power_box_h = 20
        power_x = center_x - power_box_w // 2
        draw_panel(cv, power_x, bot_y - 2, power_box_w, power_box_h, bg_color=(20, 14, 32), border_color=BORDER_MUTED, alpha=190)
        power_ratio = (power - 10) / 90.0
        draw_horizontal_bar(cv, power_x + 6, bot_y + 11, power_box_w - 12, 6, power_ratio, ACCENT_GOLD, bg_color=(40, 28, 44))
        texts.append(("POW: %d%%" % int(power), center_x, bot_y + 1, TEXT_MAIN, FONT_SMALL, "midtop"))

        # Weapon Selection (Bottom-Right)
        draw_panel(cv, cv.w - 106, bot_y - 2, 90, 20, bg_color=(20, 14, 32), border_color=BORDER_MUTED, alpha=190)
        texts.append(("WEAPON: %s" % weapon, cv.w - 100, bot_y + 2, ACCENT_P1 if weapon == "SHELL" else ACCENT_P2, FONT_SMALL, "topleft"))

        return texts
