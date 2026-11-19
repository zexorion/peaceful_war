"""Art and procedural graphics module for Peaceful War (Task 4).

Renders a painterly, scenic sunset landscape with rolling hills, distant mountain
silhouettes, sunset clouds, and stylized military tanks perched on the ridges
(modeled after the serene sunset valley artwork).

100% pure software rendering on Canvas using Bresenham lines, spans, and blend_pixel.
"""

import math
import random
import config as C
from algo.lines import line_bresenham
from core.util import clamp, lerp, lerp_color


# --- Scenic Sunset Palette ---------------------------------------------------
SKY_TOP_TWILIGHT = (130, 118, 142)    # Muted lavender-grey
SKY_MID_ROSE = (184, 144, 154)        # Dusty twilight rose
SKY_WARM_PEACH = (238, 164, 118)      # Apricot peach
SKY_HORIZON_GOLD = (254, 208, 146)    # Sunset glow at horizon

CLOUD_SHADOW = (152, 130, 148)        # Cloud body in twilight
CLOUD_WARM = (232, 148, 98)           # Sunlit cloud underside
CLOUD_GOLD = (255, 218, 154)          # Cloud highlight rim

# Mountains (Atmospheric depth layers)
MOUNTAIN_FAR = (165, 146, 175)        # Distant hazy lilac ridge
MOUNTAIN_MID = (178, 120, 128)        # Mid-distance warm plum ridge
MOUNTAIN_RIM = (215, 148, 140)        # Sunlit crest on mid-mountains

# Foreground Valley & Grassy Terrain
GRASS_SUNLIT_RIM = (248, 212, 130)    # Golden sunlight rim catching hill tops
GRASS_TOP = (118, 128, 92)            # Warm olive meadow grass
GRASS_SHADE = (84, 92, 68)            # Sloped shadow grass
EARTH_MID = (58, 62, 50)              # Subsurface soil
EARTH_DEEP = (34, 36, 30)             # Deep crust loam

# Tank 1 (Player 1 - Steel/Sky Blue)
P1_BASE = (72, 112, 150)
P1_LIGHT = (118, 162, 205)
P1_DARK = (42, 66, 92)
P1_ACCENT = (145, 210, 255)

# Tank 2 (Player 2 - Terracotta/Sunset Orange)
P2_BASE = (212, 102, 44)
P2_LIGHT = (248, 148, 78)
P2_DARK = (136, 56, 24)
P2_ACCENT = (255, 200, 110)

# Shared Tank Running Gear
TANK_TREAD = (42, 40, 38)
TANK_WHEEL_RIM = (135, 140, 130)
TANK_WHEEL_HUB = (45, 46, 44)


