# سیستم هوشمند پشتیبان تصمیم‌گیری تریاژ اورژانس

پروژه درس مدیریت پروژه فناوری اطلاعات

## خلاصه

این پروژه یک MVP برای کمک به تریاژ اورژانس است. سامانه با دریافت اطلاعات قابل دسترسی در لحظه تریاژ، احتمال بحرانی بودن بیمار را تخمین می‌زند و به صورت decision-support خروجی می‌دهد. سیستم جایگزین پزشک، پرستار یا پروتکل رسمی نیست.

تمرکز پروژه روی ارزش انسانی است: کاهش احتمال از دست رفتن بیمار بحرانی در شرایط ازدحام، بحران، کمبود منابع یا فشار کاری.

## وضعیت فعلی

- مدل نهایی: `v6`
- backend: FastAPI
- frontend: فارسی، راست‌به‌چپ و mobile-first
- پشتیبانی از ورودی ناقص
- مستندات مدیریتی و فنی در `docs/`
- گزارش‌های مدل در `reports/model/`

## متریک‌های مدل v6

حالت عملیاتی انتخاب‌شده: `safety_first_mode`

| معیار | مقدار تست |
|---|---:|
| AUC | 0.8947 |
| Average Precision | 0.8034 |
| Recall | 0.9241 |
| Precision | 0.5269 |
| FPR | 0.3598 |
| Threshold | 0.2962 |

حالت جایگزین `balanced_fpr_mode` نیز در `reports/model/metrics_v6.json` ثبت شده است؛ در آن FPR برابر `0.3483` است اما Recall به `0.9190` می‌رسد.

## ورودی‌های مدل

مدل فقط از اطلاعات قابل دفاع در لحظه تریاژ استفاده می‌کند:

- سن، جنسیت و روش ورود
- علائم حیاتی اولیه
- شکایت اصلی
- سابقه مراجعه، بستری و جراحی
- سابقه‌های بالینی قابل پرسش یا قابل مشاهده در پرونده

مواردی مثل آزمایش، دارو، تصویربرداری، disposition و تشخیص‌های بعدی حذف شده‌اند تا leakage ایجاد نشود.

## اجرای پروژه

محیط اجرای پروژه `qenv` است.

```powershell
cd C:\Users\Webhouse\Desktop\quera\pm
C:\Users\Webhouse\Desktop\quera\qenv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

سپس مرورگر:

```text
http://127.0.0.1:8000/
```

آموزش دوباره مدل:

```powershell
C:\Users\Webhouse\Desktop\quera\qenv\Scripts\python.exe ml\train.py
```

توجه: فایل داده خام و فایل مدل آموزش‌دیده به دلیل حجم/حساسیت در Git نگهداری نمی‌شوند.

## Endpointها

- `GET /health`
- `GET /model-info`
- `POST /predict`
- `GET /`

## مستندات کلیدی

- [معماری سیستم](docs/architecture.md)
- [Model Card](docs/model-card.md)
- [گزارش وضعیت](docs/status-report.md)
- [پیش‌نویس گزارش نهایی](docs/final-report-draft.md)
- [برنامه مدیریت پروژه](docs/project-management-plan.md)
- [تطبیق با معیارهای نمره‌دهی](docs/grading-rubric-alignment.md)
- [ماتریس همکاری و ثبت زمان](docs/team-collaboration-matrix.md)
- [داشبورد Agile و KPI](docs/agile-dashboard.md)
- [Backlog و Sprintها](docs/backlog.md)
- [ثبت ریسک‌ها](docs/risk-register.md)
- [گزارش استفاده از AI](docs/ai-usage-report.md)
- [درس‌آموخته‌ها](docs/lessons-learned.md)
- [محتوای پوستر](docs/poster-content.md)
- [طرح ارائه](docs/status-presentation-outline.md)
- [اسکریپت ویدئوی نهایی](docs/video-presentation-script.md)
- [ساختار board مدیریت کار](docs/work-management-board.md)
- [ساختار مدیریت دانش](docs/knowledge-management-index.md)

## اعضای تیم

| عضو | نقش |
|---|---|
| محمدامین پورمند | Project Lead / ML & System Architect |
| محمدرضا آرمان پور | Project Control & Metrics Coordinator |
| محدثه حاتمی کیا | UI/Documentation & QA Coordinator |

## هشدار اخلاقی

این پروژه آموزشی است و خروجی آن فقط برای پشتیبانی تصمیم طراحی شده است. استفاده واقعی نیازمند داده بیمارستانی معتبر، تایید متخصص، بررسی محرمانگی و ارزیابی نهادی است.
