<!-- rtl: fa -->
<div dir="rtl" align="right">

# یادداشت‌های جلسات و نقاط هم‌راستاسازی

این سند تصمیم‌های مشترک و اقدام‌های پیگیری را بر پایه مستندات پروژه، تاریخچه Git، Decision Log و Jira ثبت می‌کند. تاریخ‌های زیر «تاریخ مرجع شواهد» هستند و به‌تنهایی اثبات‌کننده برگزاری جلسه یا حضور افراد نیستند. به همین دلیل، به‌جای ادعای حضور، نقش‌های درگیر و خروجی قابل ردیابی ثبت شده‌اند.

## هم‌راستاسازی انتخاب مسئله

| فیلد | مقدار |
|---|---|
| تاریخ مرجع شواهد | <span dir="ltr">2026-06-01</span> |
| نقش‌های درگیر | مدیریت فنی و مدل؛ تحلیل ذی‌نفعان و ارزش اجتماعی؛ طراحی ارائه و تجربه کاربر |
| دستور کار | انتخاب موضوع، ارزش انسانی، امکان مدل‌سازی و تناسب با درس مدیریت پروژه |
| تصمیم‌ها | تمرکز بر اولویت‌بندی تریاژ اورژانس؛ تعریف محصول به‌عنوان پشتیبان تصمیم |
| اقدام‌ها | تدوین Problem Statement، Stakeholder Register و مرز اخلاقی |
| نتیجه | مسئله، دامنه اولیه و گروه‌های ذی‌نفع مستند شدند |
| شواهد | <span dir="ltr">docs/project-management-plan.md</span>، <span dir="ltr">docs/stakeholder-register.md</span> |
| Jira | <span dir="ltr">EMD-11, EMD-12, EMD-13</span> |

## هم‌راستاسازی محدوده و اخلاق پروژه

| فیلد | مقدار |
|---|---|
| تاریخ مرجع شواهد | <span dir="ltr">2026-06-01</span> |
| نقش‌های درگیر | مدل و داده؛ UX و متن محصول؛ مدیریت ریسک |
| دستور کار | تعیین مرز MVP، جلوگیری از ادعای تشخیص و کنترل داده‌های پس از تریاژ |
| تصمیم‌ها | هشدار اخلاقی در UI و مستندات الزامی شد؛ ویژگی‌های post-triage از مدل حذف شدند |
| اقدام‌ها | کنترل data leakage، بازنویسی پیام‌های ایمنی و ثبت ریسک اخلاقی |
| نتیجه | مرز decision-support در Model Card، Privacy و UI یکسان شد |
| شواهد | <span dir="ltr">docs/model-card.md</span>، <span dir="ltr">frontend/privacy.html</span>، Risk Register |
| Jira | <span dir="ltr">EMD-13, EMD-17, EMD-34</span> |

## هم‌راستاسازی داده و مدل

| فیلد | مقدار |
|---|---|
| تاریخ مرجع شواهد | <span dir="ltr">2026-06-08</span> |
| نقش‌های درگیر | توسعه مدل؛ KPI و مدیریت ریسک |
| دستور کار | نسخه‌های مدل، Threshold و trade-off میان Recall و FPR |
| تصمیم‌ها | Recall به‌عنوان معیار ایمنی اصلی و FPR به‌عنوان هزینه عملیاتی همزمان گزارش شوند |
| اقدام‌ها | آموزش و ارزیابی نسخه‌ها، تثبیت v7 و تهیه KPI Register |
| نتیجه | مدل v7 با AUC=0.9041، Recall=0.9246، Precision=0.5447 و FPR=0.3352 ثبت شد |
| شواهد | <span dir="ltr">reports/model/metrics_v7.json</span>، <span dir="ltr">docs/kpi-register.md</span> |
| Jira | <span dir="ltr">EMD-16..EMD-20, EMD-57</span> |

## هم‌راستاسازی رابط و خروجی قابل فهم

