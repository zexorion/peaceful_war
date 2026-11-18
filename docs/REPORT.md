# REPORT — تقرير المشروع

> **القاعدة:** كل تاسك بيكتب سطره هنا أول ما يخلص موديول. التقرير بيتجمع طول الأسبوعين، مش آخر يوم.
> كل خوارزمية: الفكرة في سطرين · التعقيد · فين بتظهر في اللعبة · لقطة.

## 1. الهدف

لعبة مدفعية turn-based، كل بكسل فيها بيتكتب بخوارزميات IT311. الهدف إثبات الفهم مش استخدام مكتبة رسم.

## 2. المعمارية

```
Input → Game Core (state: terrain, tanks, projectile)
      → Algorithms (pure modules: coordinates + color in, pixels out)
      → Canvas (bytearray + set_pixel)
      → Display (pygame: upscale + text)
```

- `Canvas` هي الطبقة الوحيدة اللي بتكتب بكسل.
- `algo/*` فيها صفر منطق لعبة ومفيش `import pygame`.
- الأداء: الخلفية بتترسم مرة وتتحفظ بـ `snapshot`، والتضاريس بتتعاد مرة واحدة بعد كل انفجار.

## 3. خريطة الخوارزميات

| # | Ch | الخوارزمية | الملف | فين بتظهر | الحالة |
|---|---|---|---|---|---|
| 1 | 2 | Direct line | `algo/lines.py` | مقارنة في الـ Lab | ⬜ |
| 2 | 2 | DDA | `algo/lines.py` | خط التصويب المنقّط | ⬜ |
| 3 | 2 | Bresenham | `algo/lines.py` | كل خط مستقيم | 🟡 |
| 4 | 3 | Midpoint Circle | `algo/circles.py` | الانفجار + القمر | ⬜ |
| 5 | 3 | Midpoint Ellipse | `algo/circles.py` | ظل الدبابة + HUD | ⬜ |
| 6 | 4 | Cubic Hermite | `algo/curves.py` | توليد التضاريس | ⬜ |
| 7 | 5 | Scan-line fill | `algo/fill.py` | التضاريس + الـ refill | ⬜ |
| 8 | 5 | Gradient | `algo/fill.py` | السما + التربة | ⬜ |
| 9 | 6 | Point clipping | `core/canvas.py` | حدود الشاشة | 🟡 |
| 10 | 7 | Rotate / Translate | `core/util.py` | المدفع + الاهتزاز | 🟡 |
| 11 | 4 | Bezier (stretch) | `algo/curves.py` | الصاروخ الموجّه | ⬜ |
| 12 | 5 | Flood fill (stretch) | `algo/fill.py` | سلاح المياه | ⬜ |

## 4. تفاصيل كل خوارزمية

### 4.x — (اسم الخوارزمية) — Ch?
- **الفكرة:**
- **التعقيد:** O(...)
- **في اللعبة:**
- **لقطة:** `docs/shots/...`
- **كتبها:**

> كرّر البلوك لكل خوارزمية.

## 5. مقارنة الأداء (Algorithms Lab)

| الخوارزمية | العملية | عدد البكسلات | الزمن (ms) | ملاحظات |
|---|---|---|---|---|
| Direct | خط 400px | | | |
| DDA | خط 400px | | | |
| Bresenham | خط 400px | | | |
| Midpoint | دايرة r=40 | | | |
| Polar | دايرة r=40 | | | |

## 6. ما تم استبعاده ولماذا

| العنصر | السبب |
|---|---|
| Sutherland–Hodgman | الشاشة ثابتة، مفيش camera/viewport |
| Window→Viewport + Minimap | نفس السبب |
| Ch8 / Ch9 / Ch11 | 3D و VR — مالهمش علاقة بلعبة 2D |
| أسلحة إضافية | كل سلاح = يوم شغل؛ الاتنين الأساسيين بيغطوا الـ scope |

## 7. جدول المساهمة

| العضو | Task | الملفات | الخوارزميات | نسبة |
|---|---|---|---|---|
| | 1 | | | |
| | 2 | | | |
| | 3 | | | |
| | 4 | | | |

## 8. اللقطات

`docs/shots/` — menu · aim · flight · explosion · crater · refill · HUD · lab · win.
