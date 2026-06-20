# سیستم هوشمند پشتیبان تصمیم‌گیری تریاژ اورژانس

پروژه درس مدیریت پروژه فناوری اطلاعات

## خلاصه

این پروژه یک MVP برای کمک به تریاژ اورژانس است. سامانه با دریافت اطلاعات قابل دسترسی در لحظه تریاژ، احتمال بحرانی بودن بیمار را تخمین می‌زند و به صورت decision-support خروجی می‌دهد. سیستم جایگزین پزشک، پرستار یا پروتکل رسمی نیست.

تمرکز پروژه روی ارزش انسانی است: کاهش احتمال از دست رفتن بیمار بحرانی در شرایط ازدحام، بحران، کمبود منابع یا فشار کاری.

## وضعیت فعلی

- مدل نهایی: `v7`
- backend: FastAPI
- frontend: فارسی، راست‌به‌چپ و mobile-first
- PWA: قابل نصب روی موبایل با `manifest.webmanifest` و `service worker`
- نسخه public/static: قابل انتشار با GitHub Pages و دارای مدل v7 داخل مرورگر
- پشتیبانی از ورودی ناقص
- خروجی safety-first hybrid شامل `model_probability`، `safety_flags` و `next_best_actions`
- مستندات مدیریتی و فنی در `docs/`
- گزارش‌های مدل در `reports/model/`

## متریک‌های مدل v7

حالت عملیاتی انتخاب‌شده: `safety_first_mode`

| معیار | مقدار تست |
|---|---:|
| AUC | 0.9041 |
| Average Precision | 0.8202 |
| Recall | 0.9246 |
| Precision | 0.5447 |
| FPR | 0.3352 |
| Threshold | 0.3017 |

حالت جایگزین `balanced_fpr_mode` نیز در `reports/model/metrics_v7.json` ثبت شده است؛ در آن FPR برابر `0.2852` است و Recall به `0.9000` می‌رسد. حالت پیش‌فرض محصول همچنان `safety_first_mode` است.

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

اجرای قابل دسترسی از گوشی روی یک شبکه وای‌فای:

```powershell
.\scripts\start_public_webapp.ps1
```

اسکریپت، آدرس‌های LAN مثل `http://192.168.x.x:8000/` را چاپ می‌کند. برای نصب کامل PWA روی Android و انتشار در بازار، نسخه نهایی باید روی HTTPS deploy شود.

## لینک عمومی وب‌اپ

نسخه public روی GitHub Pages با این آدرس منتشر می‌شود:

```text
https://aminhatesprogramming.github.io/emergency-triage-mvp/
```

این نسخه بدون backend پایتونی هم کار می‌کند؛ مدل v7 به فایل `frontend/model-v7.json` تبدیل شده و prediction داخل مرورگر/گوشی اجرا می‌شود. اگر backend جدا deploy شود، همین UI به endpointهای FastAPI وصل می‌شود.

برای ساخت خروجی GitHub Pages در local:

```powershell
C:\Users\Webhouse\Desktop\quera\qenv\Scripts\python.exe scripts\build_pages.py
```

اجرای Docker برای deploy:

```powershell
docker build -t emergency-triage-mvp .
docker run --rm -p 8000:8000 emergency-triage-mvp
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

- [خروجی‌های رسمی Word برای تحویل](docs/deliverables/README.md)
- [گزارش نهایی Word](docs/deliverables/ITPM_Final_Report_Emergency_Triage.docx)
- [بسته شواهد مدیریت پروژه Word](docs/deliverables/ITPM_Project_Management_Evidence_Package.docx)
- [راهنمای ارائه و تحویل Word](docs/deliverables/ITPM_Presentation_and_Submission_Guide.docx)
- [پیوست Word شواهد Agile و پاسخ به TA](docs/deliverables/ITPM_Agile_Evidence_Addendum.docx)
- [معماری سیستم](docs/architecture.md)
- [یادداشت تکمیل نسخه موبایل و PWA](docs/mobile-pwa-completion-note.md)
- [راهنمای deploy وب‌اپ، موبایل و بازار اندرویدی](docs/deployment-mobile-webapp.md)
- [API Documentation](docs/api-documentation.md)
- [Model Card](docs/model-card.md)
- [گزارش وضعیت](docs/status-report.md)
- [پیش‌نویس گزارش نهایی](docs/final-report-draft.md)
- [برنامه مدیریت پروژه](docs/project-management-plan.md)
- [Agile Delivery Evidence پس از بازخورد TA](docs/agile-delivery-evidence.md)
- [راهنمای عملیاتی‌سازی GitHub Projects و Notion](docs/tooling-operationalization-guide.md)
- [چک‌لیست تطبیق تحویل نهایی ۱۴۰۵/۰۳/۲۵](docs/final-submission-compliance-2026-06-15.md)
- [Knowledge Base پروژه](docs/knowledge-base/README.md)
- [Issue Seed برای GitHub Projects](docs/artifacts/github-issues-seed.csv)
- [تطبیق با معیارهای نمره‌دهی](docs/grading-rubric-alignment.md)
- [چک‌لیست مادر تحویل نهایی](docs/final-submission-master-checklist.md)
- [ماتریس همکاری و ثبت زمان](docs/team-collaboration-matrix.md)
- [داشبورد Agile و KPI](docs/agile-dashboard.md)
- [KPI Register](docs/kpi-register.md)
- [WBS و RACI](docs/wbs-raci.md)
- [Stakeholder Register](docs/stakeholder-register.md)
- [Decision Log](docs/decision-log.md)
- [Scope Change Record](docs/scope-change-record.md)
- [Quality Assurance Plan](docs/quality-assurance-plan.md)
- [Project Timeline](docs/project-timeline.md)
- [Roadmap](docs/roadmap.md)
- [Backlog و Sprintها](docs/backlog.md)
- [ثبت ریسک‌ها](docs/risk-register.md)
- [گزارش استفاده از AI](docs/ai-usage-report.md)
- [درس‌آموخته‌ها](docs/lessons-learned.md)
- [محتوای پوستر](docs/poster-content.md)
- [بخش تکمیلی پوستر برای Agile/Feedback](docs/poster-management-addendum.md)
- [پوستر A0 قابل چاپ](docs/poster/a0-poster.html)
- [طرح ارائه](docs/status-presentation-outline.md)
- [اسکریپت ویدئوی نهایی](docs/video-presentation-script.md)
- [ساختار board مدیریت کار](docs/work-management-board.md)
- [ساختار مدیریت دانش](docs/knowledge-management-index.md)

## نمودارها و داده‌های مدیریتی

- [Burndown SVG](docs/artifacts/burndown.svg)
- [Burndown Data](docs/artifacts/burndown-data.csv)
- [Velocity SVG](docs/artifacts/velocity.svg)
- [Velocity Data](docs/artifacts/velocity-data.csv)
- [User Acquisition SVG](docs/artifacts/user-acquisition.svg)
- [User Acquisition Data](docs/artifacts/user-acquisition-data.csv)

## اعضای تیم

| عضو | نقش |
|---|---|
| محمدامین پورمند | Project Lead / ML & System Architect |
| محمدرضا آرمان پور | Project Control & Metrics Coordinator |
| محدثه حاتمی کیا | UI/Documentation & QA Coordinator |

## هشدار اخلاقی

این پروژه آموزشی است و خروجی آن فقط برای پشتیبانی تصمیم طراحی شده است. استفاده واقعی نیازمند داده بیمارستانی معتبر، تایید متخصص، بررسی محرمانگی و ارزیابی نهادی است.