def draw_scenic_sunset_sky(cv):
    """Render painterly sunset sky gradient with soft, organically feathered clouds."""
    w, h = cv.w, cv.h

    # 1. Multi-band Sunset Sky Gradient
    for y in range(h):
        t = y / float(h - 1)
        if t < 0.28:
            col = lerp_color(SKY_TOP_TWILIGHT, SKY_MID_ROSE, t / 0.28)
        elif t < 0.60:
            col = lerp_color(SKY_MID_ROSE, SKY_WARM_PEACH, (t - 0.28) / 0.32)
        elif t < 0.85:
            col = lerp_color(SKY_WARM_PEACH, SKY_HORIZON_GOLD, (t - 0.60) / 0.25)
        else:
            col = SKY_HORIZON_GOLD
        cv.hline(0, w - 1, y, col)

    # 2. Feathered Painterly Sunset Clouds
    cloud_clusters = [
        # Left drifting cloud formation
        [(110, 52, 52, 18), (145, 46, 60, 22), (185, 54, 48, 16), (130, 60, 70, 14)],
        # Center-right billowing sunset clouds
        [(340, 68, 60, 22), (385, 58, 70, 26), (435, 64, 65, 24), (480, 74, 55, 18), (405, 78, 90, 16)],
        # Far right golden sunset clouds
        [(565, 85, 65, 22), (605, 78, 58, 20), (585, 94, 75, 16)],
        # Low gentle cloud wisp on left
        [(45, 95, 38, 14), (72, 92, 44, 16), (62, 102, 48, 12)],
    ]

    for cluster in cloud_clusters:
        for cx, cy, rx, ry in cluster:
            rx2 = float(rx * rx)
            ry2 = float(ry * ry)
            for py in range(cy - ry, cy + ry + 1):
                if not (0 <= py < h):
                    continue
                dy = py - cy
                dy2 = float(dy * dy)
                for px in range(cx - rx, cx + rx + 1):
                    if not (0 <= px < w):
                        continue
                    dx = px - cx
                    dist_norm = (dx * dx) / rx2 + dy2 / ry2
                    if dist_norm <= 1.0:
                        edge_feather = (1.0 - dist_norm) ** 1.2
                        v_ratio = (dy + ry) / float(2 * ry)
                        if v_ratio > 0.62:
                            t_gold = (v_ratio - 0.62) / 0.38
                            col = lerp_color(CLOUD_WARM, CLOUD_GOLD, t_gold)
                            alpha = int(edge_feather * (140 + t_gold * 85))
                        elif v_ratio > 0.30:
                            t_mid = (v_ratio - 0.30) / 0.32
                            col = lerp_color(CLOUD_SHADOW, CLOUD_WARM, t_mid)
                            alpha = int(edge_feather * 125)
                        else:
                            col = CLOUD_SHADOW
                            alpha = int(edge_feather * 105)

                        cv.blend_pixel(px, py, col, alpha)

    # 3. Distant Atmospheric Mountain Silhouette Layers
    # Far mountain ridge (Pale atmospheric hazy lilac)
    far_mountain_y = []
    for x in range(w):
        u = (x / float(w)) * 2.0 * math.pi
        m_far = 140 + math.sin(u * 1.5 + 0.3) * 16 + math.sin(u * 3.6) * 8 + math.sin(u * 8.0) * 3
        far_mountain_y.append(int(m_far))

    for x in range(w):
        m_top = far_mountain_y[x]
        for y in range(m_top, min(h, m_top + 40)):
            t = (y - m_top) / 40.0
            col = lerp_color(MOUNTAIN_FAR, SKY_HORIZON_GOLD, t * 0.42)
            cv.blend_pixel(x, y, col, int((1.0 - t * 0.3) * 150))

    # Mid-distance mountain ridge (Warm plum with sunlit golden peaks)
    mid_mountain_y = []
    for x in range(w):
        u = (x / float(w)) * 2.0 * math.pi
        m_mid = 158 + math.sin(u * 2.0 + 1.2) * 18 + math.sin(u * 4.6) * 7 + math.sin(u * 10.0) * 2.5
        mid_mountain_y.append(int(m_mid))

    for x in range(w):
        m_top = mid_mountain_y[x]
        cv.blend_pixel(x, m_top, MOUNTAIN_RIM, 190)
        for y in range(m_top + 1, min(h, m_top + 55)):
            t = (y - m_top) / 55.0
            col = lerp_color(MOUNTAIN_MID, SKY_WARM_PEACH, t * 0.38)
            cv.blend_pixel(x, y, col, int((1.0 - t * 0.25) * 180))


def generate_scenic_valley_heights(width, height):
    """Generate smooth, rolling meadow hills with smooth hilltop crests for tanks."""
    heights = []
    w = float(width)

    for x in range(width):
        u = (x / w) * 2.0 * math.pi

        # Smooth natural hill crests using wide Gaussians (slope naturally equals 0 at x=110 and x=530)
        left_hill = -34.0 * math.exp(-(((x - 110) / 105.0) ** 2))
        right_hill = -28.0 * math.exp(-(((x - 530) / 115.0) ** 2))

        # Gentle valley floor in center
        valley_dip = 22.0 * math.exp(-(((x - 320) / 160.0) ** 2))

        # Broad natural undulations
        rolling = math.sin(u * 2.0 + 0.3) * 5.0 + math.sin(u * 4.0) * 2.0

        base_y = height * 0.58
        y = base_y + left_hill + right_hill + valley_dip + rolling
        heights.append(int(clamp(y, height * 0.44, height - 35)))

    return heights


