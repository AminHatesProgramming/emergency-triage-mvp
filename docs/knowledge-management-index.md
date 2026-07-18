<!-- rtl-normalized -->
<div dir="rtl" align="right">

# ساختار اجرایی سامانه مدیریت دانش

مدیریت دانش پروژه در Notion واقعی با ۸ صفحه و ۵ دیتابیس شامل ۷۳ رکورد اجرا شده است. این سند ساختار، مالکیت و قواعد نگهداری آن را به‌صورت قابل بازسازی ثبت می‌کند. صفحه اصلی: <span dir="ltr">https://app.notion.com/p/38fd955c965a80c18b7ac3a8fd176cc3</span>

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
| حاکمیت ابزارهای کمکی | محمدامین / محدثه | آماده | دامنه استفاده، کنترل انسانی و شواهد پذیرش |
| Final Report & Poster | همه | آماده‌سازی | گزارش نهایی، ویدئو و پوستر |

## شاخص تکمیل Knowledge Base

| معیار | وضعیت |
|---|---|
| ساختار صفحه‌ها مشخص است | کامل |
| API مستند شده است | کامل |
| تصمیمات فنی ثبت شده‌اند | کامل |
| صورتجلسات وجود دارد | کامل |
| ریسک‌ها ثبت شده‌اند | کامل |
| حاکمیت ابزارهای کمکی و کنترل انسانی ثبت شده است | کامل |
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
  "version": "v7",
  "selected_predictor": "xgboost_v7_balanced",
  "test_metrics": {
    "auc": 0.9041,
    "recall": 0.9246,
    "precision": 0.5447,
    "fpr": 0.3352
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
  "model_version": "v7",
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

## نقاط هم‌راستاسازی ثبت‌شده

### جلسه 1: تعریف مسئله

- خروجی: انتخاب مسئله تریاژ اورژانس
- تصمیم: تمرکز روی decision-support، نه جایگزینی متخصص

### جلسه 2: طراحی MVP

- خروجی: API-first و mobile-first
- تصمیم: پشتیبانی از ورودی ناقص

### جلسه 3: ارزیابی مدل

- خروجی: انتخاب v7
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
</div>
