# AGENTS.md — قواعد الشغل في الريبو

اقرأ بالترتيب: [`docs/TEAM.md`](docs/TEAM.md) → [`PLAN.md`](PLAN.md) → [`docs/CONTRACT.md`](docs/CONTRACT.md) → [`docs/TASKS.md`](docs/TASKS.md).

## الحالة

**Slice 0** — نافذة + Canvas + تضاريس مؤقتة + دبابتين + HUD. اللعبة الحقيقية لسه.

## أوامر

```bash
.venv/bin/python main.py                                  # تشغيل
.venv/bin/python main.py --shot out/slice0.png            # لقطة headless
.venv/bin/python -m unittest discover -s tests -t .       # تستات
```

## قواعد إلزامية

1. **ملكية الملفات:** متعدّلش ملف مش بتاعك. لو محتاج تغيير في `config.py` أو العقد، اطلبه.
2. **ممنوع** `pygame.draw.*` · `gfxdraw` · `Surface.set_at` · `transform.rotate` · `smoothscale`.
   الفحص: `grep -rn "pygame.draw\|gfxdraw\|set_at(\|transform.rotate\|smoothscale" --include=*.py .`
3. **ممنوع `import pygame`** في `core/canvas.py`, `algo/*`, `world/terrain.py`.
4. **صفر منطق لعبة في `algo/`** — إحداثيات ولون داخل، بكسلات خارج.
5. **مفيش سحر أرقام** — الأرقام المشتركة في `config.py`.
6. **كل موديول = تست + سطرين في `docs/REPORT.md`.**
7. **`main` لازم تشتغل.** أي merge بيكسرها يترجع فورًا.

## دورة التنفيذ

UNDERSTAND → INSPECT (اقرأ الكود الموجود) → PLAN → EXECUTE → VERIFY (تشغيل حقيقي + تست) → REPORT.

- مفيش ادعاء إن حاجة شغالة من غير دليل (تشغيل/لقطة/تست).
- 3 محاولات فاشلة لنفس المشكلة = توقف، افحص السبب، اقترح 3 بدائل.
- الـ fallback قبل الجمال: أي خوارزمية ليها نسخة أبسط شغالة.

## عند إغلاق الجلسة

1. `git status` + `git diff --stat`.
2. اكتب ملخص في `docs/REPORT.md` لو فيه موديول خلص.
3. حدّث `PLAN.md` لو فيه قرار اتغير.
