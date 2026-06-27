<!-- rtl-normalized -->
<div dir="rtl" align="right">

# ساختار پیشنهادی سامانه مدیریت کار

این محتوا برای انتقال به Jira board یا GitHub Projects آماده شده است. معیار استاد شامل taskها، assignee، time tracking، Agile بودن، خروجی هر Sprint و taskهای آینده است. فایل import آماده Jira در `docs/artifacts/jira-import-issues.csv` قرار دارد.

## ستون‌ها

- Backlog
- Selected for Sprint
- In Progress
- Review/QA
- Done

## تنظیمات پیشنهادی Board واقعی

برای گرفتن نمره بخش Work Management، همین ساختار باید در Jira ساخته یا با CSV آماده import شود:

- هر کارت باید assignee داشته باشد.
- هر کارت باید برچسب sprint داشته باشد.
- هر کارت باید story point یا تخمین ساعت داشته باشد.
- کارت‌های انجام‌شده باید تاریخ انجام داشته باشند.
- taskهای آینده نباید خالی باشند؛ استاد صراحتاً taskهای آینده را بررسی می‌کند.

## Epicها

| Epic | هدف | خروجی |
|---|---|---|
| E1 - Project Definition | تعریف مسئله و ارزش | charter، scope، stakeholder list |
| E2 - ML Model | ساخت و ارزیابی مدل | v7 model، metrics، charts |
| E3 - Backend/API | سرویس پیش‌بینی | FastAPI endpoints |
| E4 - Frontend Demo | تجربه کاربر | UI فارسی mobile-first |
| E5 - Documentation | مدیریت دانش | گزارش، Model Card، AI report |
| E6 - Final Delivery | تحویل نهایی | پوستر، ویدئو، board، گزارش |

## Taskهای انجام‌شده

| Task | Assignee | وضعیت | زمان ثبت‌شده |
|---|---|---|---:|
| بررسی فایل‌های درس و استخراج الزامات | محمدامین | Done | 3h |
| تعریف مسئله و ارزش اجتماعی پروژه | محمدرضا | Done | 3h |
| طراحی scope و MVP | محمدامین | Done | 4h |
| آماده‌سازی pipeline مدل v5 | محمدامین | Done | 8h |
| بهبود مدل v6 و اصلاح واحد دما | محمدامین | Done | 9h |
| آموزش مدل v7 و کاهش FPR | محمدامین | Done | 9h |
| تحلیل KPI و trade-offها | محمدرضا | Done | 4h |
| پیاده‌سازی FastAPI | محمدامین | Done | 5h |
| طراحی UI فارسی mobile-first | محدثه | Done | 5h |
| deploy عمومی PWA و تست موبایل | محمدامین | Done | 5h |
| تست سناریوی sparse | محدثه | Done | 2h |
| تهیه Model Card | محمدامین | Done | 3h |
| تهیه Risk Register | محمدرضا | Done | 3h |
| تهیه چک‌لیست QA و ارزیابی | محدثه | Done | 3h |
| آماده‌سازی محتوای پوستر | محدثه | Done | 3h |
| ساخت چک‌لیست نمره‌دهی | محمدرضا | Done | 2h |
| ساخت dashboard چابک و KPIها | محمدرضا | Done | 3h |
| آماده‌سازی knowledge base structure | محدثه | Done | 3h |
| ثبت decision log و scope change | محمدامین | Done | 2h |
| آماده‌سازی poster assets و QR نسخه موبایل | محدثه | Done | 3h |
| آماده‌سازی فایل Word ارسال نسخه موبایل به استاد | محدثه | Done | 2h |
| آماده‌سازی Jira import CSV و Knowledge Project CSV | محمدرضا | Done | 4h |

## Taskهای آینده

| Task | Assignee | اولویت | تخمین |
|---|---|---|---:|
| وارد کردن `jira-import-issues.csv` در Jira | محمدرضا | High | 2h |
| ساخت GitHub Project مدیریت دانش با `github-project-knowledge-items.csv` | محدثه | High | 2h |
| گرفتن screenshot واقعی از Jira board و Knowledge Project | محدثه | High | 2h |
| ضبط ویدئوی 10 دقیقه‌ای | همه | High | 5h |
| گرفتن بازخورد از فرد آشنا با اورژانس | محمدرضا | Medium | 3h |
| تحلیل False Negativeها | محمدامین | Medium | 4h |
| بررسی fairness سن/جنسیت | محمدامین | Medium | 5h |
| ثبت نتایج پایلوت در گزارش نهایی Word/PDF | محدثه | High | 4h |

## Sprint Backlog خلاصه

| Sprint | Story Points برنامه‌ریزی‌شده | Story Points انجام‌شده | خروجی اصلی |
|---|---:|---:|---|
| Sprint 0 | 6 | 6 | مسئله، scope، ارزش اجتماعی |
| Sprint 1 | 10 | 9 | مدل اولیه و docs پایه |
| Sprint 2 | 9 | 8 | API و UI اولیه |
| Sprint 3 | 11 | 10 | v6، metrics، report |
| Sprint 4 | 8 | 8 | UI، PWA، poster assets، final delivery package |
| Sprint 5 | 9 | 8 | Agile evidence، feedback form، Jira/KM assets |
| Sprint 6 | 10 | 10 | v7، deploy عمومی، mobile handoff |

## Time Log قابل انتقال به Board

| تاریخ | عضو | فعالیت | زمان |
|---|---|---|---:|
| 2026-06-01 | محمدامین | بررسی فایل‌های درس و تعریف scope | 3h |
| 2026-06-02 | محمدامین | pipeline مدل baseline | 5h |
| 2026-06-03 | محمدرضا | تحلیل ارزش اجتماعی و KPI اولیه | 3h |
| 2026-06-04 | محدثه | بررسی user flow و UI requirements | 3h |
| 2026-06-08 | محمدامین | train مدل v6 و اصلاح دما | 9h |
| 2026-06-08 | محمدرضا | تحلیل trade-off و dashboard | 4h |
| 2026-06-08 | محدثه | QA سناریوها و مستندات | 5h |
| 2026-06-09 | محدثه | آماده‌سازی محتوای اولیه پوستر | 2h |
| 2026-06-10 | محمدامین | تکمیل package نمره‌دهی | 4h |
| 2026-06-20 | محمدامین | آموزش و ارزیابی مدل v7 | 9h |
| 2026-06-21 | محمدامین | deploy عمومی PWA و تست موبایل | 5h |
| 2026-06-22 | محمدرضا | آماده‌سازی Jira/KM import assets | 4h |
| 2026-06-22 | محدثه | آماده‌سازی فایل ارسال نسخه موبایل و QR | 3h |

## Definition of Done

- task assignee داشته باشد.
- زمان واقعی یا تخمینی ثبت شده باشد.
- خروجی قابل مشاهده در repository یا مستندات داشته باشد.
- برای deliverableهای اصلی، حداقل یک نفر دیگر review کند.
</div>
