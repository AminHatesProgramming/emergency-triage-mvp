<!-- rtl: fa -->
<div dir="rtl" align="right">

# امداد یار | دانشنامه پروژه و مدیریت دانش

## معرفی کوتاه

«امداد یار» یک سامانه هوشمند ارزیابی اولیه و اولویت‌بندی آسیب‌دیدگان در شرایط اورژانسی است. هدف محصول کمک به تصمیم‌گیری سریع‌تر در تریاژ، با تمرکز بر داده‌های قابل دسترس در لحظه ارزیابی اولیه است. این سامانه ابزار پشتیبان تصمیم است و جایگزین متخصص، پرستار تریاژ یا پروتکل رسمی درمانی نیست.

## مسئله

در محیط‌های شلوغ اورژانس، فشار زمانی، کمبود منابع و وابستگی زیاد به تجربه فردی می‌تواند باعث تأخیر در شناسایی بیمار پرخطر شود. پروژه تلاش می‌کند با یک MVP قابل اجرا، احتمال از دست رفتن بیمار بحرانی را کاهش دهد و همزمان محدودیت‌ها و مسئولیت اخلاقی را شفاف نگه دارد.

## راه‌حل

محصول از فرم فارسی و راست‌به‌چپ، نمونه‌های آماده تست، مدل v7، ارزیابی با ورودی ناقص، هشدارهای مهم، اقدام بعدی، خلاصه کیس، نصب PWA و لینک عمومی استفاده می‌کند. نسخه public روی GitHub Pages بدون نیاز به سرور local قابل باز شدن است.

## ارزش انسانی و اجتماعی

ارزش اصلی پروژه کاهش احتمال تأخیر در رسیدگی به بیمار پرخطر و ساخت یک نمونه بومی از کاربرد مسئولانه AI در سلامت است. توسعه محصول همراه با backlog، sprint، KPI، risk register، AI usage report، QA و پیگیری بازخورد انجام شده است.

## لینک‌های اصلی

| مورد | لینک / مسیر | وضعیت |
|---|---|---|
| اپ عمومی امداد یار | <span dir="ltr">https://aminhatesprogramming.github.io/emergency-triage-mvp/</span> | آماده |
| ریپازیتوری GitHub | <span dir="ltr">https://github.com/AminHatesProgramming/emergency-triage-mvp</span> | آماده |
| Jira Workspace | <span dir="ltr">https://pourmand.atlassian.net/jira/for-you</span> | موجود |
| Jira Project / Board | نیاز به تکمیل دارد: پس از ساخت پروژه در Jira لینک دقیق project/board را اینجا قرار دهید. | نیاز به تکمیل |
| Notion Home | نیاز به تکمیل دارد: پس از ساخت Workspace/Page در Notion لینک صفحه اصلی را اینجا قرار دهید. | نیاز به تکمیل |

## صفحات مهم Notion که باید ساخته شوند

| صفحه | فایل آماده انتقال |
|---|---|
| معرفی و دانشنامه اصلی | <span dir="ltr">project-management-final-package/notion-home.md</span> |
| نمای کلی پروژه | <span dir="ltr">project-management-final-package/notion-project-overview.md</span> |
| قابلیت‌های محصول | <span dir="ltr">project-management-final-package/notion-product-features.md</span> |
| Sprint Notes | <span dir="ltr">project-management-final-package/notion-sprint-notes.md</span> |
| Meeting Notes | <span dir="ltr">project-management-final-package/notion-meeting-notes.md</span> |
| AI Usage Report | <span dir="ltr">project-management-final-package/notion-ai-usage-report.md</span> |
| Lessons Learned | <span dir="ltr">project-management-final-package/notion-lessons-learned.md</span> |
| Decision Log Database | <span dir="ltr">project-management-final-package/notion-decision-log.csv</span> |
| Change Log Database | <span dir="ltr">project-management-final-package/notion-change-log.csv</span> |
| Risk Register Database | <span dir="ltr">project-management-final-package/notion-risk-register.csv</span> |
| Stakeholder Feedback Database | <span dir="ltr">project-management-final-package/notion-stakeholder-feedback.csv</span> |
| QA Test Log Database | <span dir="ltr">project-management-final-package/notion-qa-test-log.csv</span> |

## وضعیت فعلی پروژه

| بخش | وضعیت | شاهد |
|---|---|---|
| مدل عملیاتی | v7، AUC=0.9041، Recall=0.9246 | <span dir="ltr">reports/model/metrics_v7.json</span> |
| API | Endpointهای <span dir="ltr">/health</span>، <span dir="ltr">/model-info</span> و <span dir="ltr">/predict</span> | <span dir="ltr">backend/main.py</span> |
| UI | فارسی، راست‌به‌چپ، mobile-first، قابل نصب به شکل PWA | <span dir="ltr">frontend/index.html</span> |
| نسخه عمومی | GitHub Pages با مدل مرورگر | commit <span dir="ltr">a1ec91f</span> و <span dir="ltr">43737c8</span> |
| مستندات مدیریت پروژه | Sprint، KPI، Risk، Burndown، Evidence و Deliverables | <span dir="ltr">docs/</span> |
| حاکمیت و منابع | منابع انسانی/غیرانسانی، هزینه، ارتباطات، کیفیت و خاتمه MVP | <span dir="ltr">docs/project-governance-and-resource-management.md</span> |
| بازخورد ذی‌نفعان | ۹ بازخورد پرستار تریاژ تأیید و اثر آن‌ها بر نسخه نهایی ثبت شده است؛ دو درخواست ملاقات بیمارستانی در انتظار پاسخ نهایی است | <span dir="ltr">docs/triage-nurse-feedback-confirmation.md</span> و <span dir="ltr">docs/stakeholder-outreach-log.md</span> |
| نتیجه میدانی فعلی | ۱ وب‌اپ عمومی، ۹ بازخورد تخصصی، ۲ مرکز درمانی مخاطب، ۰ اعتبارسنجی بالینی | <span dir="ltr">docs/kpi-register.md</span> |

## اعضای تیم

| عضو | نقش |
|---|---|
| محمدامین پورمند | Project Lead / ML & System Architect |
| محدثه حاتمی کیا | UI / Documentation & QA Coordinator |
| محمدرضا آرمان‌پور | Project Control & Metrics Coordinator |

## هشدار اخلاقی

امداد یار خروجی تشخیصی قطعی تولید نمی‌کند. خروجی سامانه باید فقط به عنوان کمک تصمیم‌گیری اولیه تفسیر شود و تصمیم نهایی با متخصص، پرستار تریاژ و پروتکل رسمی مرکز درمانی است.
</div>

