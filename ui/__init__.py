"""UI module for Peaceful War (Task 4).

Provides design tokens, screens (Title, HowToPlay, Lab, GameOver),
HUD overlays, and pause menus.
"""

from ui.theme import (
    FONT_SMALL,
    FONT_MED,
    FONT_LARGE,
    FONT_TITLE,
    GRID,
    TEXT_MAIN,
    TEXT_MUTED,
    TEXT_HIGHLIGHT,
    ACCENT_P1,
    ACCENT_P2,
    ACCENT_GOLD,
    HP_FULL,
    HP_MID,
    HP_LOW,
    draw_box,
    draw_panel,
    draw_horizontal_bar,
)
from ui.title import TitleScreen
from ui.how_to_play import HowToPlayScreen
from ui.hud import HUD
from ui.pause import PauseOverlay
from ui.game_over import GameOverScreen
from ui.lab import LabScreen
from ui.art import (
    draw_scenic_sunset_sky,
    generate_scenic_valley_heights,
    render_scenic_valley_terrain,
    draw_scenic_tank,
)

__all__ = [
    "FONT_SMALL",
    "FONT_MED",
    "FONT_LARGE",
    "FONT_TITLE",
    "GRID",
    "TEXT_MAIN",
    "TEXT_MUTED",
    "TEXT_HIGHLIGHT",
    "ACCENT_P1",
    "ACCENT_P2",
    "ACCENT_GOLD",
    "HP_FULL",
    "HP_MID",
    "HP_LOW",
    "draw_box",
    "draw_panel",
    "draw_horizontal_bar",
    "TitleScreen",
    "HowToPlayScreen",
    "HUD",
    "PauseOverlay",
    "GameOverScreen",
    "LabScreen",
    "draw_scenic_sunset_sky",
    "generate_scenic_valley_heights",
    "render_scenic_valley_terrain",
    "draw_scenic_tank",
]