def render_scenic_valley_terrain(cv, heights):
    """Render rolling meadow valley with warm golden sunlight catching the ridges."""
    w, h = cv.w, cv.h

    for x in range(w):
        top_y = heights[x]

        # Calculate slope to determine sunlit faces (sunset on the right)
        prev_x = max(0, x - 3)
        next_x = min(w - 1, x + 3)
        slope = (heights[next_x] - heights[prev_x]) / float(next_x - prev_x)

        # Sun-catch factor
        sun_exposure = clamp((slope * 1.0) + 0.40, 0.0, 1.0)
        surface_rim_col = lerp_color(GRASS_TOP, GRASS_SUNLIT_RIM, sun_exposure)

        # 1. Golden sunlight rim line on terrain surface
        cv.set_pixel(x, top_y, surface_rim_col)
        if sun_exposure > 0.45:
            cv.blend_pixel(x, top_y - 1, GRASS_SUNLIT_RIM, int(sun_exposure * 160))

        # 2. Consistent horizontal soil and grass depth fill (prevents vertical striping)
        span = h - top_y
        if span > 0:
            for y in range(top_y + 1, h):
                t = (y - top_y) / float(span)
                if t < 0.12:
                    # Top grass layer
                    col = lerp_color(GRASS_TOP, GRASS_SHADE, t / 0.12)
                elif t < 0.55:
                    # Subsurface earth
                    col = lerp_color(GRASS_SHADE, EARTH_MID, (t - 0.12) / 0.43)
                else:
                    # Deep loam
                    col = lerp_color(EARTH_MID, EARTH_DEEP, (t - 0.55) / 0.45)

                cv.set_pixel(x, y, col)

    # 3. Scenic foreground wildflowers and grass tufts
    rng = random.Random(101)
    for fx in range(12, w - 12, 5):
        fy = heights[fx]
        if rng.random() < 0.32:
            cv.set_pixel(fx, fy - 1, GRASS_TOP)
            cv.set_pixel(fx + 1, fy - 2, GRASS_SUNLIT_RIM)
        if rng.random() < 0.20:
            cv.blend_pixel(fx, fy - 2, GRASS_SUNLIT_RIM, 220)
            cv.blend_pixel(fx - 1, fy - 1, (255, 235, 170), 160)


