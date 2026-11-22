"""Chapter 2 line tests. Task 1 extends these as it adds Direct, DDA and the
dotted DDA variant."""

import unittest

from algo.lines import line_bresenham, line_direct, line_dda, line_dda_dotted


class Recorder:
    """A canvas stand-in that remembers the pixels instead of drawing them."""

    def __init__(self):
        self.points = []

    def set_pixel(self, x, y, color):
        self.points.append((int(x), int(y)))


def draw_bresenham(x0, y0, x1, y1):
    cv = Recorder()
    line_bresenham(cv, x0, y0, x1, y1, (255, 255, 255))
    return cv.points


def draw_direct(x0, y0, x1, y1):
    cv = Recorder()
    line_direct(cv, x0, y0, x1, y1, (255, 255, 255))
    return cv.points


def draw_dda(x0, y0, x1, y1):
    cv = Recorder()
    line_dda(cv, x0, y0, x1, y1, (255, 255, 255))
    return cv.points


def draw_dda_dotted(x0, y0, x1, y1, gap=4):
    cv = Recorder()
    line_dda_dotted(cv, x0, y0, x1, y1, (255, 255, 255), gap=gap)
    return cv.points


class DirectLineTest(unittest.TestCase):

    def test_hits_both_endpoints(self):
        for line in ((0, 0, 10, 4), (10, 4, 0, 0), (3, 9, 3, 1), (1, 1, 9, 9)):
            pts = draw_direct(*line)
            self.assertEqual(pts[0], (line[0], line[1]))
            self.assertEqual(pts[-1], (line[2], line[3]))

    def test_no_gaps(self):
        for line in ((0, 0, 17, 5), (5, 0, 0, 13), (0, 0, 9, 9), (9, 0, 0, 9)):
            pts = draw_direct(*line)
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                self.assertLessEqual(abs(x1 - x0), 1)
                self.assertLessEqual(abs(y1 - y0), 1)

    def test_pixel_count_is_major_axis_plus_one(self):
        for line in ((0, 0, 10, 4), (0, 0, 4, 10), (6, 6, 6, 6)):
            dx = abs(line[2] - line[0])
            dy = abs(line[3] - line[1])
            self.assertEqual(len(draw_direct(*line)), max(dx, dy) + 1)

    def test_same_pixels_either_direction(self):
        a = draw_direct(2, 3, 19, 11)
        b = draw_direct(19, 11, 2, 3)
        self.assertEqual(set(a), set(b))

    def test_horizontal_and_vertical(self):
        self.assertEqual(draw_direct(0, 5, 4, 5), [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5)])
        self.assertEqual(draw_direct(2, 0, 2, 3), [(2, 0), (2, 1), (2, 2), (2, 3)])

    def test_single_point(self):
        self.assertEqual(draw_direct(4, 4, 4, 4), [(4, 4)])


class DDATest(unittest.TestCase):
    def test_hits_both_endpoints(self):
        for line in ((0, 0, 10, 4), (10, 4, 0, 0), (3, 9, 3, 1), (1, 1, 9, 9)):
            pts = draw_dda(*line)
            self.assertEqual(pts[0], (line[0], line[1]))
            self.assertEqual(pts[-1], (line[2], line[3]))

    def test_no_gaps(self):
        for line in ((0, 0, 17, 5), (5, 0, 0, 13), (0, 0, 9, 9), (9, 0, 0, 9)):
            pts = draw_dda(*line)
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                self.assertLessEqual(abs(x1 - x0), 1)
                self.assertLessEqual(abs(y1 - y0), 1)

    def test_pixel_count_is_major_axis_plus_one(self):
        for line in ((0, 0, 10, 4), (0, 0, 4, 10), (6, 6, 6, 6)):
            dx = abs(line[2] - line[0])
            dy = abs(line[3] - line[1])
            self.assertEqual(len(draw_dda(*line)), max(dx, dy) + 1)

    def test_same_pixels_either_direction(self):
        a = draw_dda(2, 3, 19, 11)
        b = draw_dda(19, 11, 2, 3)
        self.assertEqual(set(a), set(b))

    def test_horizontal_and_vertical(self):
        self.assertEqual(draw_dda(0, 5, 4, 5), [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5)])
        self.assertEqual(draw_dda(2, 0, 2, 3), [(2, 0), (2, 1), (2, 2), (2, 3)])

    def test_single_point(self):
        self.assertEqual(draw_dda(4, 4, 4, 4), [(4, 4)])

    def test_dotted_gap(self):
        pts = draw_dda_dotted(0, 0, 12, 0, gap=3)
        # 13 points total (0..12), step % 3 == 0 => steps 0, 3, 6, 9, 12
        expected = [(0, 0), (3, 0), (6, 0), (9, 0), (12, 0)]
        self.assertEqual(pts, expected)


class BresenhamTest(unittest.TestCase):
    def test_hits_both_endpoints(self):
        for line in ((0, 0, 10, 4), (10, 4, 0, 0), (3, 9, 3, 1), (1, 1, 9, 9)):
            pts = draw_bresenham(*line)
            self.assertEqual(pts[0], (line[0], line[1]))
            self.assertEqual(pts[-1], (line[2], line[3]))

    def test_no_gaps(self):
        for line in ((0, 0, 17, 5), (5, 0, 0, 13), (0, 0, 9, 9), (9, 0, 0, 9)):
            pts = draw_bresenham(*line)
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                self.assertLessEqual(abs(x1 - x0), 1)
                self.assertLessEqual(abs(y1 - y0), 1)

    def test_pixel_count_is_major_axis_plus_one(self):
        for line in ((0, 0, 10, 4), (0, 0, 4, 10), (6, 6, 6, 6)):
            dx = abs(line[2] - line[0])
            dy = abs(line[3] - line[1])
            self.assertEqual(len(draw_bresenham(*line)), max(dx, dy) + 1)

    def test_same_pixels_either_direction(self):
        a = draw_bresenham(2, 3, 19, 11)
        b = draw_bresenham(19, 11, 2, 3)
        self.assertEqual(set(a), set(b))

    def test_horizontal_and_vertical(self):
        self.assertEqual(draw_bresenham(0, 5, 4, 5), [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5)])
        self.assertEqual(draw_bresenham(2, 0, 2, 3), [(2, 0), (2, 1), (2, 2), (2, 3)])



if __name__ == "__main__":
    unittest.main()
