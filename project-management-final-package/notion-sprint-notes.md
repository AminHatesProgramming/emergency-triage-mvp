<!-- rtl: fa -->
<div dir="rtl" align="right">

# یادداشت‌های اسپرینت | امداد یار

این گزارش بر پایه تاریخچه مخزن، خروجی‌های تحویل، Jira و مستندات ثبت‌شده تهیه شده است. Deliverable، Evidence، تصمیم‌ها و کارهای باز هر مرحله به‌صورت قابل ردیابی ارائه می‌شوند.

## Sprint 0: تعریف مسئله و محدوده

| بخش | توضیح |
|---|---|
| Goal | انتخاب مسئله سلامت‌محور، تعریف ارزش انسانی، ذی‌نفعان و مرز اخلاقی MVP |
| Tasks | تعریف مسئله، کاربران هدف، نقش decision-support، دامنه و ارزش اجتماعی |
| Deliverables | <span dir="ltr">docs/project-management-plan.md</span>، <span dir="ltr">docs/stakeholder-register.md</span>، <span dir="ltr">docs/scope-change-record.md</span> |
| Risks | ادعای بیش از حد پزشکی، دامنه مبهم و نبود معیار قابل اندازه‌گیری |
| Decisions | تمرکز بر تریاژ اورژانس و ممنوعیت جایگزینی متخصص |
| Outcome | مسئله، محدوده، ذی‌نفع و هشدار اخلاقی ثبت شد |
| Jira | <span dir="ltr">EMD-2, EMD-11..EMD-15</span> |

## Sprint 1: داده و مدل

| بخش | توضیح |
|---|---|
| Goal | ساخت خط مبنا، کنترل data leakage و تعریف KPIهای مناسب سلامت |
| Tasks | انتخاب ویژگی‌های triage-time، جداسازی validation/test، آموزش نسخه‌ها و threshold tuning |
| Deliverables | <span dir="ltr">ml/train.py</span>، <span dir="ltr">docs/model-card.md</span>، <span dir="ltr">reports/model/metrics_v7.json</span> |
| Risks | leakage، FPR بالا، داده ناقص و وابستگی به داده غیر بومی |
| Decisions | گزارش همزمان AUC، Recall، Precision و FPR؛ اولویت Recall با شفافیت هزینه عملیاتی |
| Outcome | مدل v7 با AUC=0.9041 و Recall=0.9246 در test داخلی تثبیت شد |
| Jira | <span dir="ltr">EMD-3, EMD-16..EMD-20, EMD-57</span> |

## Sprint 2: Backend و تجربه کاربر

| بخش | توضیح |
|---|---|
| Goal | تبدیل مدل به محصول فارسی، ساده و قابل استفاده روی موبایل |
| Tasks | API، فرم، سناریوها، نتیجه قابل فهم، کامل بودن داده، PWA و QR |
| Deliverables | <span dir="ltr">backend/main.py</span>، <span dir="ltr">frontend/</span>، <span dir="ltr">docs/artifacts/emdadyar-pwa-qr.png</span> |
| Risks | شلوغی UI، اصطلاحات نامفهوم، ورودی اشتباه و وابستگی به local server |
| Decisions | فارسی RTL، نمونه‌های جدا از فرم، عبارت «اقدام بعدی» و انتشار GitHub Pages |
| Outcome | وب‌اپ عمومی و mobile-first بدون نیاز به سرور محلی منتشر شد |
| Jira | <span dir="ltr">EMD-4, EMD-5, EMD-21..EMD-30, EMD-51, EMD-52</span> |

## Sprint 3: ایمنی، بازخورد و مدیریت دانش

| بخش | توضیح |
|---|---|
| Goal | تکمیل شواهد مدیریت پروژه و اتصال توسعه فنی به بازخورد، ریسک و تصمیم‌های مستند |
| Tasks | safety/explainability، Knowledge Base، KPI، Risk، Burndown، حاکمیت ابزارهای کمکی و QA |
| Deliverables | <span dir="ltr">docs/knowledge-base/</span>، <span dir="ltr">docs/kpi-register.md</span>، <span dir="ltr">project-management-final-package/</span> |
| Risks | کم‌رنگ بودن همکاری تیمی، ناقص‌بودن شواهد ابزارها و ثبت بازخورد بدون منبع قابل تأیید |
| Decisions | تفکیک بازخورد تأییدشده از داده‌های آزمایشی و ثبت شفاف موارد باز |
| Outcome | ۹ بازخورد پرستار تأیید شد؛ Jira و Notion واقعی ساخته و لینک شدند |
| Jira | <span dir="ltr">EMD-6..EMD-9, EMD-31..EMD-50, EMD-59</span> |

## Final Release Sprint: ممیزی، Android و تحویل

| بخش | توضیح |
|---|---|
| Goal | آزمون سناریوهای مرزی، هم‌ارزی نسخه‌ها و تولید بسته قابل انتشار |
| Tasks | قواعد سن‌محور، held-out sparse validation، differential test، APK/AAB، docs و package |
| Deliverables | <span dir="ltr">reports/model/release_validation_v7.json</span>، <span dir="ltr">docs/model-release-scenario-audit-fa.md</span>، <span dir="ltr">docs/market/release/</span> |
| Risks | تلقی قواعد به‌عنوان پروتکل بالینی، FPR ورودی ناقص و مشکل دستگاه واقعی |
| Decisions | عدم دست‌کاری probability، رد core-vitals با FPR=0.784 و اجرای آفلاین Android |
| Outcome | ۱۱۸ تست Python، ۵۰۰۰ ترکیب بذرثابت، ۱۱۱۶۰۶ رکورد test و ۱۱۶۷ سناریوی browser/API عبور کردند |
| Open work | Burndown در EMD-43، Time Tracking در EMD-44، آزمون فیزیکی QR/PWA در EMD-52، تصاویر نهایی در EMD-55، تست دستگاه واقعی در EMD-60 و پیگیری مراکز درمانی در EMD-61 |
| Jira | <span dir="ltr">EMD-10, EMD-53..EMD-61</span> |

## Retrospective نهایی

- مهم‌ترین ارزش محصول، سادگی کار در فشار است؛ امکاناتی که شلوغی ایجاد می‌کردند از صفحه اصلی کنار گذاشته شدند.
- Accuracy به‌تنهایی معیار مناسبی نبود؛ Recall و FPR باید همزمان دیده شوند.
- داده ناقص به پروفایل اعتبارسنجی‌شده نیاز دارد؛ کاهش عمومی threshold قابل دفاع نیست.
- کنترل مهندسی با اعتبارسنجی بالینی یکسان نیست و این محدودیت در همه خروجی‌ها حفظ شد.
- ابزار مدیریت پروژه باید تاریخچه تصمیم و کار باز را نشان دهد، نه فقط فهرستی از موارد Done.

</div>
