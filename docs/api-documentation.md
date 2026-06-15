# API Documentation

Backend با FastAPI پیاده‌سازی شده است.

Base URL در demo محلی:

`http://127.0.0.1:8000`

## GET /health

هدف: بررسی آماده بودن سرویس.

نمونه خروجی:

```json
{
  "status": "ok"
}
```

## GET /model-info

هدف: دریافت نسخه مدل و متریک‌های تست.

نمونه خروجی خلاصه:

```json
{
  "version": "v6",
  "selected_predictor": "xgboost",
  "test_metrics": {
    "auc": 0.894710103871789,
    "average_precision": 0.8033684286814886,
    "recall": 0.9240543822754065,
    "precision": 0.526931846972384,
    "fpr": 0.35979189414862867
  }
}
```

## POST /predict

هدف: دریافت اطلاعات بیمار و بازگشت سطح ریسک.

### فیلدهای ورودی

| فیلد | نوع | اختیاری؟ | توضیح |
|---|---|---|---|
| `age` | number | بله | سن بیمار |
| `gender` | string | بله | Female، Male یا missing |
| `arrivalmode` | string | بله | Walk-in، Ambulance و غیره |
| `chief_complaint` | string | بله | شکایت اصلی مثل chestpain |
| `heart_rate` | number | بله | ضربان قلب |
| `systolic_bp` | number | بله | فشار سیستولی |
| `diastolic_bp` | number | بله | فشار دیاستولی |
| `respiratory_rate` | number | بله | نرخ تنفس |
| `oxygen_saturation` | number | بله | SpO2 |
| `temperature` | number | بله | دما بر حسب Celsius در API |
| `previous_ed_visits` | integer | بله | سابقه مراجعه ED |
| `previous_admissions` | integer | بله | سابقه بستری |
| `previous_surgeries` | integer | بله | سابقه جراحی |
| `history_conditions` | list[string] | بله | سوابق مثل `copd` یا `coronathero` |

### نمونه sparse input

```json
{
  "chief_complaint": "chestpain",
  "age": 63,
  "heart_rate": 112,
  "oxygen_saturation": 91,
  "history_conditions": ["coronathero"]
}
```

### نمونه خروجی

```json
{
  "model_version": "v6",
  "operational_mode": "safety_first_hybrid",
  "model_probability": 0.8181,
  "critical_probability": 0.8779,
  "threshold": 0.2962,
  "risk_level": "critical",
  "triage_band": "ESI 1-2 priority suggested",
  "recommended_action": "Immediate clinical review recommended",
  "explanation": [
    "low oxygen saturation",
    "chief complaint: chestpain",
    "known history: coronary atherosclerosis"
  ],
  "safety_flags": [
    "red flag: chest pain with high-risk cardiac history"
  ],
  "next_best_actions": [
    "notify senior triage nurse or emergency physician",
    "repeat vital signs and keep patient in visible monitored area"
  ],
  "safety_override": true,
  "data_completeness": 0.5,
  "confidence_band": "medium",
  "missing_recommended_fields": [
    "systolic blood pressure",
    "diastolic blood pressure",
    "respiratory rate",
    "temperature"
  ],
  "disclaimer": "Decision-support only; not a replacement for clinical judgment."
}
```

## نکات طراحی API

- همه فیلدهای بالینی اصلی optional هستند تا سیستم با ورودی ناقص هم کار کند.
- خروجی حتماً `data_completeness` و `missing_recommended_fields` دارد.
- `model_probability` خروجی خام مدل است و `critical_probability` خروجی عملیاتی safety-first است.
- `safety_flags` و `next_best_actions` برای توضیح بهتر در شرایط اورژانسی اضافه شده‌اند.
- API خروجی را به صورت decision-support ارائه می‌کند و disclaimer دارد.
- مدل فقط داده‌های triage-time و EHR-safe را استفاده می‌کند.

## GET /docs/...

برای demo، پوشه مستندات با StaticFiles روی `/docs` mount شده است. بنابراین از داخل MVP می‌توان فایل‌های رسمی Word مثل بسته شواهد مدیریت پروژه را باز کرد. این endpoint برای demo و تحویل درسی است و در نسخه واقعی باید با کنترل دسترسی جایگزین شود.

## POST /feedback

هدف: ثبت بازخورد ذی‌نفع یا کاربر برای پوشش feedback loop و نمایش استفاده واقعی از MVP.

نمونه ورودی:

```json
{
  "stakeholder_type": "medical-student",
  "understandability": 4,
  "ui_clarity": 5,
  "disclaimer_clarity": 5,
  "comment": "خروجی قابل فهم بود، اما بهتر است اقدام بعدی کوتاه‌تر نمایش داده شود."
}
```

نمونه خروجی:

```json
{
  "status": "stored",
  "stored_count": 1,
  "export_path": "/feedback/export"
}
```

## GET /feedback-summary

هدف: نمایش تعداد بازخوردهای ثبت‌شده و مسیر خروجی CSV.

## GET /feedback/export

هدف: خروجی CSV از feedbackهای ثبت‌شده در `data/feedback/stakeholder_feedback.csv`.

## قابلیت Case Summary در UI

پس از هر `POST /predict`، UI یک خلاصه کیس قابل copy/print تولید می‌کند که شامل نسخه مدل، احتمال بحرانی، ورودی‌های کلیدی، safety flags، next actions و disclaimer است. این خروجی برای demo و ضمیمه گزارش بازخورد ذی‌نفع استفاده می‌شود.
