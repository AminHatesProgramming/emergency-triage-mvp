# خروجی‌های رسمی قابل تحویل

این پوشه خروجی‌های Word رسمی را نگه می‌دارد. فایل‌های Markdown داخل `docs/` همچنان منبع قابل ردیابی پروژه هستند، اما برای تحویل رسمی، فایل‌های این پوشه مناسب‌ترند.

## فایل‌ها

| فایل | کاربرد |
|---|---|
| `ITPM_Final_Report_Emergency_Triage.docx` | گزارش نهایی کتبی پروژه برای بخش ۲ نمره‌ای |
| `ITPM_Project_Management_Evidence_Package.docx` | پیوست مدیریت پروژه: KPI، Burndown، RACI، WBS، Time Tracking، Work/Knowledge Management |
| `ITPM_Presentation_and_Submission_Guide.docx` | راهنمای ویدئوی ۱۰ دقیقه‌ای، demo، نقش اعضا و checklist تحویل |
| `ITPM_Agile_Evidence_Addendum.docx` | پیوست تکمیلی برای پاسخ به نقد TA درباره Sprint، ابزار مدیریت کار، Knowledge Base و feedback loop |

## پیوست‌های جدید پس از بازخورد TA

برای پاسخ به نقد «غیرمدیریت‌پروژه‌ای دیده شدن پروژه»، این artifactها به repo اضافه شدند:

- `docs/agile-delivery-evidence.md`
- `docs/tooling-operationalization-guide.md`
- `docs/final-submission-compliance-2026-06-15.md`
- `docs/artifacts/github-issues-seed.csv`
- `docs/knowledge-base/README.md`
- `docs/knowledge-base/stakeholder-feedback-log.md`
- فرم بازخورد داخل MVP با امکان خروجی CSV

## خروجی PDF

برای PDF گرفتن، فایل را در Microsoft Word باز کنید:

1. File
2. Save As یا Export
3. PDF
4. گزینه `Optimize for: Standard` را انتخاب کنید.

این روش برای متن فارسی مطمئن‌تر از تبدیل خودکار است.

## نکته QA

در این محیط LibreOffice/soffice نصب نبود، بنابراین رندر خودکار DOCX به PNG/PDF برای visual QA انجام نشد. فایل‌ها با `python-docx` از نظر باز شدن، تعداد جدول‌ها و تصاویر بررسی شدند.
