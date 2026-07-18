<!-- rtl-normalized -->
<div dir="rtl" align="right">

# Agile Delivery Evidence

این سند برای پاسخ مستقیم به نقد TA تهیه شده است: پروژه نباید فقط یک کار فنی یا ML دیده شود؛ باید نشان دهد تیم چگونه با رویکرد Agile کار کرده، هر Sprint چه خروجی قابل تحویل داشته، چه کسی مسئول چه کاری بوده، و مسیر دریافت بازخورد کاربر چگونه طراحی شده است.

## Tooling واقعی پروژه

| نیاز ارزیابی | ابزار/بستر پروژه | وضعیت |
|---|---|---|
| مدیریت کار، backlog و sprint | GitHub Issues + فایل import آماده در `docs/artifacts/github-issues-seed.csv` | آماده برای مشاهده/انتقال به GitHub Projects |
| مدیریت دانش | پوشه `docs/knowledge-base/` و اسناد رسمی Word | آماده |
| مستندسازی تصمیم‌ها | `docs/decision-log.md` و `docs/knowledge-base/technical-decisions.md` | آماده |
| ثبت بازخورد ذی‌نفع | فرم بازخورد داخل MVP + `docs/knowledge-base/stakeholder-feedback-log.md` | آماده برای جمع‌آوری واقعی |
| ردیابی KPI و Burndown | `docs/agile-dashboard.md` و `docs/artifacts/` | آماده |

## Sprintها و Deliverableها

| Sprint | بازه | هدف | Deliverable قابل تحویل | معیار Done |
|---|---|---|---|---|
| Sprint 0 | 2026-06-01 | تعریف مسئله، pivot و ارزش اجتماعی | scope change record، stakeholder register، project idea | مسئله و ارزش انسانی قابل دفاع شد |
| Sprint 1 | 2026-06-02 تا 2026-06-03 | baseline مدل و کنترل leakage | مدل اولیه، انتخاب فیچرهای triage-time، گزارش ریسک leakage | مدل بدون داده post-triage اجرا شد |
| Sprint 2 | 2026-06-04 تا 2026-06-05 | API و MVP اولیه | FastAPI، endpointهای `/health` و `/predict`، سناریوی sparse | API با ورودی ناقص پاسخ داد |
| Sprint 3 | 2026-06-06 تا 2026-06-08 | مدل v6 و explainability | metrics v6، model card، safety-first threshold | Recall هدف 0.92 پاس شد |
| Sprint 4 | 2026-06-09 تا 2026-06-10 | UI موبایل و package تحویل | PWA، UI فارسی، Word deliverables، poster placeholder | MVP قابل demo و نصب موبایل شد |
| Sprint 5 | 2026-06-13 تا 2026-06-16 | مدیریت پروژه و بازخورد ذی‌نفع | Knowledge Base، feedback form، feedback log، poster assets | مسیر پایلوت و شواهد مدیریتی آماده شد |
| Sprint 6 | 2026-06-20 تا 2026-06-22 | مدل v7، deploy عمومی و ابزارهای مدیریت پروژه | GitHub Pages PWA، QR موبایل، Jira import CSV، GitHub Knowledge CSV | محصول عمومی و evidence قابل انتقال به ابزار واقعی آماده شد |

## نگاشت نسخه‌ها به Sprint

| نسخه | Sprint | تغییر اصلی | خروجی قابل دفاع |
|---|---|---|---|
| v2 | Sprint 1 | baseline و کالیبراسیون اولیه | شناسایی مشکل FPR و calibration |
| v3 | Sprint 1 | تلاش برای تنظیم XGBoost | ثبت درس‌آموخته افت عملکرد |
| v4 | Sprint 2 | حذف calibration و ensemble | بهبود مسیر مدل و API-ready شدن |
| v5 | Sprint 3 | فیچرهای بالینی و SHAP-oriented | گزارش مدل و پوستر اولیه |
| v6 | Sprint 3 | اصلاح دما، سوابق EHR-safe و missingness | AUC 0.8947 و Recall 0.9241 |
| v6 mobile/PWA | Sprint 4 | safety-first hybrid و UI موبایل | MVP قابل استفاده با داده ناقص |
| v7 webapp | Sprint 6 | featureهای بالینی جدید، کاهش FPR و deploy عمومی | AUC 0.9041، Recall 0.9246، FPR 0.3352 |

