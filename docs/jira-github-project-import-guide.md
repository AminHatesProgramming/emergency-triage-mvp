<!-- rtl-normalized -->

<div dir="rtl" align="right">

# راهنمای عملیاتی Jira و GitHub Project برای امدادیار

این سند برای پاسخ مستقیم به ایراد TA آماده شده است: پروژه باید فقط «کدنویسی» دیده نشود، بلکه به‌صورت یک کار تیمی Agile با backlog، sprint، assignment، time tracking، مستندسازی دانش و شواهد قابل مشاهده ارائه شود.

## فایل‌های آماده

| کاربرد | فایل |
|---|---|
| import تسک‌ها در Jira | `docs/artifacts/jira-import-issues.csv` |
| ورود آیتم‌های مدیریت دانش در GitHub Project | `docs/artifacts/github-project-knowledge-items.csv` |
| مستندات دانش پروژه | `docs/knowledge-base/` |
| شواهد Agile و تحویل‌ها | `docs/agile-delivery-evidence.md` |
| گزارش KPI و ریسک | `docs/kpi-register.md` و `docs/risk-register.md` |

## منابع رسمی ابزارها

| ابزار | مرجع |
|---|---|
| Jira CSV Import | [Atlassian Support - Import data from a CSV file](https://support.atlassian.com/jira-cloud-administration/docs/import-data-from-a-csv-file/) |
| GitHub Projects | [GitHub Docs - About Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) |

## ساخت پروژه در Jira

1. وارد [Jira Cloud](https://pourmand.atlassian.net/jira/for-you) شوید.
2. یک پروژه Scrum بسازید.
3. نام پیشنهادی پروژه: `امدادیار - Emergency Decision Support`
4. کلید پیشنهادی پروژه: `EMD`
5. ستون‌های board را به این شکل تنظیم کنید:

| ستون | معنی |
|---|---|
| Backlog | ایده‌ها و کارهای هنوز شروع‌نشده |
| Selected for Sprint | کارهای انتخاب‌شده برای sprint جاری |
| In Progress | کار در حال انجام |
| Review / QA | بازبینی، تست، مستندسازی یا کنترل کیفیت |
| Done | خروجی تحویل‌شده و قابل ارائه |

## Sprintهای پیشنهادی

| Sprint | خروجی قابل تحویل |
|---|---|
| Sprint 0 - Discovery & Scope | تعریف مسئله، ذی‌نفعان، ارزش محصول، دامنه MVP |
| Sprint 1 - Triage-time Dataset | انتخاب featureهای مجاز در زمان تریاژ و کنترل leakage |
| Sprint 2 - API & MVP Skeleton | endpointهای اصلی، اسکلت backend و تست predict |
| Sprint 3 - Model/KPI/Risk | مدل v7، KPIها، risk register و burndown |
| Sprint 4 - PWA/UI/Docs | رابط فارسی mobile-first، مستندات و QA |
| Sprint 5 - Public Deploy & Evidence | deploy عمومی، تست موبایل، آماده‌سازی شواهد |
| Sprint 6 - Pilot Feedback & Final Polish | جمع‌آوری بازخورد پایلوت و روتوش نهایی |

## Import کردن CSV در Jira

مسیر دقیق ممکن است بسته به سطح دسترسی Jira کمی فرق کند. اگر دسترسی admin دارید از مسیر import رسمی Jira استفاده کنید؛ اگر ندارید از import ساده issueها در خود پروژه استفاده کنید.

در زمان import، ستون‌ها را این‌طور map کنید:

| ستون CSV | فیلد Jira |
|---|---|
| `Issue Type` | Issue Type |
| `Summary` | Summary |
| `Description` | Description |
| `Assignee` | Assignee |
| `Priority` | Priority |
| `Status` | Status |
| `Sprint` | Sprint یا Label/Custom Field |
| `Story Points` | Story point estimate |
| `Original Estimate` | Original estimate |
| `Time Spent` | Time spent |
| `Labels` | Labels |
| `Component/s` | Components |
| `Start Date` | Start date |
| `Due Date` | Due date |
| `Evidence Link` | لینک شواهد یا یک custom field با همین نام |

اگر Jira اسم اعضا را نشناخت، ابتدا محمدرضا آرمان پور و محدثه حاتمی کیا را به پروژه invite کنید. اگر امکان invite نبود، issueها را unassigned وارد کنید و فیلد `Owner Role` را نگه دارید تا نقش تیمی در گزارش و ارائه قابل دفاع بماند.

## نقش‌های تیمی قابل دفاع

| عضو | نقش | کارهای قابل توضیح در ارائه |
|---|---|---|
| محمدامین پورمند | Project Lead / ML & System Architect | معماری، مدل، API، deploy و کنترل leakage |
| محمدرضا آرمان پور | Project Control & Metrics Coordinator | KPI، ریسک، burndown، ارزش اجتماعی و زمان‌بندی |
| محدثه حاتمی کیا | UI/Documentation & QA Coordinator | تست سناریوها، بازبینی UI، مستندسازی و کنترل کیفیت |

## Time Tracking

در Jira، Time tracking را فعال کنید و برای issueها مقدارهای `Original Estimate` و `Time Spent` را نگه دارید. این کار دقیقاً همان چیزی است که TA خواسته: مشخص باشد هر task چه کسی داشته، چقدر زمان برده و در کدام sprint تحویل شده است.

## گزارش‌هایی که باید screenshot بگیرید

برای مستندات نهایی و پوستر، این screenshotها بیشترین ارزش دفاعی را دارند:

| تصویر | دلیل اهمیت |
|---|---|
| Backlog با issueهای sprintبندی‌شده | نشان می‌دهد پروژه از backlog شروع شده است |
| Active Sprint Board | نشان می‌دهد کارها وضعیت و مالک دارند |
| یک issue بازشده با assignee، زمان، sprint و evidence link | نشان‌دهنده کار تیمی و time tracking است |
| Burndown Report | پاسخ مستقیم به معیار مدیریت پروژه |
| صفحه GitHub Project دانش | پاسخ مستقیم به معیار Knowledge Management |
| لینک عمومی امدادیار روی موبایل | نشان‌دهنده عملیاتی شدن محصول |

## ساخت GitHub Project برای مدیریت دانش

1. در GitHub وارد repository شوید.
2. از بخش Projects یک Project جدید بسازید.
3. نام پیشنهادی: `Emdadyar Knowledge Base`
4. نوع نمایش را `Table` قرار دهید.
5. این فیلدها را بسازید:

| فیلد | کاربرد |
|---|---|
| Area | دسته دانش: Sprint، Risk، KPI، AI Usage، Feedback، Decision |
| Owner | مسئول نگهداری دانش |
| Status | Draft / Review / Done |
| Sprint | ارتباط با sprintهای Jira |
| Evidence Link | لینک فایل یا سند شواهد |
| Last Updated | تاریخ آخرین بروزرسانی |

سپس ردیف‌های فایل `docs/artifacts/github-project-knowledge-items.csv` را به‌صورت دستی وارد کنید یا برای هر ردیف یک issue کوچک بسازید و آن را به Project اضافه کنید. هدف این نیست که محتوا دوباره کپی شود؛ هدف این است که «مدیریت دانش» در یک ابزار قابل مشاهده باشد و هر آیتم به سند اصلی در repository لینک بدهد.

## جمله آماده برای دفاع

برای مدیریت کار، از ساختار Scrum در Jira استفاده کردیم: backlog، sprint، assignee، status، story point، time tracking و لینک شواهد برای هر task مشخص است. برای مدیریت دانش، یک GitHub Project جدا و پوشه مستندات دانش داریم که تصمیم‌های فنی، ریسک‌ها، KPIها، گزارش استفاده از AI، یادداشت‌های sprint و بازخورد ذی‌نفعان را نگهداری می‌کند.

</div>
