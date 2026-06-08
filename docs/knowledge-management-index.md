# ساختار پیشنهادی سامانه مدیریت دانش

این سند برای انتقال به Notion، Confluence یا Google Docs آماده شده است. معیار استاد شامل ساختار داکیومنت‌ها، API documentation، تصمیمات فنی، صورتجلسات و دانش تولیدشده است.

## ساختار فضای دانش

1. Project Home
2. Problem & Stakeholders
3. Architecture
4. API Documentation
5. Model Card
6. Risk Register
7. Agile Dashboard
8. Meeting Notes
9. AI Usage Report
10. Final Report & Poster

## API Documentation

| Endpoint | Method | هدف |
|---|---|---|
| `/health` | GET | بررسی آماده بودن سرویس |
| `/model-info` | GET | نمایش نسخه مدل و متریک‌ها |
| `/predict` | POST | دریافت داده بیمار و بازگرداندن سطح ریسک |
| `/` | GET | نمایش UI |

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
