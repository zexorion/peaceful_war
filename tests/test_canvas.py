"""Canvas unit tests — stdlib only, no window needed.

Run from the project root:   python -m unittest discover -s tests -t .

Task 1 extends this file. The point is not the tests themselves, it is the
habit: every algorithm module ships with a test that proves its pixels.
"""

import unittest

from core.canvas import Canvas


class CanvasTest(unittest.TestCase):
    def test_starts_filled(self):
        cv = Canvas(2, 2, fill=(10, 20, 30))
        self.assertEqual(cv.buf, bytes((10, 20, 30)) * 4)

    def test_set_and_read_pixel(self):
        cv = Canvas(3, 3)
        cv.set_pixel(1, 2, (255, 0, 0))
        i = (2 * 3 + 1) * 3
        self.assertEqual(tuple(cv.buf[i : i + 3]), (255, 0, 0))

    def test_offcanvas_writes_are_ignored(self):
        cv = Canvas(4, 4, fill=(0, 0, 0))
        for x, y in ((-1, 0), (0, -1), (4, 0), (0, 4), (99, 99)):
            cv.set_pixel(x, y, (255, 255, 255))
        self.assertEqual(cv.buf, bytes(4 * 4 * 3))

    def test_hline_is_clipped_and_ordered(self):
        cv = Canvas(5, 2)
        cv.hline(4, 2, 0, (1, 2, 3))
        row = [tuple(cv.buf[(0 * 5 + x) * 3 : (0 * 5 + x) * 3 + 3]) for x in range(5)]
        self.assertEqual(row[2:5], [(1, 2, 3)] * 3)
        self.assertEqual(row[0:2], [(0, 0, 0)] * 2)

    def test_blend_pixel_mixes(self):
        cv = Canvas(1, 1, fill=(0, 0, 0))
        cv.blend_pixel(0, 0, (255, 255, 255), 128)
        self.assertTrue(all(abs(v - 127) <= 1 for v in cv.buf))

    def test_snapshot_round_trip(self):
        cv = Canvas(2, 2)
        cv.set_pixel(0, 0, (9, 9, 9))
        snap = cv.snapshot()
        cv.clear()
        cv.restore(snap)
        self.assertEqual(cv.buf, snap)


if __name__ == "__main__":
    unittest.main()
