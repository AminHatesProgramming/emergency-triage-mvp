# ساختار پیشنهادی سامانه مدیریت دانش

این سند برای انتقال به Notion، Confluence یا Google Docs آماده شده است. معیار استاد شامل ساختار داکیومنت‌ها، API documentation، تصمیمات فنی، صورتجلسات و دانش تولیدشده است.

## ساختار فضای دانش

| صفحه | مالک | وضعیت | توضیح |
|---|---|---|---|
| Project Home | محمدامین | آماده | معرفی، لینک‌ها، وضعیت فعلی |
| Problem & Stakeholders | محمدرضا | آماده | مسئله، ارزش اجتماعی، ذی‌نفعان |
| Architecture | محمدامین | آماده | معماری API-first و ML |
| API Documentation | محمدامین | آماده | endpointها و نمونه payload |
| Model Card | محمدامین | آماده | داده، متریک، محدودیت‌ها |
| Risk Register | محمدرضا | آماده | ریسک‌ها و پاسخ‌ها |
| Agile Dashboard | محمدرضا | آماده | KPI، burndown، velocity |
| Meeting Notes | محدثه | آماده | صورتجلسات اصلی |
| AI Usage Report | محدثه | آماده | نحوه استفاده از AI |
| Final Report & Poster | همه | آماده‌سازی | گزارش نهایی، ویدئو و پوستر |

## شاخص تکمیل Knowledge Base

| معیار | وضعیت |
|---|---|
| ساختار صفحه‌ها مشخص است | کامل |
| API مستند شده است | کامل |
| تصمیمات فنی ثبت شده‌اند | کامل |
| صورتجلسات وجود دارد | کامل |
| ریسک‌ها ثبت شده‌اند | کامل |
| گزارش استفاده از AI وجود دارد | کامل |
| لینک به کد و خروجی‌ها وجود دارد | کامل |

## API Documentation

| Endpoint | Method | هدف |
|---|---|---|
| `/health` | GET | بررسی آماده بودن سرویس |
| `/model-info` | GET | نمایش نسخه مدل و متریک‌ها |
| `/predict` | POST | دریافت داده بیمار و بازگرداندن سطح ریسک |
| `/` | GET | نمایش UI |

نمونه خروجی `/model-info`:

```json
{
  "version": "v6",
  "selected_predictor": "xgboost",
  "test_metrics": {
    "auc": 0.8947,
    "recall": 0.9241,
    "precision": 0.5269,
    "fpr": 0.3598
  }
}
```

نمونه ورودی sparse:

```json
{
  "chief_complaint": "chestpain",
  "age": 63,
  "heart_rate": 112,
  "oxygen_saturation": 91,
  "history_conditions": ["coronathero"]
}
```

نمونه خروجی sparse:

```json
{
  "model_version": "v6",
  "risk_level": "critical",
  "critical_probability": 0.878,
  "data_completeness": 0.5,
  "confidence_band": "medium",
  "missing_recommended_fields": [
    "systolic blood pressure",
    "diastolic blood pressure",
    "respiratory rate",
    "temperature"
  ]
}
```

## Decision Log

| تاریخ | تصمیم | دلیل |
|---|---|---|
| 2026-06-01 | حذف calibration نامناسب | کاهش ریسک FPR بالا و پیچیدگی غیرضروری |
| 2026-06-08 | اضافه کردن سابقه‌های بالینی | قابل دسترسی از EHR/شرح حال و بهبود عملکرد |
| 2026-06-08 | اصلاح دما از Fahrenheit به Celsius | تفسیر بالینی صحیح و defensible |
| 2026-06-08 | انتخاب safety-first threshold | کاهش False Negative در تریاژ |
| 2026-06-08 | حذف race/ethnicity/insurance | کنترل ریسک bias تا قبل از fairness review |

## Meeting Notes پیشنهادی

### جلسه 1: تعریف مسئله

- خروجی: انتخاب مسئله تریاژ اورژانس
- تصمیم: تمرکز روی decision-support، نه جایگزینی متخصص

### جلسه 2: طراحی MVP

- خروجی: API-first و mobile-first
- تصمیم: پشتیبانی از ورودی ناقص

### جلسه 3: ارزیابی مدل

- خروجی: انتخاب v6
- تصمیم: ثبت هر دو mode شامل safety-first و balanced-fpr

### جلسه 4: آماده‌سازی تحویل

- خروجی: پوستر، ویدئو، گزارش و board
- تصمیم: تقسیم ارائه بین سه عضو

### جلسه 5: بازخوانی rubric نهایی

- خروجی: چک‌لیست مادر تحویل
- تصمیم: ساخت اسناد مستقل برای KPI، Burndown، RACI، WBS و Knowledge Base
- ریسک: ناهماهنگی موضوع ثبت‌شده Sheet1 با scope فعلی
- اقدام: ثبت Scope Change Record و آماده‌سازی جمله دفاعی برای ارائه

## قواعد نگهداری دانش

- هر تصمیم مهم باید در `decision-log.md` ثبت شود.
- هر ریسک جدید باید وارد `risk-register.md` شود.
- هر تغییر scope باید در `scope-change-record.md` ثبت شود.
- خروجی هر sprint باید در `status-report.md` یا `agile-dashboard.md` به‌روزرسانی شود.
- نسخه نهایی پوستر و گزارش باید در همین فضای دانش لینک شود.
