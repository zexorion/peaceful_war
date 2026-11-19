"""Unit tests for UI components, screens, and HUD (Task 4)."""

import unittest
from core.canvas import Canvas
from ui.theme import (
    draw_box,
    draw_panel,
    draw_horizontal_bar,
    HP_FULL,
    HP_MID,
    HP_LOW,
)
from ui.title import TitleScreen
from ui.how_to_play import HowToPlayScreen
from ui.hud import HUD, get_hp_color
from ui.pause import PauseOverlay
from ui.game_over import GameOverScreen
from ui.lab import LabScreen


class TestUITheme(unittest.TestCase):
    def setUp(self):
        self.cv = Canvas(100, 100)

    def test_draw_box(self):
        draw_box(self.cv, 10, 10, 20, 20, fill=(255, 0, 0), border=(0, 255, 0))
        # Interior pixel check
        idx_inner = (15 * 100 + 15) * 3
        self.assertEqual(tuple(self.cv.buf[idx_inner:idx_inner + 3]), (255, 0, 0))
        # Border pixel check
        idx_border = (10 * 100 + 10) * 3
        self.assertEqual(tuple(self.cv.buf[idx_border:idx_border + 3]), (0, 255, 0))

    def test_draw_panel(self):
        draw_panel(self.cv, 5, 5, 30, 30, bg_color=(100, 100, 100), border_color=(200, 200, 200), alpha=150)
        idx_border = (5 * 100 + 5) * 3
        self.assertEqual(tuple(self.cv.buf[idx_border:idx_border + 3]), (200, 200, 200))

    def test_hp_color_thresholds(self):
        self.assertEqual(get_hp_color(1.0), HP_FULL)
        self.assertEqual(get_hp_color(0.55), HP_FULL)
        self.assertEqual(get_hp_color(0.40), HP_MID)
        self.assertEqual(get_hp_color(0.20), HP_LOW)
        self.assertEqual(get_hp_color(0.0), HP_LOW)


class TestScreens(unittest.TestCase):
    def setUp(self):
        self.cv = Canvas(640, 360)

    def test_title_screen_navigation(self):
        title = TitleScreen()
        self.assertEqual(title.selected, 0)
        title.next_option()
        self.assertEqual(title.selected, 1)
        title.prev_option()
        self.assertEqual(title.selected, 0)
        title.prev_option()
        self.assertEqual(title.selected, len(TitleScreen.OPTIONS) - 1)

    def test_title_screen_draw(self):
        title = TitleScreen()
        texts = title.draw(self.cv)
        self.assertGreater(len(texts), 0)
        # Check title text present
        has_title = any("PEACEFUL WAR" in str(t[0]) for t in texts)
        self.assertTrue(has_title)

    def test_how_to_play_screen_draw(self):
        screen = HowToPlayScreen()
        texts = screen.draw(self.cv)
        self.assertGreater(len(texts), 0)
        has_controls = any("HOW TO PLAY" in str(t[0]) for t in texts)
        self.assertTrue(has_controls)

    def test_hud_draw(self):
        hud = HUD()
        data = {
            "turn": 0,
            "p1_hp": 85,
            "p2_hp": 60,
            "angle": 55.0,
            "power": 70,
            "wind": -5,
            "weapon": "SHELL",
        }
        texts = hud.draw(self.cv, data)
        self.assertGreater(len(texts), 0)
        self.assertTrue(any("85 HP" in str(t[0]) for t in texts))
        self.assertTrue(any("60 HP" in str(t[0]) for t in texts))
        self.assertTrue(any("ANG: 55°" in str(t[0]) for t in texts))
        self.assertTrue(any("WIND -5" in str(t[0]) for t in texts))

    def test_pause_overlay(self):
        pause = PauseOverlay()
        self.assertEqual(pause.selected, 0)
        pause.next_option()
        self.assertEqual(pause.selected, 1)
        texts = pause.draw(self.cv)
        self.assertGreater(len(texts), 0)

    def test_game_over_screen(self):
        go_p1 = GameOverScreen(winner=0, total_turns=8)
        texts_p1 = go_p1.draw(self.cv)
        self.assertTrue(any("PLAYER 1" in str(t[0]) for t in texts_p1))

        go_p2 = GameOverScreen(winner=1, total_turns=15)
        texts_p2 = go_p2.draw(self.cv)
        self.assertTrue(any("PLAYER 2" in str(t[0]) for t in texts_p2))

    def test_lab_screen(self):
        lab = LabScreen()
        self.assertIsNotNone(lab.cached_bench)
        self.assertGreater(len(lab.cached_bench), 0)
        texts = lab.draw(self.cv)
        self.assertGreater(len(texts), 0)
        self.assertTrue(any("ALGORITHMS COMPARISON LAB" in str(t[0]) for t in texts))


if __name__ == "__main__":
    unittest.main()
