<!-- rtl: fa -->
<div dir="rtl" align="right">

# ثبت ساختار و بازیابی دانشنامه Notion

پیاده‌سازی اصلی دانشنامه در ۲۰۲۶-۰۷-۱۶ انجام و در ۲۰۲۶-۰۷-۱۸ ممیزی شد. این سند ساختار فعال و روش بازیابی آن در صورت انتقال Workspace را ثبت می‌کند.

صفحه اصلی: <span dir="ltr">https://app.notion.com/p/38fd955c965a80c18b7ac3a8fd176cc3</span>

## ساختار فعال

| نوع | تعداد | محتوا |
|---|---:|---|
| صفحه محتوایی | ۸ | نمای کلی، قابلیت‌ها، Sprint، نقاط هم‌راستاسازی، حاکمیت ابزارها، درس‌آموخته‌ها، شواهد باز و راهنمای تصاویر |
| پایگاه داده | ۵ | تصمیم‌ها، تغییرات، ریسک‌ها، بازخورد و QA |
| رکورد | ۷۵ | رکوردهای دارای مالک، وضعیت و Evidence |

## نگاشت فایل‌های پشتیبان

| بخش Notion | منبع قابل بازیابی |
|---|---|
| صفحه اصلی | <span dir="ltr">notion-home.md</span> |
| نمای کلی | <span dir="ltr">notion-project-overview.md</span> |
| قابلیت‌های محصول | <span dir="ltr">notion-product-features.md</span> |
| Sprint Notes | <span dir="ltr">notion-sprint-notes.md</span> |
| نقاط هم‌راستاسازی | <span dir="ltr">notion-meeting-notes.md</span> |
| حاکمیت ابزارهای کمکی | <span dir="ltr">notion-ai-usage-report.md</span> |
| درس‌آموخته‌ها | <span dir="ltr">notion-lessons-learned.md</span> |
| شواهد باز | <span dir="ltr">missing-info-checklist.md</span> |

## پایگاه‌های داده و فایل بازیابی

| پایگاه داده | فایل CSV |
|---|---|
| Decision Log | <span dir="ltr">notion-decision-log.csv</span> |
| Change Log | <span dir="ltr">notion-change-log.csv</span> |
| Risk Register | <span dir="ltr">notion-risk-register.csv</span> |
| Stakeholder Feedback | <span dir="ltr">notion-stakeholder-feedback.csv</span> |
| QA Test Log | <span dir="ltr">notion-qa-test-log.csv</span> |

فایل‌های CSV با UTF-8 BOM ذخیره شده‌اند تا متن فارسی هنگام Import به‌هم نریزد. Markdownها نیز دارای ظرف راست‌به‌چپ هستند.

## روابط دانشی

- تصمیم‌ها به Issue و Evidence مرتبط‌اند.
- تغییرها به تصمیم، فایل و نتیجه آزمون متصل‌اند.
- ریسک‌ها دارای پاسخ، مالک و کار مرتبط هستند.
- QA به سناریو، آزمون‌گر و Issue متصل است.
- بازخوردها به اقدام محصولی و وضعیت پیگیری متصل‌اند.

## کنترل نگهداری

مرجع وضعیت کار Jira و مرجع دانش پروژه Notion است. نسخه این پوشه برای بازیابی و ممیزی نگهداری می‌شود. هر ادعای وابسته به حضور، دستگاه واقعی، پاسخ بیمارستان یا اعتبارسنجی بالینی فقط پس از ثبت شاهد مستقل بسته می‌شود.

</div>
