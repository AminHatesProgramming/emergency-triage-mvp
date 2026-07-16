<!-- rtl: fa -->
<div dir="rtl" align="right">

# تنظیمات واقعی Jira و راهنمای نگهداری برد امداد یار

## 1. پروژه اجراشده

| فیلد | مقدار واقعی |
|---|---|
| نام پروژه | <span dir="ltr">Emdadyar - Emergency Decision Support</span> |
| Key | <span dir="ltr">EMD</span> |
| نوع | Team-managed software / Scrum workflow |
| لینک | <span dir="ltr">https://pourmand.atlassian.net/jira/software/projects/EMD/board</span> |
| ساختار | ۹ Epic، ۴۵ Story واردشده و ۶ Task نهایی |
| آخرین بازبینی | ۲۰۲۶-۰۷-۱۶ |

تمام ۴۵ Story قدیمی به Epic درست متصل شده‌اند. Taskهای <span dir="ltr">EMD-56</span> تا <span dir="ltr">EMD-61</span> ممیزی انتشار، Android، Notion، تست دستگاه و پایلوت را پوشش می‌دهند.

## 2. Board Type

| گزینه | مقدار پیشنهادی |
|---|---|
| Board | Scrum Board |
| Estimation | Story Points |
| Time Tracking | فعال |
| Reports | Burndown، Sprint Report، Velocity |

## 3. Workflow پیشنهادی

| ستون | معنی |
|---|---|
| Backlog | ایده یا کار هنوز وارد sprint نشده |
| Selected for Sprint | انتخاب‌شده برای sprint |
| In Progress | در حال انجام |
| Review / QA | آماده بازبینی تیم، تست یا مستندسازی |
| Done | انجام‌شده با evidence |

## 4. Issue Types

- Epic
- Story
- Task
- Bug
- Spike

این ۹ Epic اکنون با کلیدهای <span dir="ltr">EMD-2</span> تا <span dir="ltr">EMD-10</span> موجودند.

## 5. Epics

1. Problem Discovery & Scope
2. Data & Model Logic
3. Backend / Evaluation Logic
4. Frontend & UX
5. Explainability & Safety
6. Feedback & Validation
7. Project Management & Agile
8. Documentation & Knowledge Base
9. Final Deliverables

## 6. سابقه Import CSV

فایل import:
<span dir="ltr">project-management-final-package/jira-issues-import.csv</span>

CSV وارد شده است و اکنون به عنوان نسخه قابل بازسازی نگهداری می‌شود. Mapping استفاده‌شده:

| CSV Column | Jira Field |
|---|---|
| Issue Type | Issue Type |
| Summary | Summary |
| Description | Description |
| Epic Name | Epic Name یا Parent/Epic Link |
| Parent | Parent یا Epic Link |
| Assignee | Assignee |
| Priority | Priority |
| Story Points | Story Points |
| Sprint | Sprint |
| Status | Status |
| Labels | Labels |
| Acceptance Criteria | Description یا Custom Field |
| Definition of Done | Description یا Custom Field |
| Notion Link Placeholder | Description |
| Evidence Link | Description یا Web Link |

## 7. ساختار اسپرینت قابل ردیابی

| Sprint | بازه قابل دفاع | خروجی |
|---|---|---|
| Sprint 0 | 2026-06-01 تا 2026-06-02 | مسئله، scope، اخلاق |
| Sprint 1 | 2026-06-02 تا 2026-06-08 | مدل و leakage control |
| Sprint 2 | 2026-06-04 تا 2026-06-10 | backend و UI اولیه |
| Sprint 3 | 2026-06-10 تا 2026-06-15 | docs، KPI، risk، QA |
| Final Sprint | 2026-06-20 تا 2026-06-29 | deploy، QR، Notion/Jira، final deliverables |

اگر تاریخ واقعی جلسات یا کارها متفاوت است، در Jira همان تاریخ واقعی تیم را وارد کنید.

## 8. Labels

از labelهای زیر استفاده کنید:

<span dir="ltr">scope, ethics, ml, leakage, api, frontend, pwa, safety, feedback, agile, kpi, risk, documentation, notion, jira, deploy, poster, qa</span>

## 9. Components

| Component | مالک پیشنهادی |
|---|---|
| ML Model | محمدامین پورمند |
| Backend/API | محمدامین پورمند |
| Frontend/PWA | محدثه حاتمی کیا |
| Project Control | محمدرضا آرمان‌پور |
| Documentation | محدثه حاتمی کیا |
| Validation/Feedback | محمدرضا آرمان‌پور |
| Final Delivery | محمدامین پورمند |

## 10. اتصال Jira به Notion

Notion Home واقعی در این آدرس قرار دارد:
<span dir="ltr">https://app.notion.com/p/38fd955c965a80c18b7ac3a8fd176cc3</span>

رکوردهای Notion به کلید و URL واقعی Issueها وصل شده‌اند. Task پیاده‌سازی این اتصال <span dir="ltr">EMD-59</span> است. برای دسترسی سریع برد، یک Project Shortcut با عنوان «Notion Knowledge Base» در رابط Jira اضافه شود؛ این اقدام UIمحور است و باید با حساب مالک پروژه انجام شود.

## 11. لینک دادن Jira به GitHub commits

Commitهای قدیمی الزاماً key Jira ندارند؛ بنابراین Evidence هر Issue به hash و مسیر فایل متصل شده است. آخرین انتشار قابل استناد:
<span dir="ltr">16b6fc9 - Finalize safety validation and Android release</span>

برای commitهای بعدی:

1. در description هر issue بخش Evidence بسازید.
2. commit hash یا مسیر فایل را بگذارید؛ مثال:
   <span dir="ltr">commit 43737c8 - frontend/index.html</span>
3. برای commitهای بعدی، نام issue را در commit message بیاورید؛ مثال:
   <span dir="ltr">EMD-23 update stakeholder feedback log</span>
4. در GitHub repository، اگر دسترسی داشتی Jira integration را فعال کن تا commitها خودکار لینک شوند.

## 12. Screenshotهای شواهد نهایی نیازمند ثبت دستی

- Backlog با Epics و taskها
- Active Sprint با ستون‌های workflow
- یک issue باز شده که Assignee، Story Point، Time Tracking و Evidence Link دارد
- Burndown chart
- صفحه Project Settings یا Components برای نشان دادن roleها
</div>

