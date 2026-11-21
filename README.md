# Peaceful War

A retro turn-based 2D artillery game built from scratch using fundamental Computer Graphics algorithms. Every visual element—lines, circles, curves, fills, and destructible terrain—is rasterized pixel-by-pixel onto a custom software canvas without using high-level drawing libraries (zero `pygame.draw.*`).

---

## Features

- **Software Rasterization:** Pure software-rendered graphics buffer at a native 640×360 resolution with clean integer scaling.
- **Classic Graphics Algorithms:**
  - **Lines:** Direct, DDA, Bresenham.
  - **Curves & Circles:** Midpoint Circle, Polar Circle, Ellipse, Hermite Curves.
  - **Filling:** Scan-line polygon filling and procedural gradient fills.
- **Destructible Terrain:** Dynamic procedural heightmap with real-time explosion carving and terrain deformation.
- **Artillery Mechanics:** Ballistic trajectory physics (gravity, wind), angle/power adjustments, and turn-based combat.

---

## Quickstart

### Prerequisites
- Python 3.11+

### Installation & Run

```bash
# Clone the repository
git clone https://github.com/zexorion/peaceful_war.git
cd peaceful_war

# Setup virtual environment
python3 -m venv .venv

# On Linux / macOS:
source .venv/bin/activate
pip install -r requirements.txt
python main.py

# On Windows:
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Additional Commands

- **Run tests:**
  ```bash
  python -m unittest discover -s tests -t .
  ```
- **Capture headless frame:**
  ```bash
  python main.py --shot out/screenshot.png
  ```

---

## Controls

| Key | Action |
| --- | --- |
| `←` / `→` | Adjust barrel aim angle |
| `Space` | Fire projectile |
| `F11` | Toggle Fullscreen |
| `ESC` | Quit |

---

## Project Structure

```text
peaceful_war/
├── main.py              # Application entry point & game loop
├── config.py            # Global constants, colors, and configuration
├── core/                # Low-level canvas, buffer management, display scaler
├── algo/                # Graphics algorithms (lines, circles, curves, fills)
├── world/               # Terrain generation, destruction, and physics
├── game/                # State machine and turn-based game loop
├── ui/                  # HUD and screen management
└── tests/               # Unit and algorithm verification tests
```

---

## Core Rule

All graphics must be plotted via `core/canvas.py` (`Canvas.set_pixel` and low-level spans). External drawing wrappers like `pygame.draw` are strictly prohibited. Pygame is utilized solely for window management, user input handling, and font rendering.
