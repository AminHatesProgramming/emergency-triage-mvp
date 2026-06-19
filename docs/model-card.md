# Model Card - Emergency Triage Decision Support

## مشخصات مدل

نام مدل: Emergency Triage Decision-Support Model

نسخه عملیاتی: `v7`

اسکریپت آموزش: `ml/train.py`

خروجی‌های اصلی:

- `models/triage_model_v7.pkl`
- `reports/model/metrics_v7.json`
- `reports/model/confusion_matrix_v7.png`
- `reports/model/confidence_distribution_v7.png`
- `reports/model/shap_summary_v7.png`

## هدف

مدل احتمال بحرانی بودن بیمار را تخمین می‌زند. در این پروژه بیمار بحرانی به صورت `ESI <= 2` تعریف شده است. خروجی مدل فقط decision-support است و جایگزین پزشک، پرستار تریاژ یا پروتکل رسمی بیمارستان نیست.

## داده‌های مجاز در لحظه تریاژ

برای کنترل leakage فقط اطلاعاتی استفاده شده که در لحظه تریاژ یا در شرح حال/پرونده کوتاه اولیه قابل دسترسی است:

- سن، جنسیت و روش ورود
- علائم حیاتی اولیه
- شکایت اصلی بیمار
- سابقه مراجعه، بستری و جراحی
- سابقه‌های بالینی قابل پرسش یا قابل مشاهده در پرونده
- فیچرهای مشتق‌شده بالینی مثل `shock_index`، `pulse_pressure`، `vital_severity_score` و `vital_red_flag_count`
- شاخص‌های missingness برای پشتیبانی از ورودی ناقص

موارد حذف‌شده برای کنترل leakage و اخلاق:

- آزمایش‌ها، داروها، تصویربرداری و disposition بعد از تریاژ
- تشخیص‌های بعدی که در لحظه تریاژ قطعی نیستند
- race/ethnicity/insurance تا قبل از انجام تحلیل fairness
- ستون‌های `*_last` که می‌توانند مربوط به رویدادهای بعد از تریاژ باشند

## بهبودهای v7

- انتخاب سه candidate از XGBoost و انتخاب بهترین مدل فقط روی validation
- افزایش featureهای بالینی قابل دفاع مثل red flag count، hypoxia severe، shock/hypotension و تعامل سن با علائم حیاتی
- کاهش FPR همزمان با حفظ Recall بالای بیماران بحرانی
- سبک شدن artifact عملیاتی به حدود ۲.۵MB برای deploy
- نرمال‌سازی `arrivalmode` و `oxygen_device` برای جلوگیری از mismatch بین UI و featureهای آموزش
- نگهداری operating pointهای مختلف برای سناریوهای safety-first، balanced و high-sensitivity

## معماری مدل

در v7 چند variant از XGBoost آموزش داده شد و روی validation مقایسه شد. predictor عملیاتی:

`xgboost_v7_balanced`

threshold روی validation انتخاب شد و test فقط برای گزارش نهایی استفاده شد. این جداسازی برای جلوگیری از leakage ارزیابی و دفاع علمی پروژه ضروری است.

## متریک‌های تست v7

حالت عملیاتی انتخاب‌شده: `safety_first_mode`

| معیار | مقدار |
|---|---:|
| AUC | 0.9041 |
| Average Precision | 0.8202 |
| Recall | 0.9246 |
| Precision | 0.5447 |
| F1 | 0.6855 |
| FPR | 0.3352 |
| Specificity | 0.6648 |
| Threshold | 0.3017 |

## Operating Points

| حالت | Recall | FPR | Precision | Threshold | کاربرد |
|---|---:|---:|---:|---:|---|
| balanced_fpr_mode | 0.9000 | 0.2852 | 0.5778 | 0.3585 | کاهش فشار منابع |
| safety_first_mode | 0.9246 | 0.3352 | 0.5447 | 0.3017 | پیش‌فرض محصول |
| high_sensitivity_mode | 0.9378 | 0.3744 | 0.5207 | 0.2653 | حساسیت بیشتر |
| max_f1_mode | 0.7719 | 0.1411 | 0.7035 | 0.5706 | تحلیل مقایسه‌ای، نه مناسب تریاژ ایمن |

انتخاب پیش‌فرض safety-first است، چون در تریاژ اورژانس هزینه انسانی False Negative از هزینه بررسی اضافه چند بیمار غیر بحرانی بالاتر است.

## مقایسه با v6

| معیار | v6 | v7 | نتیجه |
|---|---:|---:|---|
| AUC | 0.8947 | 0.9041 | بهتر |
| Average Precision | 0.8034 | 0.8202 | بهتر |
| Recall | 0.9241 | 0.9246 | حفظ/بهبود جزئی |
| Precision | 0.5269 | 0.5447 | بهتر |
| FPR | 0.3598 | 0.3352 | بهتر |

## پشتیبانی از ورودی ناقص

UI و API همه فیلدهای بالینی اصلی را optional نگه می‌دارند. خروجی همیشه شامل موارد زیر است:

- `data_completeness`
- `confidence_band`
- `missing_recommended_fields`
- `safety_flags`
- `next_best_actions`

اگر فقط چند فیلد مثل شکایت اصلی، سن، SpO2 و سابقه قلبی وارد شود، سیستم همچنان ارزیابی اولیه می‌دهد و همزمان محدودیت داده را نشان می‌دهد.

## محدودیت‌ها

- داده آموزشی ثانویه است و برای استفاده واقعی به اعتبارسنجی بالینی نیاز دارد.
- مدل باید زیر نظر متخصص و پروتکل رسمی استفاده شود.
- تحلیل fairness کامل هنوز انجام نشده است.
- این مدل برای demo/pilot مناسب است، نه تصمیم‌گیری درمانی مستقل.

## برنامه بهبود

- جمع‌آوری بازخورد واقعی از کاربران پایلوت
- تحلیل False Negativeها
- تحلیل subgroup برای سن، جنسیت و الگوهای شکایت اصلی
- اتصال Laravel برای consent، audit log و مدیریت بازخورد
- انتشار PWA/TWA روی دامنه HTTPS برای تست موبایلی واقعی
