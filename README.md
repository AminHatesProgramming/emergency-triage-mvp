<!-- rtl-normalized -->
<div dir="rtl" align="right">

# امداد یار

سامانه هوشمند ارزیابی اولیه و اولویت‌بندی در شرایط اورژانسی

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
- نسخه Android آفلاین: `APK` و `AAB` امضاشده با شناسه `ir.pourmand.emdadyar`
- پشتیبانی از ورودی ناقص؛ حداقل یک شکایت اصلی یا علامت حیاتی لازم است
- آستانه validationمحور برای الگوهای سه و چهار ورودی پرکاربرد؛ بدون تغییر احتمال خام مدل
- خروجی ترکیبی شامل احتمال خام مدل، سطح فوریت مستقل، دلیل هشدار و اقدام پیشنهادی
- لایه ایمنی سن‌محور برای مقادیر دور از محدوده، همراه با هشدار تکرار اندازه‌گیری
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

برای ورودی ناقص، الگوی «شکایت + ضربان + SpO2» روی test به AUC=`0.8159` و Recall=`0.9411` و الگوی چهارفیلدی همراه سن به AUC=`0.8356` و Recall=`0.9246` رسید. این حالت‌ها FPR بالاتری دارند و با برچسب محدودیت داده استفاده می‌شوند. آستانه پیشنهادیِ «فقط علائم حیاتی» به دلیل FPR=`0.7840` رد و وارد محصول نشد.

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

اسکریپت، آدرس‌های LAN مثل `http://192.168.x.x:8000/` را چاپ می‌کند. نصب PWA از مرورگر به HTTPS نیاز دارد؛ نسخه Android بازار، وب‌اپ و مدل را داخل بسته نگه می‌دارد و برای ارزیابی آفلاین به سرور وابسته نیست.

## لینک عمومی وب‌اپ

نسخه عمومی روی GitHub Pages با این آدرس در دسترس است:

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

توجه: داده خام در Git نگهداری نمی‌شود. artifact سبک و نهایی `models/triage_model_v7.pkl` برای بازتولید inference در مخزن وجود دارد؛ مدل‌های حجیم قدیمی جزو تحویل نیستند.

## Endpointها

- `GET /health`
- `GET /model-info`
- `POST /predict`
- `GET /`

## مستندات کلیدی

- [هسته بسته تحویل، آماده افزودن شواهد واقعی Jira/Notion](Emdadyar_Submission_Core_Ready_For_Platform_Evidence.zip)
- [فهرست رسمی تحویل نهایی](docs/final-submission-index.md)
- [خروجی‌های رسمی Word برای تحویل](docs/deliverables/README.md)
- [گزارش نهایی Word](docs/deliverables/ITPM_Final_Report_Emergency_Triage.docx)
- [بسته شواهد مدیریت پروژه Word](docs/deliverables/ITPM_Project_Management_Evidence_Package.docx)
- [سناریوی نهایی ارائه ۱۰ دقیقه‌ای](docs/deliverables/Emdadyar_Final_Presentation_Runbook.docx)
- [حاکمیت و مدیریت منابع پروژه](docs/deliverables/ITPM_Project_Governance_and_Resource_Management.docx)
- [ماتریس انطباق با اعلان نهایی](docs/deliverables/ITPM_Final_Announcement_Compliance_Matrix.docx)
- [فایل Word ارسال نسخه موبایل به استاد](docs/deliverables/Emdadyar_Mobile_App_For_Professor.docx)
- [بسته انتشار/مارکت امداد یار](docs/deliverables/Emdadyar_Market_Release_Package.zip)
- [معماری سیستم](docs/architecture.md)
- [یادداشت تکمیل نسخه موبایل و PWA](docs/mobile-pwa-completion-note.md)
- [راهنمای deploy وب‌اپ، موبایل و بازار اندرویدی](docs/deployment-mobile-webapp.md)
- [API Documentation](docs/api-documentation.md)
- [Model Card](docs/model-card.md)
- [ممیزی نهایی متریک‌های مدل v7](docs/model-final-metrics-audit.md)
- [ممیزی ۱۱۱٬۶۰۶ رکورد test و سناریوهای ناقص/مرزی](docs/model-release-scenario-audit-fa.md)
- [تحلیل UX با بازخوردهای شبیه‌سازی‌شده پیش از پایلوت](docs/ux-feedback-synthesis.md)
- [گزارش تأیید ۹ بازخورد پرستاران تریاژ](docs/triage-nurse-feedback-confirmation.md)
- [برنامه مدیریت پروژه](docs/project-management-plan.md)
- [Agile Delivery Evidence پس از بازخورد TA](docs/agile-delivery-evidence.md)
- [راهنمای عملیاتی‌سازی Jira و مدیریت دانش](docs/jira-github-project-import-guide.md)
- [بسته نهایی قابل ورود به Jira و Notion](project-management-final-package/README.md)
- [Knowledge Base پروژه](docs/knowledge-base/README.md)
- [تعریف و اعتبارسنجی لایه ایمنی سن‌محور](docs/knowledge-base/safety-layer-v1-fa.md)
- [Jira Import CSV](docs/artifacts/jira-import-issues.csv)
- [GitHub Knowledge Project CSV](docs/artifacts/github-project-knowledge-items.csv)
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
- [حاکمیت ابزارهای کمکی و کنترل انسانی](docs/ai-usage-report.md)
- [درس‌آموخته‌ها](docs/lessons-learned.md)
- [محتوای پوستر](docs/poster-content.md)
- [محتوای نهایی آماده برای پوستر](poster-final-assets-fa.md)
- [اسکریپت ویدئوی نهایی](docs/video-presentation-script.md)
- [ساختار board مدیریت کار](docs/work-management-board.md)
- [ساختار مدیریت دانش](docs/knowledge-management-index.md)
- [بسته انتشار Android و راهنمای بازار](docs/market/README.md)
- [فایل APK امضاشده امداد یار 1.0.0](docs/market/release/Emdadyar-1.0.0-release.apk)
- [فایل AAB امضاشده امداد یار 1.0.0](docs/market/release/Emdadyar-1.0.0-release.aab)
- [ZIP یکپارچه انتشار Android 1.0.0](docs/market/Emdadyar_Android_Market_Release_1.0.0.zip)

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
| محدثه حاتمی کیا | UI/Documentation & QA Coordinator |
| محمدرضا آرمان‌پور | Project Control & Metrics Coordinator |

## هشدار اخلاقی

این پروژه آموزشی است و خروجی آن فقط برای پشتیبانی تصمیم طراحی شده است. استفاده واقعی نیازمند داده بیمارستانی معتبر، تایید متخصص، بررسی محرمانگی و ارزیابی نهادی است.
</div>
