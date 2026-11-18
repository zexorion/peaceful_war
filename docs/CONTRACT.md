# CONTRACT — العقد التقني بين الفرق

> **اقرأ ده قبل أول سطر كود.** أي خلاف على التوقيعات بيتحسم هنا، مش في الكومنتات.

الغرض: 8 أفراد بيشتغلوا بالتوازي من غير ما يستنوا بعض. لو كل تاسك مشي على التوقيعات دي، الدمج بيبقى لصق مش إعادة كتابة.

---

## 1. الإحداثيات والألوان

- الأصل **أعلى الشمال**، `x` لليمين، `y` لتحت (اصطلاح Ch2–Ch6 في الكتاب).
- كل الإحداثيات **أعداد صحيحة بالبكسل** في الدقة الداخلية 640×360.
- اللون = tuple من 3 أرقام `(r, g, b)` من 0 لـ 255. مفيش alpha في نوع اللون؛ الشفافية بتتبعت كوسيط لوحدها في `blend_pixel`.
- الدوران بالسالب/الموجب: `rotate` بتلف عكس عقارب الساعة على الشاشة (يعني زاوية المدفع بتزيد = لفوق).

---

## 2. Canvas — الطبقة الوحيدة اللي بتمسك بكسل

`core/canvas.py` (Task 1). ممنوع أي موديول تاني يعمل `import pygame` عشان يرسم.

```python
Canvas(w, h, fill=(0, 0, 0))
cv.w, cv.h, cv.buf                      # buf = bytearray RGB
cv.set_pixel(x, y, color)               # clipped
cv.blend_pixel(x, y, color, alpha)      # alpha 0..255
cv.hline(x0, x1, y, color)              # ordered + clipped
cv.vline(x, y0, y1, color)              # ordered + clipped
cv.rect(x, y, w, h, color)              # filled, spans
cv.clear(color)
cv.snapshot() -> bytes                  # cache the static layer
cv.restore(snap)                        # one C-level copy
```

**قاعدة الأداء:** كل حاجة ثابتة (سما، نجوم، قمر، تضاريس) بتترسم مرة واحدة وتتحفظ بـ `snapshot`.
كل فريم بيبدأ بـ `restore` وبعدها بيتضاف اللي بيتحرك بس.

---

## 3. توقيعات الخوارزميات

### موجودة الآن (Task 1 بيكمّلها)

```python
# algo/lines.py — Ch2
line_bresenham(cv, x0, y0, x1, y1, color)
line_dda_dotted(cv, x0, y0, x1, y1, color, gap=4)
# يضيف: line_direct(cv, ..., color) · line_dda(cv, ..., color)

# algo/circles.py — Ch3
circle_direct(cv, cx, cy, r, color)     # fallback
disc_spans(cv, cx, cy, r, color)
disc_blend(cv, cx, cy, r, color, alpha)
# يضيف: circle_midpoint(...) · ellipse_midpoint(cv, cx, cy, rx, ry, color) · circle_polar(...)
```

### Task 2

```python
# algo/curves.py — Ch4 (كلها ترجع list[tuple[int,int]] نقاط جاهزة للربط بـ Bresenham)
hermite(p0, p1, t0, t1, steps) -> [(x, y), ...]
bezier(p0, p1, p2, steps) -> [(x, y), ...]          # stretch
cardinal(points, tension, steps) -> [(x, y), ...]   # stretch
curve_screen(cv, points, color)                     # ties points with Bresenham

# algo/fill.py — Ch5/Ch6
fill_polygon(cv, points, color)              # general scan-line, even-odd
vertical_gradient(cv, y0, y1, c0, c1)        # Gouraud-style, per row
flood_fill(cv, x, y, color)                  # stretch
clip_line_cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax) -> clipped or None   # stretch

# world/terrain.py
terrain = Terrain(width, height, seed)
terrain.w, terrain.h, terrain.heights        # heights[x] = surface y
terrain.height_at(x) -> int
terrain.is_solid(x, y) -> bool
terrain.render(cv)                           # رسم التضاريس فوق اللي موجود
terrain.carve(cx, cy, r) -> (x0, x1)         # حفرة: تعدّل heights وترجع المدى المتأثر
```

**بعد كل حفرة (تكامل Task 2 + Task 3):** التضاريس بتترسم فوق الـ sky snapshot، مش فوق الصورة القديمة:

