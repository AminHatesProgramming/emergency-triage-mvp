<!-- rtl-normalized -->
<div dir="rtl" align="right">

# ثبت عملیاتی مدیریت کار و دانش امداد یار

این سند وضعیت اجراشده ابزارهای مدیریت پروژه و مدیریت دانش را ثبت می‌کند. مرجع زنده کارها Jira، مرجع زنده دانش Notion و مرجع شواهد فنی GitHub است.

## بسترهای فعال

| بستر | کاربرد | وضعیت |
|---|---|---|
| Jira | Backlog، Sprint، مالک، اولویت، وضعیت، معیار پذیرش و Evidence | پروژه EMD فعال |
| Notion | تصمیم‌ها، تغییرات، ریسک‌ها، QA، بازخورد و درس‌آموخته‌ها | دانشنامه فعال |
| GitHub | کد، تاریخچه تغییر، گزارش‌های مدل و فایل‌های تحویل | مخزن عمومی فعال |

## وضعیت ثبت‌شده Jira

| شاخص | مقدار ممیزی‌شده |
|---|---:|
| Epic | ۹ |
| Story و Task | ۵۱ |
| Done | ۵۱ |
| In Progress | ۶ |
| In Review | ۱ |
| Backlog | ۲ |

برد پروژه: <span dir="ltr">https://pourmand.atlassian.net/jira/software/projects/EMD/board</span>

Workflow ثبت‌شده شامل Backlog، انتخاب برای Sprint، In Progress، Review/QA و Done است. هر کار اصلی به Epic، Owner، Sprint و Evidence مرتبط شده است.

## وضعیت ثبت‌شده Notion

دانشنامه «امداد یار | دانشنامه پروژه و مدیریت دانش» شامل ۸ صفحه محتوایی، ۵ پایگاه داده و ۷۵ رکورد است.

| پایگاه دانش | محتوای ثبت‌شده |
|---|---|
| Decision Log | تصمیم، زمینه، گزینه‌ها، دلیل، اثر، مالک و شاهد |
| Change Log | قبل و بعد تغییر، دلیل، نتیجه آزمون و فایل مرتبط |
| Risk Register | علت، احتمال، شدت، پاسخ، مالک و وضعیت |
| QA Test Log | سناریو، انتظار، نتیجه واقعی، آزمون‌گر و Issue |
| Stakeholder Feedback | بازخورد، اقدام انجام‌شده، مالک و وضعیت پیگیری |

صفحه اصلی: <span dir="ltr">https://app.notion.com/p/38fd955c965a80c18b7ac3a8fd176cc3</span>

## مالکیت تیمی

| عضو | نقش | حوزه قابل ردیابی |
|---|---|---|
| محمدامین پورمند | Project Lead / ML & System Architect | مدل، API، معماری، انتشار و کنترل علمی |
| محدثه حاتمی کیا | UI / Documentation & QA Coordinator | بازبینی رابط، سناریوهای QA و کنترل مستندات |
| محمدرضا آرمان‌پور | Project Control & Metrics Coordinator | KPI، ریسک، Burndown و پیگیری ذی‌نفعان |

برآورد زمانی مستند تیم ۸۸ ساعت است. Worklog شخصی اعضا تا زمان ایجاد حساب و تأیید هر فرد، جدا از این برآورد و در وضعیت باز نگهداری می‌شود.

## اتصال شواهد

- Issueهای Jira به فایل، گزارش یا کامیت مرتبط لینک شده‌اند.
- رکوردهای Notion دارای Owner، Jira Key و Evidence هستند.
- آخرین انتشار ممیزی‌شده: <span dir="ltr">a8fb828</span>.
- گزارش مرورگر: <span dir="ltr">reports/model/ui_smoke_v7.json</span>.
- گزارش held-out: <span dir="ltr">reports/model/release_validation_v7.json</span>.

## موارد باز

- ثبت تصاویر واقعی رابط Jira و Notion در <span dir="ltr">EMD-55</span>.
- تکمیل Worklog شخصی اعضا در <span dir="ltr">EMD-44</span>.
- اسکن فیزیکی QR و نصب PWA در <span dir="ltr">EMD-52</span>.
- نصب APK روی دستگاه واقعی در <span dir="ltr">EMD-60</span>.
- پاسخ نهایی مراکز درمانی و طراحی پایلوت در <span dir="ltr">EMD-61</span>.

این موارد تا زمان ثبت شاهد مستقل به وضعیت Done منتقل نمی‌شوند.

</div>
