<!-- rtl: fa -->
<div dir="rtl" align="right">

# Sprint Notes | امداد یار

## Sprint 0: تعریف مسئله و محدوده

| بخش | توضیح |
|---|---|
| Goal | انتخاب مسئله سلامت‌محور، تعریف ارزش انسانی و محدوده MVP |
| Tasks | تعریف مسئله، ذی‌نفعان، ارزش اجتماعی/ملی، نقش decision-support، محدودیت اخلاقی |
| Deliverables | <span dir="ltr">docs/project-management-plan.md</span>، <span dir="ltr">docs/stakeholder-register.md</span>، <span dir="ltr">docs/scope-change-record.md</span> |
| Risks | ادعای بیش از حد پزشکی؛ دامنه مبهم؛ نبود ارزش قابل اندازه‌گیری |
| Decisions | تمرکز بر تریاژ اورژانس و تعریف سامانه به عنوان پشتیبان تصمیم |
| What changed? | پروژه از ایده خام به محصول سلامت‌محور با KPI مشخص تبدیل شد. |
| What remained? | تاریخ دقیق جلسه و لینک واقعی Jira هنوز باید تکمیل شود. |
| Link to Jira issues | PD-01, PD-02, SAFE-01 |

## Sprint 1: مدل/منطق ارزیابی

| بخش | توضیح |
|---|---|
| Goal | ساخت baseline مدل و کنترل data leakage |
| Tasks | انتخاب features triage-time، حذف داده‌های آینده، آموزش مدل‌های اولیه، تعریف threshold و متریک‌ها |
| Deliverables | <span dir="ltr">ml/train.py</span>، <span dir="ltr">docs/model-card.md</span>، <span dir="ltr">reports/model/metrics_v5.json</span> و سپس v6/v7 |
| Risks | leakage، FPR بالا، وابستگی بیش از حد به age/gender، ناتوانی با داده ناقص |
| Decisions | استفاده از AUC/Recall/Precision/FPR؛ انتخاب safety-first threshold |
| What changed? | مدل از آزمایش اولیه به نسخه قابل دفاع‌تر با داده زمان تریاژ رسید. |
| What remained? | اعتبارسنجی بالینی و تحلیل fairness در فاز بعدی. |
| Link to Jira issues | ML-01, ML-02, ML-03, ML-04, ML-05 |

## Sprint 2: UI و تجربه کاربر

| بخش | توضیح |
|---|---|
| Goal | تبدیل مدل به تجربه قابل استفاده برای کاربر فارسی‌زبان |
| Tasks | طراحی فرم، خروجی قابل فهم، نمونه‌های تست، هشدارهای مهم، اقدام بعدی، خلاصه کیس |
| Deliverables | <span dir="ltr">frontend/index.html</span>، <span dir="ltr">frontend/app.js</span>، <span dir="ltr">frontend/styles.css</span> |
| Risks | شلوغی UI، سوءبرداشت از خروجی، سختی استفاده روی موبایل |
| Decisions | فارسی و راست‌به‌چپ؛ متن ساده؛ قرار گرفتن نمونه‌های تست پایین فرم |
| What changed? | خروجی از ESI/عدد خام به پیام قابل عمل تبدیل شد. |
| What remained? | تست خوانایی با کاربر واقعی. |
| Link to Jira issues | UX-01, UX-02, UX-03, SAFE-02, SAFE-03 |

## Sprint 3: مستندسازی، بازخورد و آماده‌سازی دفاع

| بخش | توضیح |
|---|---|
| Goal | پاسخ به نقد TA درباره غیرمدیریت‌پروژه‌ای بودن کار |
| Tasks | ساخت Knowledge Base، Sprint Notes، Meeting Notes، Risk Register، KPI، Burndown، AI Usage Report |
| Deliverables | <span dir="ltr">docs/knowledge-base/</span>، <span dir="ltr">docs/agile-delivery-evidence.md</span>، <span dir="ltr">docs/kpi-register.md</span>، <span dir="ltr">docs/risk-register.md</span> |
| Risks | کم‌رنگ دیده شدن نقش اعضا؛ نبود evidence واقعی ابزار مدیریت پروژه؛ نبود feedback خارجی |
| Decisions | تعریف نقش‌های قابل ارائه برای هر عضو؛ آماده‌سازی CSV import برای Jira و knowledge project |
| What changed? | پروژه از demo فنی به بسته مدیریت پروژه با artifactهای قابل دفاع تبدیل شد. |
| What remained? | ساخت واقعی Jira/Notion و گرفتن screenshot واقعی. |
| Link to Jira issues | PM-01, PM-02, PM-03, DOC-01, DOC-04 |

## Final Sprint: deploy، QR، پوستر و تحویل نهایی

| بخش | توضیح |
|---|---|
| Goal | آماده‌سازی نسخه عمومی و بسته تحویل نهایی |
| Tasks | GitHub Pages، PWA، QR، package بازار، poster assets، cleanup docs، final index |
| Deliverables | <span dir="ltr">https://aminhatesprogramming.github.io/emergency-triage-mvp/</span>، <span dir="ltr">docs/artifacts/emdadyar-pwa-qr.png</span>، <span dir="ltr">poster-final-assets-fa.md</span>، <span dir="ltr">docs/final-submission-index.md</span> |
| Risks | خراب شدن لینک عمومی، ادعای بازخورد بدون تأیید، فایل‌های قدیمی و گیج‌کننده |
| Decisions | حذف docs قدیمی، برچسب‌گذاری feedbackهای synthetic، ثبت بازخوردهای پرستار به صورت pending confirmation |
| What changed? | نسخه نهایی تمیزتر و قابل ارسال‌تر شد. |
| What remained? | وارد کردن CSVها در Jira/Notion، گرفتن screenshot واقعی و تأیید بازخوردهای خارجی. |
| Link to Jira issues | DEP-01, FD-01, FD-02, FD-03, FB-02 |
</div>