## نقش‌های واقعی و قابل ارائه

| عضو | نقش در پروژه | کارهای ساده و قابل توضیح در ارائه |
|---|---|---|
| محمدامین پورمند | Project Lead / ML & System Architect | توضیح معماری، مدل، API، کنترل leakage، trade-off Recall/FPR |
| محمدرضا آرمان پور | Project Control & Stakeholder/KPI Coordinator | توضیح KPIها، risk register، burndown، ارزش اجتماعی و برنامه جمع‌آوری بازخورد |
| محدثه حاتمی کیا | UI/Documentation & QA Coordinator | توضیح UI موبایل، سناریوهای تست، خوانایی خروجی، مستندات و QA |

## Backlog قابل انتقال به Jira

فایل `docs/artifacts/jira-import-issues.csv` شامل Epic، Story و Taskهای آماده برای import در Jira است. این فایل ستون‌های assignee، sprint، story point، original estimate، time spent، priority، label و evidence link دارد.

اگر بخواهید دستی انجام دهید:

1. در Jira یک پروژه Scrum با نام `امداد یار - Emergency Decision Support` بسازید.
2. فایل `docs/artifacts/jira-import-issues.csv` را import کنید.
3. ستون‌های `Backlog`, `Selected for Sprint`, `In Progress`, `Review/QA`, `Done` را بسازید.
4. برای هر issue، assignee، sprint، story point و time tracking را بررسی کنید.

## Knowledge Base قابل انتقال به GitHub Project

فایل `docs/artifacts/github-project-knowledge-items.csv` شامل آیتم‌های مدیریت دانش است: Sprint Notes، Meeting Notes، Technical Decisions، Stakeholder Feedback، AI Usage، Risk Register و KPI Register. این آیتم‌ها باید در یک GitHub Project یا Wiki به فایل‌های اصلی repository لینک شوند.

اگر استاد پرسید چرا screenshot واقعی هنوز در فایل نیست، پاسخ دفاعی:

> برای جلوگیری از جعل evidence، screenshot واقعی فقط پس از ساخت board با حساب کاربری گرفته می‌شود. در repository فایل‌های import، مستند راهنما، time tracking، backlog، Sprintها و evidence linkها آماده‌اند و قابل انتقال مستقیم به Jira/GitHub Project هستند.

## بازخورد ذی‌نفع و ادامه پایلوت

۹ بازخورد کیفی پرستاران تریاژ در ۱۲ ژوئیه ۲۰۲۶ تأیید و به اقدام‌های محصولی متصل شد. جزئیات بدون اطلاعات هویتی در `docs/triage-nurse-feedback-confirmation.md` ثبت شده است. این شواهد برای کاربردپذیری ارزشمند است، اما اعتبارسنجی بالینی محسوب نمی‌شود.

مرحله بعدی، پایلوت کمی با حداقل ۵ کاربر جدید و ثبت امتیازهای ۱ تا ۵ برای وضوح رابط، وضوح خروجی و مرز اخلاقی سامانه است.

چهار سؤال اصلی همان فرم داخل MVP است:

1. آیا خروجی سیستم قابل فهم بود؟
2. آیا UI سریع و واضح بود؟
3. آیا مشخص بود سیستم جایگزین پزشک نیست؟
4. مهم‌ترین پیشنهاد بهبود چیست؟

نتیجه بازخوردهای تأییدشده و برنامه پایلوت بعدی در `docs/knowledge-base/stakeholder-feedback-log.md` ثبت شده است.
</div>
