"""Algorithms Lab screen for Chapter 2 - 5 benchmark and live visualization.

Compares line rendering (Direct vs DDA vs Bresenham) and circle algorithms
alongside runtime benchmarks and pixel counts.
"""

import time
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
    HP_FULL,
    SURFACE_CARD,
    SURFACE_DARK,
    BORDER_MUTED,
    BORDER_ACTIVE,
    draw_box,
    draw_panel,
)


class LabScreen:
    """Live interactive benchmark and visualization for computer graphics algorithms."""

    def __init__(self):
        self.cached_bench = None
        self._run_benchmarks()

    def _run_benchmarks(self):
        """Run benchmark runs and measure timing and pixel count."""
        results = []

        # Benchmark Bresenham line
        class CounterCanvas:
            def __init__(self):
                self.pixels = 0
            def set_pixel(self, x, y, col):
                self.pixels += 1

        c = CounterCanvas()
        t0 = time.perf_counter()
        for _ in range(500):
            line_bresenham(c, 0, 0, 300, 180, (255, 255, 255))
        t1 = time.perf_counter()
        bres_ms = ((t1 - t0) / 500.0) * 1000.0

        results.append({
            "name": "Bresenham (Ch2)",
            "pixels": c.pixels // 500,
            "ms": "%.3f ms" % bres_ms,
            "status": "ACTIVE",
        })

        # Placeholders for Task 1 algorithms if not yet integrated
        try:
            from algo.lines import line_direct
            c = CounterCanvas()
            t0 = time.perf_counter()
            for _ in range(500):
                line_direct(c, 0, 0, 300, 180, (255, 255, 255))
            t1 = time.perf_counter()
            d_ms = ((t1 - t0) / 500.0) * 1000.0
            results.append({
                "name": "Direct naive (Ch2)",
                "pixels": c.pixels // 500,
                "ms": "%.3f ms" % d_ms,
                "status": "ACTIVE",
            })
        except (ImportError, AttributeError):
            results.append({
                "name": "Direct naive (Ch2)",
                "pixels": 301,
                "ms": "~0.045 ms",
                "status": "Task 1 pending",
            })

        try:
            from algo.lines import line_dda
            c = CounterCanvas()
            t0 = time.perf_counter()
            for _ in range(500):
                line_dda(c, 0, 0, 300, 180, (255, 255, 255))
            t1 = time.perf_counter()
            dda_ms = ((t1 - t0) / 500.0) * 1000.0
            results.append({
                "name": "DDA (Ch2)",
                "pixels": c.pixels // 500,
                "ms": "%.3f ms" % dda_ms,
                "status": "ACTIVE",
            })
        except (ImportError, AttributeError):
            results.append({
                "name": "DDA (Ch2)",
                "pixels": 301,
                "ms": "~0.038 ms",
                "status": "Task 1 pending",
            })

        results.append({
            "name": "Midpoint Circle (Ch3)",
            "pixels": 252,
            "ms": "~0.022 ms",
            "status": "Task 1 pending",
        })
        results.append({
            "name": "Polar Circle (Ch3)",
            "pixels": 252,
            "ms": "~0.089 ms",
            "status": "Task 1 pending",
        })

        self.cached_bench = results

    def draw(self, cv):
        texts = []
        center_x = cv.w // 2

        # Header
        draw_panel(cv, 60, 16, cv.w - 120, 38, bg_color=SURFACE_DARK, border_color=ACCENT_GOLD, alpha=230)
        texts.append(("ALGORITHMS COMPARISON LAB", center_x, 22, TEXT_MAIN, FONT_TITLE, "midtop"))
        texts.append(("CHAPTER 2 - 5 ALGORITHM PROFILING & BENCHMARK", center_x, 42, ACCENT_P1, FONT_SMALL, "midtop"))

        # Main Table Box
        tbl_x = 40
        tbl_y = 66
        tbl_w = cv.w - 80
        tbl_h = 240
        draw_panel(cv, tbl_x, tbl_y, tbl_w, tbl_h, bg_color=SURFACE_CARD, border_color=BORDER_MUTED, alpha=230)

        # Table Header Row
        head_y = tbl_y + 12
        cv.hline(tbl_x + 12, tbl_x + tbl_w - 12, head_y + 18, BORDER_MUTED)
        texts.append(("ALGORITHM", tbl_x + 20, head_y, ACCENT_GOLD, FONT_SMALL, "topleft"))
        texts.append(("PX COUNT", tbl_x + 220, head_y, ACCENT_GOLD, FONT_SMALL, "topleft"))
        texts.append(("AVG TIME", tbl_x + 330, head_y, ACCENT_GOLD, FONT_SMALL, "topleft"))
        texts.append(("STATUS", tbl_x + 440, head_y, ACCENT_GOLD, FONT_SMALL, "topleft"))

        # Data Rows
        row_y = head_y + 24
        for item in self.cached_bench:
            status_col = HP_FULL if item["status"] == "ACTIVE" else TEXT_MUTED
            texts.append((item["name"], tbl_x + 20, row_y, TEXT_MAIN, FONT_SMALL, "topleft"))
            texts.append((str(item["pixels"]), tbl_x + 220, row_y, TEXT_HIGHLIGHT, FONT_SMALL, "topleft"))
            texts.append((item["ms"], tbl_x + 330, row_y, ACCENT_P1, FONT_SMALL, "topleft"))
            texts.append((item["status"], tbl_x + 440, row_y, status_col, FONT_SMALL, "topleft"))
            cv.hline(tbl_x + 12, tbl_x + tbl_w - 12, row_y + 18, (34, 24, 46))
            row_y += 24

        # Visual demo box at the bottom of the table
        demo_y = tbl_y + tbl_h - 75
        draw_box(cv, tbl_x + 20, demo_y, tbl_w - 40, 60, fill=(18, 12, 28), border=BORDER_MUTED)
        texts.append(("VISUAL TEST BENCH: Bresenham Line Rasterization Sample", tbl_x + 28, demo_y + 6, TEXT_MUTED, FONT_SMALL, "topleft"))

        # Draw a small sample line in the demo box
        line_bresenham(cv, tbl_x + 30, demo_y + 45, tbl_x + 220, demo_y + 20, ACCENT_P1)
        line_bresenham(cv, tbl_x + 260, demo_y + 45, tbl_x + 450, demo_y + 25, ACCENT_P2)

        # Footer
        texts.append(("Press ESC or ENTER to return to Menu", center_x, cv.h - 24, TEXT_MUTED, FONT_SMALL, "midtop"))

        return texts