def draw_scenic_tank(cv, x, y, angle, is_p1=True):
    """Draw a stylized military tank matching the scenic illustration.

    - P1: Steel/Sky Blue tank perched on left ridge, aiming rightwards.
    - P2: Terracotta/Sunset Orange tank perched on right hillside, aiming leftwards.
    """
    x = int(x)
    y = int(y)
    facing = 1 if is_p1 else -1

    base_col = P1_BASE if is_p1 else P2_BASE
    light_col = P1_LIGHT if is_p1 else P2_LIGHT
    dark_col = P1_DARK if is_p1 else P2_DARK
    accent_col = P1_ACCENT if is_p1 else P2_ACCENT

    # -------------------------------------------------------------------------
    # 1. Soft Shadow on the grassy hill
    # -------------------------------------------------------------------------
    for sx in range(x - 20, x + 21):
        cv.blend_pixel(sx, y + 1, (22, 26, 20), 160)
        cv.blend_pixel(sx, y + 2, (22, 26, 20), 90)

    # -------------------------------------------------------------------------
    # 2. Tracks & Road Wheels
    # -------------------------------------------------------------------------
    track_y0 = y - 6
    track_y1 = y
    track_x0 = x - 18
    track_x1 = x + 18

    # Dark track housing
    cv.rect(track_x0, track_y0 + 1, 37, 5, TANK_TREAD)
    cv.hline(track_x0 + 2, track_x1 - 2, track_y0, (30, 28, 26))
    cv.hline(track_x0 + 1, track_x1 - 1, track_y1, (20, 18, 16))

    # Curved track endpoints
    cv.set_pixel(track_x0, track_y0 + 2, (55, 50, 45))
    cv.set_pixel(track_x0 + 1, track_y0 + 1, (75, 70, 65))
    cv.set_pixel(track_x1, track_y0 + 2, (55, 50, 45))
    cv.set_pixel(track_x1 - 1, track_y0 + 1, (75, 70, 65))

    # Four road wheels
    wheel_xs = [x - 12, x - 4, x + 4, x + 12]
    wheel_y = track_y0 + 3
    for wx in wheel_xs:
        cv.rect(wx - 2, wheel_y - 2, 5, 5, TANK_WHEEL_RIM)
        cv.set_pixel(wx, wheel_y, TANK_WHEEL_HUB)
        cv.set_pixel(wx - 2, wheel_y - 2, (180, 185, 175))
        cv.set_pixel(wx + 2, wheel_y + 2, (30, 32, 30))

    # -------------------------------------------------------------------------
    # 3. Main Hull (Chassis with sloped armor)
    # -------------------------------------------------------------------------
    hull_y0 = y - 13

    # Mudguard runner
    cv.hline(track_x0 - 1, track_x1 + 1, track_y0, light_col)
    cv.hline(track_x0 - 2, track_x1 + 2, track_y0 - 1, dark_col)

    # Armored hull body
    cv.rect(x - 16, hull_y0 + 2, 32, 4, base_col)

    # Sloped front & rear armor
    if facing == 1:
        line_bresenham(cv, x + 16, track_y0, x + 11, hull_y0, light_col)
        line_bresenham(cv, x + 15, track_y0, x + 10, hull_y0, base_col)
        line_bresenham(cv, x - 16, track_y0, x - 13, hull_y0, dark_col)
    else:
        line_bresenham(cv, x - 16, track_y0, x - 11, hull_y0, light_col)
        line_bresenham(cv, x - 15, track_y0, x - 10, hull_y0, base_col)
        line_bresenham(cv, x + 16, track_y0, x + 13, hull_y0, dark_col)

    # Upper hull deck
    cv.hline(x - 12, x + 12, hull_y0, light_col)

    # Decorative team insignia on hull side
    cv.rect(x - 2, hull_y0 + 2, 4, 3, accent_col)

    # -------------------------------------------------------------------------
    # 4. Cast Rounded Turret Dome & Cupola
    # -------------------------------------------------------------------------
    turret_cx = (x - 1) if facing == 1 else (x + 1)
    turret_cy = y - 16

    # Turret dome
    cv.rect(turret_cx - 8, turret_cy - 1, 16, 4, base_col)
    cv.hline(turret_cx - 7, turret_cx + 7, turret_cy - 2, light_col)
    cv.hline(turret_cx - 8, turret_cx + 8, turret_cy + 3, dark_col)

    # Upper dome curve
    cv.rect(turret_cx - 5, turret_cy - 4, 10, 3, base_col)
    cv.hline(turret_cx - 4, turret_cx + 4, turret_cy - 5, light_col)

    # Commander's Cupola / Hatch
    cupola_x = (turret_cx - 3) if facing == 1 else (turret_cx + 1)
    cv.rect(cupola_x, turret_cy - 7, 4, 2, dark_col)
    cv.hline(cupola_x, cupola_x + 3, turret_cy - 7, light_col)

    # Turret star / team emblem
    cv.set_pixel(turret_cx, turret_cy - 1, accent_col)

    # -------------------------------------------------------------------------
    # 5. Heavy Rotating Cannon Barrel with Mantlet & Muzzle
    # -------------------------------------------------------------------------
    rad = math.radians(angle)
    pivot_x = turret_cx + (2 if facing == 1 else -2)
    pivot_y = turret_cy - 1

    # Armored mantlet collar
    mantlet_ox = int(pivot_x + math.cos(rad) * 3)
    mantlet_oy = int(pivot_y - math.sin(rad) * 3)
    cv.rect(mantlet_ox - 2, mantlet_oy - 2, 5, 5, dark_col)
    cv.rect(mantlet_ox - 1, mantlet_oy - 1, 3, 3, light_col)

    # 20-pixel long cannon barrel
    barrel_len = 20
    end_x = int(pivot_x + math.cos(rad) * barrel_len)
    end_y = int(pivot_y - math.sin(rad) * barrel_len)

    line_bresenham(cv, pivot_x, pivot_y, end_x, end_y, dark_col)
    line_bresenham(cv, pivot_x, pivot_y - 1, end_x, end_y - 1, light_col)

    # Muzzle ring at tip
    perp_dx = int(-math.sin(rad) * 2)
    perp_dy = int(-math.cos(rad) * 2)
    line_bresenham(cv, end_x - perp_dx, end_y - perp_dy, end_x + perp_dx, end_y + perp_dy, dark_col)
    cv.set_pixel(end_x, end_y, (18, 18, 18))
