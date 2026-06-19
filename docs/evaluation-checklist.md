# چک‌لیست ارزیابی استاد

## مسئله و ارزش

- [x] مسئله واقعی و انسانی در حوزه سلامت تعریف شده است.
- [x] ارزش اجتماعی و ملی پروژه توضیح داده شده است.
- [x] سیستم به صورت decision-support معرفی شده، نه جایگزین متخصص.

## مدیریت پروژه

- [x] رویکرد Agile/Scrum سبک توضیح داده شده است.
- [x] backlog و sprintها مستند شده‌اند.
- [x] risk register آماده است.
- [x] status report به‌روز شده است.
- [x] نقش اعضای تیم مشخص و قابل ارائه است.

## مدل و داده

- [x] مدل v7 آموزش داده و ارزیابی شده است.
- [x] train/validation/test جدا هستند.
- [x] threshold روی validation انتخاب شده است.
- [x] داده‌های بعد از تریاژ برای کنترل leakage حذف شده‌اند.
- [x] واحد دما اصلاح شده است.
- [x] سابقه‌های بالینی فقط در صورت قابل دفاع بودن وارد شده‌اند.
- [x] ورودی ناقص پشتیبانی می‌شود.

## متریک‌ها

- [x] AUC تست: 0.9041
- [x] Recall تست: 0.9246
- [x] Average Precision تست: 0.8034
- [x] trade-off بین safety-first و balanced mode توضیح داده شده است.
- [x] FPR و Precision در کنار Recall گزارش شده‌اند.

## محصول

- [x] FastAPI backend آماده است.
- [x] frontend فارسی mobile-first آماده است.
- [x] `/health`، `/model-info` و `/predict` تست شده‌اند.
- [x] سناریوی بحرانی، متوسط و sparse وجود دارد.
- [x] خروجی شامل probability، risk level، explanation و data quality است.

## مستندات

- [x] README
- [x] architecture
- [x] model card
- [x] status report
- [x] final report draft
- [x] AI usage report
- [x] lessons learned
- [x] poster content
- [x] presentation outline

## ریسک‌ها و اخلاق

- [x] False Negative به عنوان ریسک اصلی ثبت شده است.
- [x] disclaimer در UI و docs وجود دارد.
- [x] محدودیت داده ثانویه و نیاز به اعتبارسنجی بالینی گفته شده است.
- [x] متغیرهای حساس تا قبل از fairness review حذف شده‌اند.
