<!-- rtl-normalized -->
<div dir="rtl" align="right">

# خروجی‌های رسمی قابل تحویل

این پوشه خروجی‌های Word رسمی را نگه می‌دارد. فایل‌های Markdown داخل `docs/` همچنان منبع قابل ردیابی پروژه هستند، اما برای تحویل رسمی، فایل‌های این پوشه مناسب‌ترند.

## فایل‌ها

| فایل | کاربرد |
|---|---|
| `ITPM_Final_Report_Emergency_Triage.docx` | گزارش نهایی کتبی پروژه برای بخش ۲ نمره‌ای |
| `ITPM_Project_Management_Evidence_Package.docx` | پیوست مدیریت پروژه: KPI، Burndown، RACI، WBS، Time Tracking، Work/Knowledge Management |
| `ITPM_Project_Governance_and_Resource_Management.docx` | چرخه عمر، منابع انسانی و غیرانسانی، هزینه، ارتباطات، کیفیت و خاتمه MVP |
| `ITPM_Final_Announcement_Compliance_Matrix.docx` | تطبیق هر الزام اعلان نهایی با شاهد، وضعیت و اقدام باقی‌مانده |
| `Emdadyar_Final_Presentation_Runbook.docx` | سناریوی دقیق ارائه ۱۰ دقیقه‌ای با تقسیم زمان ۶، ۲ و ۲ دقیقه |
| `Emdadyar_Mobile_App_For_Professor.docx` | فایل کوتاه و قابل ارسال برای استاد شامل لینک، QR و روش نصب PWA |
| `Emdadyar_Market_Release_Package.zip` | بسته آماده انتشار شامل APK/AAB امضاشده، متن مارکت، screenshotها، دارایی‌های گرافیکی و گزارش کنترل کیفیت |

## پیوست‌های جدید پس از بازخورد TA

برای پاسخ به نقد «غیرمدیریت‌پروژه‌ای دیده شدن پروژه»، این artifactها به repo اضافه شدند:

- `docs/agile-delivery-evidence.md`
- `docs/jira-github-project-import-guide.md`
- `docs/final-submission-index.md`
- `docs/final-submission-master-checklist.md`
- `docs/artifacts/jira-import-issues.csv`
- `docs/artifacts/github-project-knowledge-items.csv`
- `docs/knowledge-base/README.md`
- `docs/knowledge-base/stakeholder-feedback-log.md`
- `docs/ux-feedback-synthesis.md`
- `docs/triage-nurse-feedback-confirmation.md`
- `data/feedback/synthetic-prepilot-feedback-fa.csv` با برچسب شفاف `synthetic_pre_pilot`
- `data/feedback/triage-nurse-feedback-confirmed.csv` شامل ۹ بازخورد تأییدشده و اقدام متناظر
- `docs/stakeholder-outreach-log.md` شامل وضعیت پیگیری بیمارستان پیامبران تهران و سلامت فردای تهران

## خروجی PDF

برای PDF گرفتن، فایل را در Microsoft Word باز کنید:

1. File
2. Save As یا Export
3. PDF
4. گزینه `Optimize for: Standard` را انتخاب کنید.

این روش برای متن فارسی مطمئن‌تر از تبدیل خودکار است.

## نکته QA

در این محیط LibreOffice/soffice نصب نبود، بنابراین رندر خودکار DOCX به PNG/PDF برای visual QA انجام نشد. فایل‌ها با `python-docx` از نظر باز شدن، تعداد جدول‌ها و تصاویر بررسی شدند.
</div>
