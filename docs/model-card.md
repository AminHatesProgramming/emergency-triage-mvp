# Model Card - Emergency Triage Decision Support

## مشخصات مدل

نام مدل: Emergency Triage Decision-Support Model

نسخه هدف: `v6`

اسکریپت آموزش: `ml/train.py`

خروجی‌های اصلی:

- `models/triage_model_v6.pkl`
- `reports/model/metrics_v6.json`
- `reports/model/confusion_matrix_v6.png`
- `reports/model/confidence_distribution_v6.png`
- `reports/model/shap_summary_v6.png`

## هدف

مدل احتمال بحرانی بودن بیمار را تخمین می‌زند. در این پروژه بیمار بحرانی به صورت `ESI <= 2` تعریف شده است. خروجی مدل فقط نقش decision-support دارد و جایگزین پزشک، پرستار تریاژ یا پروتکل رسمی بیمارستان نیست.

## داده‌های مجاز در لحظه تریاژ

برای کنترل leakage فقط اطلاعاتی استفاده شده که در لحظه تریاژ یا از پرونده/شرح حال کوتاه قابل دسترسی است:

- سن، جنسیت و روش ورود
- علائم حیاتی اولیه
- شکایت اصلی بیمار (`cc_*`)
- سابقه مراجعه، بستری و جراحی از پرونده
- سابقه‌های بالینی شناخته‌شده مثل فشار خون، دیابت، COPD، نارسایی قلبی و بیماری مزمن کلیه
- فیچرهای مشتق‌شده بالینی مثل `shock_index`، `pulse_pressure` و `vital_severity_score`
- شاخص‌های missingness برای پشتیبانی از ورودی ناقص

موارد حذف‌شده برای کنترل leakage و اخلاق:

- آزمایش‌ها، داروها، تصویربرداری و disposition بعد از تریاژ
- تشخیص‌های بعدی که در لحظه تریاژ قطعی نیستند
- race/ethnicity/insurance تا قبل از انجام تحلیل fairness

## بهبودهای v6

- اصلاح واحد دما: دمای dataset بر حسب Fahrenheit بود و در v6 به Celsius تبدیل می‌شود.
- اضافه شدن سابقه‌های بالینی قابل دفاع از EHR/شرح حال بیمار.
- اضافه شدن missingness features برای اینکه مدل با ۳ یا ۴ ورودی هم رفتار پایدار داشته باشد.
- انتخاب operating mode به صورت safety-first با هدف Recall حداقل `0.925` روی validation.

## معماری مدل

سه مدل tabular آموزش داده می‌شوند و روی validation مقایسه می‌شوند:

- Random Forest
- Extra Trees
- XGBoost

در اجرای نهایی v6، XGBoost بهترین AUC validation را داشت و به عنوان predictor عملیاتی انتخاب شد. threshold روی validation انتخاب شده و test فقط برای گزارش نهایی استفاده شده است.

## متریک‌های تست v6

حالت عملیاتی انتخاب‌شده: `safety_first_mode`

| معیار | مقدار |
|---|---:|
| AUC | 0.8947 |
| Average Precision | 0.8034 |
| Recall | 0.9241 |
| Precision | 0.5269 |
| F1 | 0.6711 |
| FPR | 0.3598 |
| Specificity | 0.6402 |
| Threshold | 0.2962 |

حالت جایگزین برای کاهش فشار منابع:

| حالت | Recall | FPR | Precision | Threshold |
|---|---:|---:|---:|---:|
| balanced_fpr_mode | 0.9190 | 0.3483 | 0.5337 | 0.3077 |
| safety_first_mode | 0.9241 | 0.3598 | 0.5269 | 0.2962 |

انتخاب نهایی safety-first است، چون در تریاژ اورژانس هزینه انسانی False Negative از هزینه بررسی بیشتر چند بیمار غیر بحرانی بالاتر است.

## محدودیت‌ها

- داده آموزشی ثانویه است و برای استفاده واقعی به اعتبارسنجی بالینی نیاز دارد.
- مدل باید زیر نظر متخصص و پروتکل رسمی استفاده شود.
- تحلیل fairness کامل هنوز انجام نشده است.
- فایل مدل به دلیل حجم و حساسیت داده در Git نگهداری نمی‌شود و باید با `python ml/train.py` بازتولید شود.

## برنامه بهبود

- تحلیل False Negativeها
- ارزیابی subgroup برای سن و جنسیت
- گرفتن بازخورد از فرد آشنا با اورژانس
- سبک‌سازی مدل برای deployment آفلاین
