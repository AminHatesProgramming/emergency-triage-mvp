# خروجی‌های رسمی قابل تحویل

این پوشه خروجی‌های Word رسمی را نگه می‌دارد. فایل‌های Markdown داخل `docs/` همچنان منبع قابل ردیابی پروژه هستند، اما برای تحویل رسمی، فایل‌های این پوشه مناسب‌ترند.

## فایل‌ها

| فایل | کاربرد |
|---|---|
| `ITPM_Final_Report_Emergency_Triage.docx` | گزارش نهایی کتبی پروژه برای بخش ۲ نمره‌ای |
| `ITPM_Project_Management_Evidence_Package.docx` | پیوست مدیریت پروژه: KPI، Burndown، RACI، WBS، Time Tracking، Work/Knowledge Management |
| `ITPM_Presentation_and_Submission_Guide.docx` | راهنمای ویدئوی ۱۰ دقیقه‌ای، demo، نقش اعضا و checklist تحویل |

## خروجی PDF

برای PDF گرفتن، فایل را در Microsoft Word باز کنید:

1. File
2. Save As یا Export
3. PDF
4. گزینه `Optimize for: Standard` را انتخاب کنید.

این روش برای متن فارسی مطمئن‌تر از تبدیل خودکار است.

## نکته QA

در این محیط LibreOffice/soffice نصب نبود، بنابراین رندر خودکار DOCX به PNG/PDF برای visual QA انجام نشد. فایل‌ها با `python-docx` از نظر باز شدن، تعداد جدول‌ها و تصاویر بررسی شدند.
