<!-- rtl-normalized -->
<div dir="rtl" align="right">

# WBS و RACI Matrix

## Work Breakdown Structure

| کد | بسته کاری | خروجی | مسئول اصلی |
|---|---|---|---|
| 1.0 | تعریف پروژه | charter، scope، stakeholder list | محمدامین |
| 1.1 | تحلیل الزامات تحویل | checklist انطباق | محمدرضا |
| 1.2 | تحلیل مسئله و ارزش اجتماعی | problem statement | محمدرضا |
| 2.0 | توسعه مدل ML | train script، model metrics | محمدامین |
| 2.1 | کنترل leakage | انتخاب featureهای مجاز | محمدامین |
| 2.2 | بهبود v6 | اصلاح دما، history features، threshold | محمدامین |
| 3.0 | Backend | FastAPI endpoints | محمدامین |
| 4.0 | Frontend | UI فارسی mobile-first | محدثه |
| 4.1 | سناریوهای demo | critical، moderate، sparse | محدثه |
| 5.0 | مستندات | report، model card، architecture | همه |
| 5.1 | Risk/KPI/Agile docs | dashboard، risk register، KPI register | محمدرضا |
| 5.2 | QA و Knowledge Base | QA، meeting notes، API docs | محدثه |
| 6.0 | تحویل نهایی | پوستر، ویدئو، گزارش، board | همه |

## RACI

راهنما:

- R = Responsible
- A = Accountable
- C = Consulted
- I = Informed

| فعالیت | محمدامین | محمدرضا | محدثه |
|---|---|---|---|
| تعریف scope | A/R | C | C |
| تحلیل ارزش اجتماعی | C | A/R | C |
| مدل ML | A/R | C | I |
| API | A/R | I | C |
| UI | C | I | A/R |
| KPI و trade-off | C | A/R | I |
| Risk Register | C | A/R | C |
| QA سناریوها | C | I | A/R |
| پوستر | C | C | A/R |
| ویدئوی نهایی | A/R | R | R |
| گزارش نهایی | A/R | C | R |
| Trello/Notion board | C | A/R | C |
| Knowledge Base | C | C | A/R |

## منطق تقسیم مسئولیت

این RACI مالکیت هر خروجی را روشن می‌کند. مسئولیت فنی اصلی با محمدامین است؛ محدثه مالک QA و دانش پروژه است و محمدرضا کنترل شاخص‌ها، ریسک و ذی‌نفعان را بر عهده دارد.
</div>
