<!-- rtl-normalized -->
<div dir="rtl" align="right">

# Quality Assurance Plan

## هدف QA

اطمینان از اینکه MVP برای ارائه کلاسی قابل اجرا، قابل توضیح و مطابق با rubric استاد است.

## محدوده QA

- مدل ML
- API
- UI
- مستندات
- پوستر
- ویدئو و گزارش نهایی

## تست‌های انجام‌شده

| تست | ورودی/روش | نتیجه |
|---|---|---|
| Python compile | `py_compile` روی فایل‌های backend و ML | Pass |
| API health | `GET /health` | Pass |
| model info | `GET /model-info` | version = v6 |
| سناریوی sparse | chestpain، age، HR، SpO2، history | خروجی با confidence medium |
| سناریوی بحرانی | تنگی نفس، SpO2 پایین، shock index بالا | خروجی critical |
| کنترل leakage | بررسی featureهای مجاز | labs/meds/imaging/disposition حذف |
| مستندات rubric | checklist مادر | پوشش کامل موارد اصلی |

## سناریوهای Demo

| سناریو | هدف | انتظار |
|---|---|---|
| بیمار بحرانی تنفسی | نشان دادن هشدار فوری | critical |
| بیمار متوسط با تب | نشان دادن خروجی غیر بحرانی یا کم‌ریسک‌تر | non-critical/moderate |
| ورودی ناقص | اثبات کار با 3-4 آیتم | خروجی + data completeness |
| سالمند با درد قفسه سینه | نمایش اثر سن و شکایت اصلی | critical/high probability |
| بیمار با سابقه COPD/CHF | نمایش اثر history conditions | افزایش ریسک |

## معیار پذیرش تحویل

- README لینک همه artefactها را داشته باشد.
- گزارش نهایی scope، risk، decision، team dynamics و roadmap را پوشش دهد.
- پوستر KPI، burndown، team matrix و user acquisition داشته باشد.
- ویدئو کمتر از ۱۰ دقیقه و با حضور هر سه عضو باشد.
- board واقعی قبل از تحویل ساخته شود یا حداقل ساختار کامل آن آماده باشد.

## ریسک‌های QA

| ریسک | کنترل |
|---|---|
| اجرای نشدن server هنگام demo | آماده کردن screenshot و سناریوهای از قبل تست‌شده |
| سوال استاد درباره topic اولیه Sheet1 | استفاده از `scope-change-record.md` |
| سوال درباره کاربرد بالینی | تاکید بر decision-support و نیاز به validation |
| سوال درباره false positives | توضیح trade-off safety-first و balanced mode |
</div>
