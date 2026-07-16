<!-- rtl-normalized -->
<div dir="rtl" align="right">

# فهرست رسمی تحویل نهایی امدادیار

این فایل مرجع اصلی تحویل پروژه است. برای ارائه به استاد و TA، از همین فهرست استفاده شود و فایل‌های draft یا قدیمی مبنای دفاع قرار نگیرند.

بسته `Emdadyar_Submission_Core_Ready_For_Platform_Evidence.zip` شامل هسته آماده تحویل است. تا زمانی که اسکرین‌شات‌های واقعی Jira/Notion، لینک دسترسی، ویدئوی ۱۰ دقیقه‌ای و پوستر نهایی به آن افزوده نشده‌اند، نباید به‌عنوان ZIP کامل تحویل ارسال شود.

## 1. خروجی‌های رسمی Word و بسته تحویل

| خروجی | مسیر | کاربرد |
|---|---|---|
| گزارش نهایی پروژه | `docs/deliverables/ITPM_Final_Report_Emergency_Triage.docx` | گزارش اصلی درس |
| پیوست شواهد مدیریت پروژه | `docs/deliverables/ITPM_Project_Management_Evidence_Package.docx` | KPI، Burndown، WBS، RACI، Time Tracking |
| حاکمیت و مدیریت منابع | `docs/deliverables/ITPM_Project_Governance_and_Resource_Management.docx` | چرخه عمر، منابع، هزینه، ارتباطات، کیفیت و دانش |
| ماتریس انطباق اعلان نهایی | `docs/deliverables/ITPM_Final_Announcement_Compliance_Matrix.docx` | تطبیق مو‌به‌موی الزامات با شاهد و وضعیت |
| سناریوی ارائه نهایی | `docs/deliverables/Emdadyar_Final_Presentation_Runbook.docx` | تقسیم قطعی ۶ + ۲ + ۲، دمو و پاسخ پرسش‌ها |
| نسخه موبایلی برای استاد | `docs/deliverables/Emdadyar_Mobile_App_For_Professor.docx` | لینک، QR و روش نصب PWA |
| بسته انتشار امدادیار | `docs/deliverables/Emdadyar_Market_Release_Package.zip` | APK/AAB امضاشده، تصویرها، متن مارکت، Data Safety و گزارش صحت build |

## 2. مستندات فنی رسمی

| سند | مسیر |
|---|---|
| معماری سیستم | `docs/architecture.md` |
| مستند API | `docs/api-documentation.md` |
| Model Card | `docs/model-card.md` |
| ممیزی نهایی متریک مدل | `docs/model-final-metrics-audit.md` |
| ممیزی held-out و سناریوهای ایمنی | `docs/model-release-scenario-audit-fa.md` |
| راهنمای deploy عمومی و موبایل | `docs/deployment-mobile-webapp.md` |
| یادداشت تکمیل PWA | `docs/mobile-pwa-completion-note.md` |

## 3. مستندات مدیریت پروژه رسمی

| سند | مسیر |
|---|---|
| برنامه مدیریت پروژه | `docs/project-management-plan.md` |
| حاکمیت، منابع، هزینه و ارتباطات | `docs/project-governance-and-resource-management.md` |
| شواهد Agile و تحویل Sprintها | `docs/agile-delivery-evidence.md` |
| ساختار مدیریت کار | `docs/work-management-board.md` |
| راهنمای Jira و GitHub Project | `docs/jira-github-project-import-guide.md` |
| چک‌لیست مادر تحویل | `docs/final-submission-master-checklist.md` |
| ماتریس انطباق با اعلان نهایی | `docs/final-announcement-compliance-matrix.md` |
| KPI Register | `docs/kpi-register.md` |
| Risk Register | `docs/risk-register.md` |
| WBS و RACI | `docs/wbs-raci.md` |
| ماتریس همکاری تیم | `docs/team-collaboration-matrix.md` |
| Roadmap | `docs/roadmap.md` |

## 4. مستندات مدیریت دانش رسمی

| سند | مسیر |
|---|---|
| Knowledge Base | `docs/knowledge-base/README.md` |
| Sprint Notes | `docs/knowledge-base/sprint-notes.md` |
| Meeting Notes | `docs/knowledge-base/meeting-notes.md` |
| Technical Decisions | `docs/knowledge-base/technical-decisions.md` |
| Team Playbook | `docs/knowledge-base/team-playbook.md` |
| Stakeholder Feedback Log | `docs/knowledge-base/stakeholder-feedback-log.md` |
| ساختار مدیریت دانش | `docs/knowledge-management-index.md` |
| گزارش استفاده از AI | `docs/ai-usage-report.md` |
| درس‌آموخته‌ها | `docs/lessons-learned.md` |

## 5. فایل‌های آماده ورود به ابزارها

| فایل | کاربرد |
|---|---|
| `docs/artifacts/jira-import-issues.csv` | ورود backlog، Sprintها، assignee و time tracking به Jira |
| `docs/artifacts/github-project-knowledge-items.csv` | ورود آیتم‌های مدیریت دانش به GitHub Project |
| `docs/artifacts/time-tracking-log.csv` | شواهد زمان همکاری تیم |
| `docs/artifacts/burndown.svg` | نمودار Burndown |
| `docs/artifacts/velocity.svg` | نمودار Velocity |
| `docs/artifacts/user-acquisition.svg` | پیش‌بینی جذب کاربر پایلوت |
| `reports/model/release_validation_v7.json` | بازتولید متریک روی ۱۱۱٬۶۰۶ رکورد test و ارزیابی sparse |
| `reports/model/browser_backend_differential_v7.json` | تطابق ۱٬۱۶۷ سناریوی مرورگر و API |

## 6. بازخورد و اعتبارسنجی کاربر

| سند | وضعیت |
|---|---|
| `docs/ux-feedback-synthesis.md` | تحلیل 78 بازخورد شبیه‌سازی‌شده پیش از پایلوت |
| `docs/triage-nurse-feedback-confirmation.md` | گزارش ۹ بازخورد تأییدشده پرستاران و اقدام‌های نسخه نهایی |
| `data/feedback/triage-nurse-feedback-confirmed.csv` | ۹ بازخورد تأییدشده با اقدام‌های نسخه نهایی |
| `docs/stakeholder-outreach-log.md` | پیگیری دو مرکز درمانی و وضعیت در انتظار پاسخ نهایی |

## 7. فایل‌های پوستر و ارائه

| فایل | کاربرد |
|---|---|
| `poster-final-assets-fa.md` | محتوای نهایی آماده برای ساخت پوستر با مدل تصویر |
| `docs/poster-content.md` | نسخه متنی خلاصه برای پوستر |
| `docs/video-presentation-script.md` | راهنمای ارجاع به سناریوی رسمی ۱۰ دقیقه‌ای |
| `docs/deliverables/Emdadyar_Final_Presentation_Runbook.docx` | سناریوی دقیق ارائه ۱۰ دقیقه‌ای با تقسیم ۶ + ۲ + ۲ |
| `docs/market/README.md` | بسته انتشار و screenshotهای مارکت |

## جمله دفاعی

پروژه امدادیار فقط یک مدل هوش مصنوعی نیست؛ یک MVP قابل اجرا با رویکرد Agile است که برای آن backlog، Sprint، assignee، time tracking، KPI، risk register، مدیریت دانش، بازخورد کاربر، مستندات فنی و نسخه قابل نصب موبایل آماده شده است.

</div>
