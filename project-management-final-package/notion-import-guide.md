<!-- rtl: fa -->
<div dir="rtl" align="right">

# راهنمای ورود بسته به Notion

## 1. ساخت ساختار صفحه‌ها

در Notion یک صفحه اصلی بسازید:

«امداد یار | دانشنامه پروژه و مدیریت دانش»

سپس این sub-pageها را بسازید:

| صفحه | فایل منبع |
|---|---|
| Project Overview | notion-project-overview.md |
| Product Features | notion-product-features.md |
| Sprint Notes | notion-sprint-notes.md |
| Meeting Notes | notion-meeting-notes.md |
| AI Usage Report | notion-ai-usage-report.md |
| Lessons Learned | notion-lessons-learned.md |
| Jira Import & Board Setup | jira-board-setup.md |
| Missing Info Checklist | missing-info-checklist.md |

## 2. وارد کردن Markdownها

بهترین روش:

1. محتوای هر فایل markdown را باز کنید.
2. متن داخل فایل را در صفحه مربوط Notion paste کنید.
3. اگر جدول‌ها بهم ریختند، از Notion table ساده استفاده کنید.
4. لینک‌های مسیر فایل را به repository یا GitHub raw/file link تبدیل کنید.

## 3. ساخت Databaseها از CSV

فایل‌های زیر را با گزینه Import یا Merge with CSV وارد کنید:

| Database | فایل |
|---|---|
| Decision Log | notion-decision-log.csv |
| Change Log | notion-change-log.csv |
| Risk Register | notion-risk-register.csv |
| Stakeholder Feedback | notion-stakeholder-feedback.csv |
| QA Test Log | notion-qa-test-log.csv |

## 4. Relationهای پیشنهادی

| From Database | Relation To | دلیل |
|---|---|---|
| Decision Log | Jira Issues | هر تصمیم باید issue مرتبط داشته باشد |
| Change Log | Decision Log | بعضی تغییرها نتیجه تصمیم هستند |
| Risk Register | Jira Issues | هر ریسک باید action یا task داشته باشد |
| QA Test Log | Jira Issues | تست‌ها باید به taskهای QA وصل شوند |
| Stakeholder Feedback | Change Log | هر بازخورد مهم باید action taken داشته باشد |

## 5. Propertyهای مهم Notion

برای هر database این propertyها را بسازید:

- Owner: Person یا Text
- Status: Select
- Sprint: Select
- Jira Issue: URL یا Text
- Evidence Link: URL یا Text
- Last Updated: Date
- Needs Completion: Checkbox

## 6. اضافه کردن Jira issue link

پس از import در Jira:

1. key هر issue مثل EMD-12 را بردارید.
2. در Notion property «Jira Issue» وارد کنید.
3. در Jira هم لینک Notion page/database item را در description یا web link بگذارید.

## 7. اضافه کردن Evidence Link

برای هر item، حداقل یکی از این شواهد را بگذارید:

- مسیر فایل در repo، مثل frontend/app.js
- commit hash، مثل 43737c8
- artifact تصویری، مثل poster-assets/ui-mobile-view.png
- گزارش، مثل reports/model/metrics_v7.json
- لینک عمومی اپ
- screenshot واقعی Jira/Notion پس از ساخت

## 8. مرتب کردن صفحه اصلی مثل دانشنامه پروژه

ترتیب پیشنهادی صفحه Home:

1. معرفی کوتاه و warning اخلاقی
2. لینک اپ، repo، Jira و Notion
3. وضعیت فعلی MVP
4. اعضای تیم و نقش‌ها
5. Quick Links به databaseها
6. آخرین Sprint و کارهای باقی‌مانده
7. بخش Evidence برای screenshotها

## 9. نکته مهم برای صداقت دفاع

هر چیزی که هنوز واقعی نیست، با عبارت «نیاز به تکمیل دارد» نگه دارید. بعد از ساخت واقعی Jira board، Notion database، گرفتن feedback واقعی و screenshotها، همان itemها را به Done یا Confirmed تغییر دهید.
</div>

