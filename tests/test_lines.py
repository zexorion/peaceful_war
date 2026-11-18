"""Chapter 2 line tests. Task 1 extends these as it adds Direct, DDA and the
dotted DDA variant."""

import unittest

from algo.lines import line_bresenham


class Recorder:
    """A canvas stand-in that remembers the pixels instead of drawing them."""

    def __init__(self):
        self.points = []

    def set_pixel(self, x, y, color):
        self.points.append((int(x), int(y)))


def draw(x0, y0, x1, y1):
    cv = Recorder()
    line_bresenham(cv, x0, y0, x1, y1, (255, 255, 255))
    return cv.points


class BresenhamTest(unittest.TestCase):
    def test_hits_both_endpoints(self):
        for line in ((0, 0, 10, 4), (10, 4, 0, 0), (3, 9, 3, 1), (1, 1, 9, 9)):
            pts = draw(*line)
            self.assertEqual(pts[0], (line[0], line[1]))
            self.assertEqual(pts[-1], (line[2], line[3]))

    def test_no_gaps(self):
        for line in ((0, 0, 17, 5), (5, 0, 0, 13), (0, 0, 9, 9), (9, 0, 0, 9)):
            pts = draw(*line)
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                self.assertLessEqual(abs(x1 - x0), 1)
                self.assertLessEqual(abs(y1 - y0), 1)

    def test_pixel_count_is_major_axis_plus_one(self):
        for line in ((0, 0, 10, 4), (0, 0, 4, 10), (6, 6, 6, 6)):
            dx = abs(line[2] - line[0])
            dy = abs(line[3] - line[1])
            self.assertEqual(len(draw(*line)), max(dx, dy) + 1)

    def test_same_pixels_either_direction(self):
        a = draw(2, 3, 19, 11)
        b = draw(19, 11, 2, 3)
        self.assertEqual(set(a), set(b))

    def test_horizontal_and_vertical(self):
        self.assertEqual(draw(0, 5, 4, 5), [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5)])
        self.assertEqual(draw(2, 0, 2, 3), [(2, 0), (2, 1), (2, 2), (2, 3)])


if __name__ == "__main__":
    unittest.main()
