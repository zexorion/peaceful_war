"""Chapter 4 & 5 tests — curves, polygon fill, and terrain destruction (Task 2)."""

import math
import unittest

from algo.curves import bezier, cardinal, curve_screen, hermite
from algo.fill import (
    clip_line_cohen_sutherland,
    fill_polygon,
    flood_fill,
    vertical_gradient,
)
from core.canvas import Canvas
from world.terrain import Terrain


class MockCanvas:
    def __init__(self, w=640, h=360):
        self.w = w
        self.h = h
        self.points = set()

    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.points.add((int(x), int(y)))

    def hline(self, x0, x1, y, color):
        if x1 < x0:
            x0, x1 = x1, x0
        for x in range(int(x0), int(x1) + 1):
            self.set_pixel(x, y, color)


class CurvesTest(unittest.TestCase):
    def test_hermite_endpoints(self):
        p0 = (10, 20)
        p1 = (100, 200)
        t0 = (50, 0)
        t1 = (0, 50)
        pts = hermite(p0, p1, t0, t1, steps=20)
        self.assertEqual(pts[0], p0)
        self.assertEqual(pts[-1], p1)
        self.assertEqual(len(pts), 21)

    def test_bezier_endpoints(self):
        p0 = (0, 0)
        p1 = (50, 100)
        p2 = (100, 0)
        pts = bezier(p0, p1, p2, steps=10)
        self.assertEqual(pts[0], p0)
        self.assertEqual(pts[-1], p2)
        self.assertEqual(len(pts), 11)

    def test_cardinal_interpolates_all_points(self):
        ctrl = [(0, 50), (100, 20), (200, 80), (300, 40)]
        pts = cardinal(ctrl, tension=0.0, steps=10)
        self.assertEqual(pts[0], ctrl[0])
        self.assertEqual(pts[-1], ctrl[-1])
        # Intermediate control points should be hit or extremely close
        for cp in ctrl:
            closest = min(math.hypot(p[0] - cp[0], p[1] - cp[1]) for p in pts)
            self.assertLessEqual(closest, 1.0)

    def test_curve_screen(self):
        cv = MockCanvas()
        pts = [(10, 10), (30, 40), (60, 20)]
        curve_screen(cv, pts, (255, 255, 255))
        self.assertGreater(len(cv.points), len(pts))
        self.assertIn((10, 10), cv.points)
        self.assertIn((60, 20), cv.points)


class FillTest(unittest.TestCase):
    def test_fill_polygon_square(self):
        cv = MockCanvas()
        # Square from (10, 10) to (20, 20)
        poly = [(10, 10), (20, 10), (20, 20), (10, 20)]
        fill_polygon(cv, poly, (255, 255, 255))
        # Interior points should all be set
        for x in range(11, 20):
            for y in range(11, 20):
                self.assertIn((x, y), cv.points)

    def test_vertical_gradient(self):
        cv = Canvas(100, 50)
        c_top = (0, 0, 0)
        c_bot = (100, 200, 255)
        vertical_gradient(cv, 0, 49, c_top, c_bot)
        # Check top row
        self.assertEqual(cv.buf[0], 0)
        self.assertEqual(cv.buf[1], 0)
        self.assertEqual(cv.buf[2], 0)
        # Check bottom row
        last_idx = (49 * 100 + 50) * 3
        self.assertEqual(cv.buf[last_idx], 100)
        self.assertEqual(cv.buf[last_idx + 1], 200)
        self.assertEqual(cv.buf[last_idx + 2], 255)

    def test_flood_fill(self):
        cv = Canvas(20, 20, fill=(0, 0, 0))
        # Draw a small 5x5 box boundary with white
        for x in range(5, 11):
            cv.set_pixel(x, 5, (255, 255, 255))
            cv.set_pixel(x, 10, (255, 255, 255))
        for y in range(5, 11):
            cv.set_pixel(5, y, (255, 255, 255))
            cv.set_pixel(10, y, (255, 255, 255))

        flood_fill(cv, 7, 7, (200, 100, 50))
        # Inside pixel changed
        idx = (7 * 20 + 7) * 3
        self.assertEqual((cv.buf[idx], cv.buf[idx + 1], cv.buf[idx + 2]), (200, 100, 50))
        # Outside pixel unchanged
        out_idx = (0 * 20 + 0) * 3
        self.assertEqual((cv.buf[out_idx], cv.buf[out_idx + 1], cv.buf[out_idx + 2]), (0, 0, 0))

    def test_cohen_sutherland_clipping(self):
        # Inside
        res = clip_line_cohen_sutherland(10, 10, 50, 50, 0, 0, 100, 100)
        self.assertEqual(res, (10, 10, 50, 50))
        # Outside (trivial reject)
        res = clip_line_cohen_sutherland(120, 10, 150, 50, 0, 0, 100, 100)
        self.assertIsNone(res)
        # Partially clipped
        res = clip_line_cohen_sutherland(-50, 50, 50, 50, 0, 0, 100, 100)
        self.assertIsNotNone(res)
        self.assertEqual(res[0], 0)
        self.assertEqual(res[1], 50)
        self.assertEqual(res[2], 50)
        self.assertEqual(res[3], 50)


class TerrainTest(unittest.TestCase):
    def test_deterministic_seed(self):
        t1 = Terrain(640, 360, seed=42)
        t2 = Terrain(640, 360, seed=42)
        self.assertEqual(t1.heights, t2.heights)

    def test_different_seeds_produce_different_terrains(self):
        t1 = Terrain(640, 360, seed=1)
        t2 = Terrain(640, 360, seed=2)
        self.assertNotEqual(t1.heights, t2.heights)

    def test_all_columns_valid(self):
        t = Terrain(640, 360, seed=7)
        self.assertEqual(len(t.heights), 640)
        for x in range(640):
            h = t.height_at(x)
            self.assertGreater(h, 0)
            self.assertLess(h, 360 - 2)

    def test_is_solid(self):
        t = Terrain(640, 360, seed=7)
        hy = t.height_at(100)
        self.assertFalse(t.is_solid(100, hy - 5))
        self.assertTrue(t.is_solid(100, hy))
        self.assertTrue(t.is_solid(100, hy + 5))

    def test_carve_crater(self):
        t = Terrain(640, 360, seed=7)
        cx = 200
        cy = t.height_at(cx)
        r = 25

        old_center_y = t.height_at(cx)
        old_outside_y = t.height_at(cx + r + 10)

        x0, x1 = t.carve(cx, cy, r)
        self.assertEqual(x0, cx - r)
        self.assertEqual(x1, cx + r)

        # Center height increased (surface lowered to crater bottom)
        new_center_y = t.height_at(cx)
        self.assertGreater(new_center_y, old_center_y)

        # Outside columns completely untouched
        self.assertEqual(t.height_at(cx + r + 10), old_outside_y)

    def test_render_writes_pixels(self):
        t = Terrain(640, 360, seed=7)
        cv = Canvas(640, 360)
        t.render(cv)
        # Check that canvas buffer is not all black
        self.assertTrue(any(byte != 0 for byte in cv.buf))


if __name__ == "__main__":
    unittest.main()