| فیلد | مقدار |
|---|---|
| تاریخ مرجع شواهد | <span dir="ltr">2026-06-21</span> |
| نقش‌های درگیر | UX و QA؛ اتصال مدل و API |
| دستور کار | ساده‌سازی فرم، طراحی mobile-first، نمایش نتیجه و سناریوهای آماده |
| تصمیم‌ها | رابط فارسی RTL؛ نمونه‌های آزمایشی جدا از فرم؛ نمایش هشدار، اقدام بعدی و کامل‌بودن داده |
| اقدام‌ها | بازبینی UX، پیاده‌سازی سناریوها و هماهنگی خروجی مرورگر/API |
| نتیجه | نسخه عمومی PWA با مسیر ساده و خروجی قابل توضیح منتشر شد |
| شواهد | <span dir="ltr">frontend/index.html</span>، <span dir="ltr">frontend/app.js</span>، <span dir="ltr">frontend/manifest.webmanifest</span> |
| Jira | <span dir="ltr">EMD-26..EMD-32, EMD-51</span> |

## هم‌راستاسازی نقش‌ها و مسئولیت‌ها

| فیلد | مقدار |
|---|---|
| نقش‌های تعریف‌شده | محمدامین: مدل، API و معماری؛ محدثه: UI، مستندات و QA؛ محمدرضا: KPI، ریسک، Burndown و بازخورد |
| دستور کار | تفکیک مالکیت خروجی‌ها و آماده‌سازی بخش قابل ارائه برای هر عضو |
| تصمیم‌ها | Owner هر کار در Jira و مسئول هر رکورد در Notion مشخص باشد |
| اقدام‌ها | تکمیل Collaboration Matrix، Labelهای Owner و Time Tracking |
| نتیجه | تقسیم نقش در مستندات و Jira ثبت شد؛ تکمیل Time Tracking در EMD-44 باز است |
| شواهد | <span dir="ltr">docs/team-collaboration-matrix.md</span>، Jira EMD |
| Jira | <span dir="ltr">EMD-44, EMD-59</span> |

## هم‌راستاسازی شواهد مدیریت پروژه

| فیلد | مقدار |
|---|---|
| تاریخ مرجع شواهد | <span dir="ltr">2026-06-13</span> |
| دستور کار | تکمیل Backlog، Sprint، KPI، Risk، Feedback، Time Tracking و Knowledge Base |
| تصمیم‌ها | Jira و Notion واقعی به‌عنوان منبع شواهد استفاده شوند؛ موارد بدون شاهد باز بمانند |
| اقدام‌ها | ساخت Project EMD، ایجاد دیتابیس‌های Notion و اتصال Evidenceها |
| نتیجه | ساختار مدیریت پروژه و دانشنامه ایجاد و همگام شد |
| کار باز | تکمیل Burndown در EMD-43، Time Tracking در EMD-44 و تصاویر رابط در EMD-55 |
| شواهد | Jira EMD، Notion Project Knowledge Base، <span dir="ltr">project-management-final-package/</span> |
| Jira | <span dir="ltr">EMD-41..EMD-50, EMD-55, EMD-59</span> |

## هم‌راستاسازی پوستر و تحویل

| فیلد | مقدار |
|---|---|
| تاریخ مرجع شواهد | <span dir="ltr">2026-06-15</span> تا Final Release |
| دستور کار | انتخاب محتوای پوستر A0 و بسته تحویل استاد |
| تصمیم‌ها | استفاده از متریک‌های v7، تصاویر واقعی UI، KPI، Burndown، QR و محدودیت‌های محصول |
| اقدام‌ها | آماده‌سازی نمودارها، QR، فایل‌های Word، بسته Android و راهنمای ارائه |
| نتیجه | دارایی‌های پوستر و بسته تحویل آماده شدند؛ تصاویر Jira/Notion و تست دستگاه واقعی باز هستند |
| شواهد | <span dir="ltr">poster-assets/</span>، <span dir="ltr">docs/deliverables/</span>، <span dir="ltr">docs/market/release/</span> |
| Jira | <span dir="ltr">EMD-53..EMD-55, EMD-60</span> |

## وضعیت پیگیری نهایی

- شواهد فنی، مدل، PWA و بسته Android ثبت شده‌اند.
- ۹ بازخورد کاربردپذیری پرستاران تریاژ از اعتبارسنجی بالینی تفکیک شده‌اند.
- <span dir="ltr">EMD-43</span> در Review است؛ <span dir="ltr">EMD-44</span>، <span dir="ltr">EMD-52</span> و <span dir="ltr">EMD-55</span> در حال انجام‌اند؛ <span dir="ltr">EMD-60</span> و <span dir="ltr">EMD-61</span> در Backlog باقی می‌مانند.
- هیچ همکاری درمانی، نصب دستگاه واقعی یا حضور جلسه‌ای بدون شاهد مستقل به‌عنوان انجام‌شده گزارش نمی‌شود.

</div>