```python
sky = ...                      # snapshot للسما والنجوم والقمر (ثابت)
terrain.carve(cx, cy, r)
background = rebuild_background(cv, terrain, sky)   # موجودة في main.py
```

من غير `restore(sky)` الأول، التضاريس القديمة هتفضل تحت وباينة كشبح حوالين الحفرة.
التكلفة ~45ms وبتتنفذ **مرة واحدة لكل انفجار**، مش كل فريم.

### Task 3

```python
# world/tank.py
Tank(x, angle=45.0, power=55, hp=100, color=P1)
tank.muzzle() -> (x, y)               # نقطة فوهة المدفع (rotate)
tank.take_damage(amount)

# world/physics.py
step_projectile(p, wind, dt=1.0)      # پعدّل p.x, p.y, p.vx, p.vy
hits_terrain(p, terrain) -> bool

# world/weapons.py
fire(kind, tank, state) -> Projectile | None
# kind: "shell" | "laser" | "rocket"(stretch)

# game/state.py
GameState(terrain)                    # phase, turn, wind, tanks[2], projectile, winner
state.update(keys)                    # or however Task 3 wants; it owns main.py
state.draw(cv)                        # dynamic layer only
```

---

## 4. شكل البيانات

```python
Terrain.heights : list[int]   # len = WIDTH، heights[x] = y السطح
Tank            : x, angle, power, hp, color, weapon
Projectile      : x, y, vx, vy, kind, alive
GameState       : phase ("menu" | "aim" | "flying" | "boom" | "over"), turn(0|1), wind, ...
```

- الارتفاع لكل عمود هو مصدر الحقيقة الوحيد للأرض. مفيش صور.
- التصادم: `terrain.is_solid(x, y)` — O(1).
- الانفجار: `terrain.carve(cx, cy, r)` → إعادة بناء الـ polygon → `render` مرة واحدة → `snapshot`.

---

## 5. ممنوعات (هتتفحص بـ grep قبل أي merge)

```bash
grep -rn "pygame.draw\|gfxdraw\|\.set_at(\|transform.rotate\|smoothscale" --include=*.py .
```

- ممنوع `pygame.draw.*` أو `gfxdraw` أو `Surface.set_at`.
- ممنوع `pygame.transform.rotate` للدبابات — استخدم `core/util.rotate`.
- `pygame.transform.scale` مسموح **بس** في `core/display.py` لتكبير البافر.
- ممنوع `import pygame` في `algo/` أو `world/terrain.py` أو `core/canvas.py`.
- ممنوع منطق لعبة في `algo/` (مفيش HP ولا أدوار ولا أسلحة هناك).
- **استثناء واحد:** النص عبر `pygame.font` في `core/display.py`.

---

## 6. قواعد الكود

- **الأرقام المشتركة** في `config.py` بس. أي رقم سحري جديد في موديولك يبقى محلي وprivate.
- **أسماء:** `snake_case` للدوال والمتغيرات، `CapWords` للكلاسات.
- كل دالة عامة ليها **docstring سطرين**: إيه بتعمل + من أنهي chapter.
- مفيش `print` في الكود النهائي (الـ debug بيتشال قبل الـ PR).
- مفيش دالة بتعدّل canvas بره `cv.*` — يعني مفيش `cv.buf[i] = ...` من بره `canvas.py`.

## 7. "خلصت الموديول" معناها إيه

1. التوقيع مطابق للعقد.
2. فيه test في `tests/` وبيعدي: `python -m unittest discover -s tests -t .`
3. فيه لقطة أو ديمو صغير يبينه شغال.
4. سطرين في `docs/REPORT.md`: الخوارزمية + تعقيدها + فين بتظهر.
5. `grep` الممنوعات رجع صفر.

## 8. ملكية الملفات

| المسار | المالك |
|---|---|
| `config.py` | Task 3 (أي تغيير بيتمر عليه) |
| `core/`, `algo/lines.py`, `algo/circles.py`, `tests/` | Task 1 |
| `algo/curves.py`, `algo/fill.py`, `world/terrain.py` | Task 2 |
| `main.py`, `game/`, `world/physics.py`, `world/weapons.py` | Task 3 |
| `ui/`, `assets/`, `docs/REPORT.md`, العرض | Task 4 |
| `docs/CONTRACT.md`, `PLAN.md` | قائد الفريق + Task 3 |

محتاج تغيير في ملف مش بتاعك؟ اطلبه في الجروب. متعدلوش.
