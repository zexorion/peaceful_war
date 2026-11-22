"""Chapter 3 circle and ellipse tests (Task 1)."""

import math
import unittest

from algo.circles import (
    circle_midpoint,
    circle_polar,
    disc_midpoint,
    ellipse_midpoint,
    lab_report,
)


class Recorder:
    def __init__(self):
        self.points = set()

    def set_pixel(self, x, y, color):
        self.points.add((int(x), int(y)))

    def hline(self, x0, x1, y, color):
        if x1 < x0:
            x0, x1 = x1, x0
        for x in range(int(x0), int(x1) + 1):
            self.points.add((x, int(y)))

    def vline(self, x, y0, y1, color):
        if y1 < y0:
            y0, y1 = y1, y0
        for y in range(int(y0), int(y1) + 1):
            self.points.add((int(x), y))


class MidpointCircleTest(unittest.TestCase):
    def test_single_point_and_negative(self):
        cv = Recorder()
        circle_midpoint(cv, 10, 10, 0, (255, 255, 255))
        self.assertEqual(cv.points, {(10, 10)})

        cv2 = Recorder()
        circle_midpoint(cv2, 10, 10, -5, (255, 255, 255))
        self.assertEqual(len(cv2.points), 0)

    def test_cardinal_points(self):
        cv = Recorder()
        cx, cy, r = 50, 50, 20
        circle_midpoint(cv, cx, cy, r, (255, 255, 255))
        for pt in ((cx + r, cy), (cx - r, cy), (cx, cy + r), (cx, cy - r)):
            self.assertIn(pt, cv.points)

    def test_points_close_to_radius(self):
        cv = Recorder()
        cx, cy, r = 100, 100, 30
        circle_midpoint(cv, cx, cy, r, (255, 255, 255))
        for x, y in cv.points:
            dist = math.hypot(x - cx, y - cy)
            self.assertAlmostEqual(dist, r, delta=1.5)


class DiscMidpointTest(unittest.TestCase):
    def test_fills_interior(self):
        cv = Recorder()
        cx, cy, r = 50, 50, 15
        disc_midpoint(cv, cx, cy, r, (255, 255, 255))
        # Center must be filled
        self.assertIn((cx, cy), cv.points)
        # Cardinal extremes must be present
        for pt in ((cx + r, cy), (cx - r, cy), (cx, cy + r), (cx, cy - r)):
            self.assertIn(pt, cv.points)
        # Expected area roughly pi * r^2
        expected_area = math.pi * (r ** 2)
        self.assertAlmostEqual(len(cv.points), expected_area, delta=expected_area * 0.15)


class EllipseMidpointTest(unittest.TestCase):
    def test_cardinal_points(self):
        cv = Recorder()
        cx, cy, rx, ry = 60, 60, 25, 12
        ellipse_midpoint(cv, cx, cy, rx, ry, (255, 255, 255))
        for pt in ((cx + rx, cy), (cx - rx, cy), (cx, cy + ry), (cx, cy - ry)):
            self.assertIn(pt, cv.points)

    def test_flat_ellipse(self):
        cv = Recorder()
        ellipse_midpoint(cv, 10, 10, 10, 0, (255, 255, 255))
        self.assertTrue(len(cv.points) > 0)


class PolarCircleTest(unittest.TestCase):
    def test_cardinal_points_and_count(self):
        cv_mid = Recorder()
        cv_pol = Recorder()
        cx, cy, r = 50, 50, 25
        circle_midpoint(cv_mid, cx, cy, r, (255, 255, 255))
        circle_polar(cv_pol, cx, cy, r, (255, 255, 255))

        for pt in ((cx + r, cy), (cx - r, cy), (cx, cy + r), (cx, cy - r)):
            self.assertIn(pt, cv_pol.points)
        # Pixel counts should be comparable
        self.assertAlmostEqual(len(cv_pol.points), len(cv_mid.points), delta=20)


class LabReportTest(unittest.TestCase):
    def test_report_structure(self):
        data = lab_report()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 5)
        for item in data:
            self.assertIn("name", item)
            self.assertIn("pixels", item)
            self.assertIn("ms", item)
            self.assertIsInstance(item["pixels"], int)
            self.assertIsInstance(item["ms"], (int, float))


if __name__ == "__main__":
    unittest.main()
