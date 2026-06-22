<!-- rtl-normalized -->
<div dir="rtl" align="right">

# Final Submission Compliance - 2026-06-15

این سند بر اساس فایل `ITPM Project Submission - Final (3).pdf` و اسکرین‌شات معیارهای Work Management / Knowledge Management تهیه شده است.

## خلاصه بارم‌بندی

| بخش | نمره | الزام | وضعیت پروژه |
|---|---:|---|---|
| ویدئوی ۱۰ دقیقه‌ای | ۲ | معرفی، KPI، چالش‌ها، demo و استفاده خدمت‌گیرندگان | سناریوی ویدئو و MVP آماده؛ feedback واقعی باید ضبط/ثبت شود |
| گزارش نهایی کتبی | ۲ | رخدادها، معماری، scope، تیم، ریسک، roadmap | Word/PDF-ready و گزارش تکمیلی Agile آماده |
| دسترسی سامانه‌ها | ۳ | Work Management + Knowledge Management واقعی | اسکریپت ساخت GitHub Projects و Notion KB آماده؛ پس از اجرای credentialها لینک‌ها ثبت شود |

## Work Management

الزام PDF:

- استفاده از Jira/Trello یا موارد مشابه
- taskهای تعریف‌شده
- assign شدن وظایف
- time tracking از ابتدای ترم
- taskهای آینده
- انطباق با Agile

پوشش پروژه:

- ابزار پیشنهادی عملیاتی: GitHub Issues / GitHub Projects
- اسکریپت اجرا: `scripts/setup_github_work_management.ps1`
- seed تسک‌ها: `docs/artifacts/github-issues-seed.csv`
- board CSV قابل import: `docs/artifacts/work-management-board.csv`
- time tracking CSV: `docs/artifacts/time-tracking-log.csv`
- شواهد Agile: `docs/agile-delivery-evidence.md`

خروجی مورد نیاز قبل از ارسال:

- لینک GitHub Issues
- لینک GitHub Project board
- screenshot از board با ستون‌های Backlog / To Do / In Progress / Review / Done

## Knowledge Management

الزام PDF:

- استفاده از Confluence/Notion یا موارد مشابه
- ساختار داکیومنت‌ها
- مستندسازی API
- تصمیمات فنی
- صورتجلسات
- دانش تولیدشده در طول ترم

پوشش پروژه:

- ابزار پیشنهادی عملیاتی: Notion Knowledge Base
- اسکریپت اجرا: `scripts/setup_notion_knowledge_base.py`
- منابع Knowledge Base: `docs/knowledge-base/`
- API docs: `docs/api-documentation.md`
- decision log: `docs/decision-log.md`

خروجی مورد نیاز قبل از ارسال:

- لینک Notion parent page
- لینک Notion Task Board database
- export یا screenshot از صفحات Sprint Notes، Technical Decisions و Stakeholder Feedback

## خروجی گرفتن از کاربر / ذی‌نفع

الزام PDF در بخش demo:

- نمایش عملکرد واقعی محصول و استفاده خدمت‌گیرندگان نهایی از محصول

پوشش پروژه:

- فرم بازخورد داخل MVP
- endpointهای backend:
  - `POST /feedback`
  - `GET /feedback-summary`
  - `GET /feedback/export`
- خروجی CSV عملیاتی:
  - `data/feedback/stakeholder_feedback.csv`

هدف قبل از ارائه:

- حداقل ۵ بازخورد واقعی از کاربر/ذی‌نفع
- ثبت خلاصه feedback در `docs/knowledge-base/stakeholder-feedback-log.md`
- اشاره در ویدئو که feedback loop به Sprint 5 اضافه شد

## کارهای باقی‌مانده غیرقابل اتوماسیون بدون credential

| کار | دلیل |
|---|---|
| اجرای GitHub Projects واقعی | نیاز به GitHub CLI login و scope `project` |
| ساخت Notion واقعی | نیاز به `NOTION_TOKEN` و share شدن parent page با integration |
| دادن دسترسی به تیم آموزشی | باید از داخل GitHub/Notion با حساب مالک انجام شود |

## جمله دفاعی

> برای بخش ۳ نمره‌ای، پروژه فقط فایل مستند ندارد. Work Management با GitHub Issues/Projects ساخته می‌شود که شامل backlog، sprint، owner، status، story point، time tracking و taskهای آینده است. Knowledge Management نیز در Notion ساخته می‌شود و صفحات Sprint Notes، Meeting Notes، Technical Decisions، API Docs، Stakeholder Feedback و Team Playbook دارد. برای استفاده خدمت‌گیرندگان، داخل MVP فرم بازخورد و خروجی CSV سروری اضافه شده است.
</div>
