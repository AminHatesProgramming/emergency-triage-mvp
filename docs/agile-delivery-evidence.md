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
| Sprint 5 | 2026-06-13 تا 2026-06-16 | مدیریت پروژه و بازخورد ذی‌نفع | GitHub Issues seed، Knowledge Base، feedback form، feedback log | حداقل 5 بازخورد واقعی جمع‌آوری شود |

## نگاشت نسخه‌ها به Sprint

| نسخه | Sprint | تغییر اصلی | خروجی قابل دفاع |
|---|---|---|---|
| v2 | Sprint 1 | baseline و کالیبراسیون اولیه | شناسایی مشکل FPR و calibration |
| v3 | Sprint 1 | تلاش برای تنظیم XGBoost | ثبت درس‌آموخته افت عملکرد |
| v4 | Sprint 2 | حذف calibration و ensemble | بهبود مسیر مدل و API-ready شدن |
| v5 | Sprint 3 | فیچرهای بالینی و SHAP-oriented | گزارش مدل و پوستر اولیه |
| v6 | Sprint 3 | اصلاح دما، سوابق EHR-safe و missingness | AUC 0.8947 و Recall 0.9241 |
| v6 mobile/PWA | Sprint 4 | safety-first hybrid و UI موبایل | MVP قابل استفاده با داده ناقص |
| v7 webapp | Sprint 6 | featureهای بالینی جدید، کاهش FPR و آماده‌سازی deploy | AUC 0.9041، Recall 0.9246، FPR 0.3352 |

## نقش‌های واقعی و قابل ارائه

| عضو | نقش در پروژه | کارهای ساده و قابل توضیح در ارائه |
|---|---|---|
| محمدامین پورمند | Project Lead / ML & System Architect | توضیح معماری، مدل، API، کنترل leakage، trade-off Recall/FPR |
| محمدرضا آرمان پور | Project Control & Stakeholder/KPI Coordinator | توضیح KPIها، risk register، burndown، ارزش اجتماعی و برنامه جمع‌آوری بازخورد |
| محدثه حاتمی کیا | UI/Documentation & QA Coordinator | توضیح UI موبایل، سناریوهای تست، خوانایی خروجی، مستندات و QA |

## Backlog قابل انتقال به GitHub Projects

فایل `docs/artifacts/github-issues-seed.csv` شامل issueهای آماده است. برای ساخت board واقعی، اسکریپت `scripts/setup_github_work_management.ps1` اضافه شده است.

اجرای پیشنهادی:

```powershell
winget install --id GitHub.cli
gh auth login
gh auth refresh -s project
.\scripts\setup_github_work_management.ps1
```

اگر بخواهید دستی انجام دهید:

1. در GitHub repo وارد تب `Issues` شوید.
2. issueهای CSV را دستی یا با GitHub CLI بسازید.
3. از تب `Projects` یک board با ستون‌های `Backlog`, `To Do`, `In Progress`, `Review`, `Done` بسازید.
4. issueها را بر اساس مقدار ستون `Status` در CSV روی board قرار دهید.

## Knowledge Base واقعی در Notion

برای ساخت Knowledge Base واقعی در Notion، اسکریپت `scripts/setup_notion_knowledge_base.py` اضافه شده است. این اسکریپت صفحات Sprint Notes، Meeting Notes، Technical Decisions، Stakeholder Feedback و Team Playbook را در Notion می‌سازد و یک database برای task board ایجاد می‌کند.

اجرای پیشنهادی:

```powershell
$env:NOTION_TOKEN='secret_...'
$env:NOTION_PARENT_PAGE_ID='your_parent_page_id'
C:\Users\Webhouse\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\setup_notion_knowledge_base.py
```

اگر استاد پرسید چرا Jira استفاده نشده، پاسخ دفاعی:

> برای مقیاس کوچک پروژه از Jira رسمی استفاده نکردیم، اما artifactهای معادل Jira شامل backlog، sprint board، task assignment، time tracking، burndown، KPI tracking و knowledge base در GitHub/Docs پیاده‌سازی شده است.

## برنامه بازخورد ذی‌نفع

حداقل 5 بازخورد واقعی باید تا ارائه نهایی جمع‌آوری شود:

- 1 نفر آشنا با اورژانس، پرستاری، پزشکی یا درمانگاه
- 2 دانشجوی مهندسی/مدیریت برای UI و فهم خروجی
- 1 نفر آشنا با مدیریت بحران یا عملیات
- 1 نفر کاربر عمومی برای سادگی زبان

چهار سؤال اصلی همان فرم داخل MVP است:

1. آیا خروجی سیستم قابل فهم بود؟
2. آیا UI سریع و واضح بود؟
3. آیا مشخص بود سیستم جایگزین پزشک نیست؟
4. مهم‌ترین پیشنهاد بهبود چیست؟

خروجی فرم MVP به CSV export می‌شود و باید خلاصه آن در `docs/knowledge-base/stakeholder-feedback-log.md` ثبت شود.
