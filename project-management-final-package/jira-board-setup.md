<!-- rtl: fa -->
<div dir="rtl" align="right">

# پیکربندی ثبت‌شده برد Jira امداد یار

## 1. پروژه اجراشده

| فیلد | مقدار واقعی |
|---|---|
| نام پروژه | <span dir="ltr">Emdadyar - Emergency Decision Support</span> |
| Key | <span dir="ltr">EMD</span> |
| نوع | Team-managed software / Scrum workflow |
| لینک | <span dir="ltr">https://pourmand.atlassian.net/jira/software/projects/EMD/board</span> |
| ساختار | ۹ Epic، ۴۵ Story واردشده و ۶ Task نهایی |
| آخرین بازبینی | ۲۰۲۶-۰۷-۱۸ |

تمام ۴۵ Story قدیمی به Epic درست متصل شده‌اند. Taskهای <span dir="ltr">EMD-56</span> تا <span dir="ltr">EMD-61</span> ممیزی انتشار، Android، Notion، تست دستگاه و پایلوت را پوشش می‌دهند.

## 2. تنظیمات برد

| گزینه | مقدار ثبت‌شده |
|---|---|
| Board | Scrum Board |
| Estimation | Story Points |
| Time Tracking | فعال |
| Reports | Burndown، Sprint Report، Velocity |

## 3. Workflow فعال

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

1. شناخت مسئله و تعیین محدوده
2. داده و منطق مدل
3. بک‌اند و منطق ارزیابی
4. رابط کاربری و تجربه کاربر
5. توضیح‌پذیری و ایمنی
6. بازخورد و اعتبارسنجی
7. مدیریت پروژه و اجرای چابک
8. مستندسازی و مدیریت دانش
9. تحویل‌های نهایی

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
| Notion Link | Description یا Web Link |
| Evidence Link | Description یا Web Link |

## 7. ساختار اسپرینت قابل ردیابی

| Sprint | بازه قابل دفاع | خروجی |
|---|---|---|
| Sprint 0 | 2026-06-01 تا 2026-06-02 | مسئله، scope، اخلاق |
| Sprint 1 | 2026-06-02 تا 2026-06-08 | مدل و leakage control |
| Sprint 2 | 2026-06-04 تا 2026-06-10 | backend و UI اولیه |
| Sprint 3 | 2026-06-10 تا 2026-06-15 | docs، KPI، risk، QA |
| Final Sprint | 2026-06-20 تا 2026-06-29 | deploy، QR، Notion/Jira، final deliverables |

تاریخ‌های مرجع Sprint از شواهد مخزن استخراج شده‌اند؛ تاریخ حضور یا جلسه فقط با شاهد مستقل ثبت می‌شود.

## 8. Labels

labelهای استاندارد پروژه:

<span dir="ltr">scope, ethics, ml, leakage, api, frontend, pwa, safety, feedback, agile, kpi, risk, documentation, notion, jira, deploy, poster, qa</span>

## 9. Components

| Component | مالک حوزه |
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

رکوردهای Notion به کلید و URL واقعی Issueها وصل شده‌اند و پیاده‌سازی این اتصال در <span dir="ltr">EMD-59</span> ثبت شده است. میان‌بر صفحه اصلی دانشنامه نیز به‌عنوان کنترل دسترسی سریع برد نگهداری می‌شود.

## 11. لینک دادن Jira به GitHub commits

Commitهای قدیمی الزاماً Jira Key ندارند؛ بنابراین Evidence هر Issue به hash و مسیر فایل متصل شده است. آخرین انتشار قابل استناد:
<span dir="ltr">176996a - Finalize synchronized evidence and release artifacts</span>

رویه نگهداری از این مرحله، ثبت Jira Key در پیام commit و افزودن لینک commit یا فایل در بخش Evidence همان Issue است.

## 12. مجموعه تصاویر شواهد

- Backlog با Epics و taskها
- Active Sprint با ستون‌های workflow
- یک issue باز شده که Assignee، Story Point، Time Tracking و Evidence Link دارد
- Burndown chart
- صفحه Project Settings یا Components برای نشان دادن roleها

راهنمای کامل کادر، محتوا و نام فایل‌ها در <span dir="ltr">final-screenshot-evidence-guide.md</span> و صفحه زیر قرار دارد:
<span dir="ltr">https://app.notion.com/p/3a1d955c965a81ecaa4aefc2cd3ac014</span>
</div>

