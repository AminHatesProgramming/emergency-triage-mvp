<!-- rtl: fa -->
<div dir="rtl" align="right">

# راهنمای ساخت Jira Board برای امداد یار

## 1. ساخت پروژه

1. وارد Jira شوید: <span dir="ltr">https://pourmand.atlassian.net/jira/for-you</span>
2. گزینه Create Project را بزنید.
3. نوع پروژه را Scrum انتخاب کنید، نه Kanban.
4. نام پروژه:
   <span dir="ltr">Emdadyar - Emergency Decision Support</span>
5. Key پیشنهادی:
   <span dir="ltr">EMD</span>
6. اگر Jira فارسی/انگلیسی بود مهم نیست؛ نام issueها فارسی هستند.

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

اگر Jira اجازه import Epic Name نداد، اول ۹ Epic را دستی بسازید و سپس taskها را import کنید.

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

## 6. Import CSV

فایل import:
<span dir="ltr">project-management-final-package/jira-issues-import.csv</span>

Mapping پیشنهادی:

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

## 7. Sprints پیشنهادی

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

## 10. لینک دادن Jira به Notion

1. پس از ساخت Notion Home، URL صفحه را کپی کنید.
2. در Jira یک Project Shortcut با نام «Notion Knowledge Base» بسازید.
3. برای هر Epic، لینک صفحه Notion مرتبط را در Description قرار دهید.
4. در Notion هم یک property به نام Jira Issue بسازید و key issue را وارد کنید.

## 11. لینک دادن Jira به GitHub commits

چون commitهای قدیمی key Jira ندارند، ساده‌ترین راه:

1. در description هر issue بخش Evidence بسازید.
2. commit hash یا مسیر فایل را بگذارید؛ مثال:
   <span dir="ltr">commit 43737c8 - frontend/index.html</span>
3. برای commitهای بعدی، نام issue را در commit message بیاورید؛ مثال:
   <span dir="ltr">EMD-23 update stakeholder feedback log</span>
4. در GitHub repository، اگر دسترسی داشتی Jira integration را فعال کن تا commitها خودکار لینک شوند.

## 12. Screenshotهایی که باید برای استاد بگیری

- Backlog با Epics و taskها
- Active Sprint با ستون‌های workflow
- یک issue باز شده که Assignee، Story Point، Time Tracking و Evidence Link دارد
- Burndown chart
- صفحه Project Settings یا Components برای نشان دادن roleها
</div>

