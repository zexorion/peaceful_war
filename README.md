# Peaceful War

لعبة مدفعية **turn-based** زي Pocket Tanks / Tank Stars: دبابتين على تضاريس، تظبيط زاوية وقوة، إطلاق، حفر، ضرر.
وكل بكسل على الشاشة بيتكتب بخوارزميات الكتاب (IT311) — مفيش `pygame.draw.*` ولا أي دالة رسم جاهزة.

**الفريق:** 8 أفراد · **المدة:** أسبوعين · **التقنية:** Python + pygame-ce (نافذة/إدخال/توقيت/نص فقط)

---

## التشغيل

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

- `F11` فولسكرين · `ESC` خروج · `←/→` تصويب (في الـ Slice 0).
- لقطة من غير نافذة: `.venv/bin/python main.py --shot out/slice0.png`
- الاختبارات: `.venv/bin/python -m unittest discover -s tests -t .`

> **الوضع الحالي: Slice 0 (هيكل شغال).** النافذة + Canvas + تضاريس + دبابتين + HUD.
> مش اللعبة بعد — دي نقطة البداية اللي كل تاسك هيبني عليها. شوف [PLAN.md](PLAN.md).

---

## الهيكل

```
config.py            كل الأرقام والألوان المشتركة (مصدر واحد)
core/
  canvas.py          الـ bytearray والـ set_pixel — الطبقة الوحيدة اللي بتكتب بكسل
  display.py         pygame: النافذة، التكبير، الفولسكرين، النص
  util.py            clamp / lerp / rotate
algo/
  lines.py           Ch2 — Bresenham فقط (Direct + DDA + المنقّط: Task 1)
  circles.py         Ch3 — فاضي عمدًا: Task 1 بيكتبه كله
  curves.py          Ch4 — يبدأ فاضي (Task 2)
  fill.py            Ch5 — يبدأ فاضي (Task 2)
world/
  terrain.py         heightmap + render (+ carve لاحقًا)
  physics.py         (Task 3)
  weapons.py         (Task 3)
game/                (Task 3)
ui/                  (Task 4)
tests/               unittest لكل موديول
assets/              خطوط/أيقونات/لقطات
docs/
  CONTRACT.md        العقد التقني بين الفرق — يُقرأ قبل أي كود
  TASKS.md           تقسيم الشغل 4×2 بالتفصيل
```

## مين بيملك إيه

| المجلد | Task |
|---|---|
| `core/`, `algo/lines.py`, `algo/circles.py`, `tests/` | 1 — Engine |
| `algo/curves.py`, `algo/fill.py`, `world/terrain.py` | 2 — Terrain |
| `main.py`, `game/`, `world/physics.py`, `world/weapons.py` | 3 — Core |
| `ui/`, `assets/`, `docs/` | 4 — UI/UX |

## المستندات

- **[PLAN.md](PLAN.md)** — القرارات، الـ scope، التقسيم، الجدول، المخاطر.
- **[docs/TASKS.md](docs/TASKS.md)** — ورق كل تاسك (يتنسخ للجروب زي ما هو).
- **[docs/CONTRACT.md](docs/CONTRACT.md)** — التوقيعات وقواعد الكود. **إلزامي.**

## القاعدة الذهبية

`Canvas` بس هي اللي بتكتب بكسل. الـ algorithms مالهاش أي منطق لعبة. واللعبة عمرها ما بتنادي رسم مباشر.
النص هو الاستثناء الوحيد المتفق عليه (خط جاهز عبر `pygame.font`).
