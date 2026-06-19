# گزارش وضعیت پروژه

پروژه «سیستم هوشمند پشتیبان تصمیم‌گیری تریاژ اورژانس» اکنون یک MVP قابل اجرا و قابل deploy دارد: مدل `v7`، API با FastAPI، رابط فارسی mobile-first، PWA، فرم بازخورد، مستندات مدیریتی و مسیر انتشار موبایلی. سیستم جایگزین پزشک یا پرستار نیست و فقط نقش decision-support دارد.

## وضعیت فعلی

| بخش | وضعیت | توضیح |
|---|---|---|
| مدل ML | سبز | v7 آموزش داده شد و نسبت به v6 بهبود واقعی دارد. |
| Backend | سبز | `/health`، `/model-info`، `/predict` و feedback endpoints آماده‌اند. |
| Frontend | سبز | فارسی، RTL، mobile-first و PWA-ready است. |
| Deploy | سبز | Dockerfile، Procfile، render.yaml و اجرای LAN آماده شد. |
| مستندات | سبز | Model Card، KPI، deployment guide و poster assets به‌روزرسانی شدند. |
| مدیریت پروژه | سبز | Agile evidence portal، backlog، time tracking و knowledge base structure موجود است. |
| بازخورد واقعی | زرد | فرم و export آماده است؛ هنوز باید بازخورد واقعی جمع‌آوری شود. |

## مقایسه نسخه‌های مدل

| نسخه | AUC | Recall | Precision | FPR | نکته اصلی |
|---|---:|---:|---:|---:|---|
| v2 | 0.8467 | - | - | 0.4870 | calibration نامناسب و FPR بالا |
| v3 | 0.8467 | - | - | - | تنظیم نامناسب XGBoost |
| v5 | 0.8917 | 0.9194 | 0.5275 | 0.3572 | بهبود UI/model و کاهش نسبی خطا |
| v6 | 0.8947 | 0.9241 | 0.5269 | 0.3598 | اصلاح دما، سوابق بالینی و missingness |
| v7 | 0.9041 | 0.9246 | 0.5447 | 0.3352 | بهترین نسخه فعلی، deploy-ready و سبک‌تر |

## متریک‌های تست v7

| معیار | مقدار |
|---|---:|
| AUC | 0.9041 |
| Average Precision | 0.8202 |
| Recall بیماران بحرانی | 0.9246 |
| Precision | 0.5447 |
| FPR | 0.3352 |
| Threshold | 0.3017 |

## دستاوردهای اخیر

- آموزش مدل v7 روی 558,029 رکورد معتبر
- حذف ستون‌های مشکوک به post-triage مثل `*_last`
- اضافه شدن featureهای بالینی قابل دفاع مثل `vital_red_flag_count` و تعامل سن با علائم حیاتی
- کاهش FPR از 0.3598 به 0.3352 همزمان با حفظ Recall
- کاهش حجم مدل عملیاتی به حدود ۲.۵MB
- آماده‌سازی Dockerfile، render.yaml و Procfile
- افزودن `scripts/start_public_webapp.ps1` برای تست روی گوشی در شبکه داخلی
- افزودن صفحه privacy و مستند deployment موبایلی

## شواهد قابل ارائه

- مدل محلی deploy-ready: `models/triage_model_v7.pkl`
- گزارش متریک: `reports/model/metrics_v7.json`
- نمودارها: `reports/model/confusion_matrix_v7.png`، `reports/model/confidence_distribution_v7.png`، `reports/model/shap_summary_v7.png`
- نمودارهای پوستر: `poster-assets/roc-curve.png`، `poster-assets/precision-recall-curve.png`، `poster-assets/model-version-comparison.png`
- راهنمای deploy: `docs/deployment-mobile-webapp.md`
- پورتال شواهد مدیریت پروژه: `docs/evidence-portal/index.html`

## ریسک‌های فعلی

| ریسک | کنترل |
|---|---|
| False Negative برای بیمار بحرانی | threshold safety-first و safety flags |
| False Positive و فشار منابع | operating pointهای balanced و گزارش FPR |
| اتکای بیش از حد به AI | disclaimer، privacy page و decision-support بودن |
| استفاده بدون HTTPS در موبایل | راهنمای deploy ابری و PWA روی HTTPS |
| نبود بازخورد واقعی | feedback form و CSV export آماده است |

## قدم بعدی

1. اجرای وب‌اپ روی گوشی با `scripts/start_public_webapp.ps1`
2. deploy روی یک سرویس HTTPS مثل Render/Railway/VPS
3. جمع‌آوری حداقل ۵ بازخورد واقعی
4. ساخت Android wrapper با TWA یا Capacitor
5. در فاز Laravel، افزودن consent، audit log، auth و panel مدیریت بازخورد
