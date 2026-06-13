# Technical Decisions

| Date | Decision | Rationale | Impact |
|---|---|---|---|
| 2026-06-01 | Use triage-time data only | مدل باید در لحظه تریاژ قابل دفاع باشد | حذف leakage و افزایش اعتبار پروژه |
| 2026-06-02 | Remove labs/meds/imaging/disposition | این داده‌ها بعد از تریاژ تولید می‌شوند | کاهش AUC احتمالی اما افزایش صداقت علمی |
| 2026-06-08 | Convert temperature from Fahrenheit to Celsius | تفسیر بالینی اشتباه باعث خروجی غیرقابل دفاع می‌شد | بهبود کیفیت feature engineering |
| 2026-06-08 | Use safety-first threshold | هزینه false negative در تریاژ بالاست | Recall به KPI اصلی تبدیل شد |
| 2026-06-10 | Build mobile-first PWA | کاربر واقعی تریاژ بیشتر به موبایل/تبلت نیاز دارد | demo عملیاتی‌تر شد |
| 2026-06-10 | Add safety-first hybrid layer | مدل با ورودی ناقص ممکن است uncertainty داشته باشد | red flagها جداگانه و شفاف گزارش می‌شوند |
| 2026-06-13 | Add feedback capture to MVP | TA روی operationalization و user feedback تاکید کرد | امکان جمع‌آوری شواهد واقعی فراهم شد |
