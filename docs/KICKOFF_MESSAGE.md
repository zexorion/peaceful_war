# رسالة الـ kickoff (واتساب / تيليجرام)

> انسخ النص اللي تحت، وعدّل مكان `[اليوم والوقت والمكان]`.

---

🎮 *مشروع Computer Graphics — Peaceful War*

لعبة دبابات دور ورا دور: تظبط الزاوية والقوة، تطلق، القذيفة تنفجر وتحفر الأرض وتنقص HP.
والشرط الأساسي: *كل بكسل على الشاشة مكتوب بخوارزميات من الكتاب* — ممنوع أي دالة رسم جاهزة.

*١) شغّلوا المشروع*

▸ *ويندوز (PowerShell أو CMD):*
```
git clone https://github.com/zexorion/peaceful_war.git
cd peaceful_war
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```
(لو `py` مش موجود استخدم `python` بدالها — ومش محتاج تفعّل الـ venv)

▸ *لينكس / ماك:*
```
git clone https://github.com/zexorion/peaceful_war.git
cd peaceful_war
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

▸ *لقطة + تست (ويندوز):*
```
.venv\Scripts\python.exe main.py --shot out\slice0.png
.venv\Scripts\python.exe -m unittest discover -s tests -t .
```

*٢) اقرأوا بالترتيب*
1. docs/TEAM.md — دليل الفريق كامل (ابدأ من هنا)
2. docs/CONTRACT.md — العقد التقني (إلزامي قبل أي كود)
3. PLAN.md — القرارات والجدول

*٣) اللي هتشوفوه إيه*
ماكيت (Slice 0) — الشاشة والرسم شغالين، بس مفيش لعب لسه.
جاهز: الورقة والقلم + خط واحد (Bresenham) + تضاريس مؤقتة + HUD.
ناقص: الدواير (القمر/الانفجار) + DDA + الفيزياء + الأدوار + الحفر + الشاشات.

*٤) الشغل ٤ تاسكات × ٢*
▸ Task 1 — أدوات الرسم: Canvas + الخطوط + الدواير
▸ Task 2 — الأرض: المنحنيات + التلوين + الحفر
▸ Task 3 — اللعبة: الأدوار + الفيزياء + الانفجار + الدمج
▸ Task 4 — الشكل والتقرير: الشاشات + الـ HUD + التقرير + العرض

*٥) قواعد*
- كل تاسك ليه فولدر — محدش يعدّل فولدر حد تاني.
- ممنوع `pygame.draw` أو أي رسم جاهز.
- مفيش شغل على `main` — كل تاسك على branch.
- أي حد واقف أكتر من ساعتين يسأل هنا.
- التوزيع في الـ kickoff (٣٠ دقيقة)، مش دلوقتي.

*٦) الاجتماع*
[اليوم والوقت والمكان]
هنشغّل اللعبة قدامكم، ونوزّع التاسكات، ونبدأ.

الكتاب: الفصول 2 · 3 · 4 · 5
الريبو: https://github.com/zexorion/peaceful_war
