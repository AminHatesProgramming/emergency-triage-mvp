<!-- rtl-normalized -->
<div dir="rtl" align="right">

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
| 2026-07-15 | Separate model probability from safety urgency | بالا بردن مصنوعی احتمال مدل، تفسیر خروجی را مخدوش می‌کرد | احتمال خام مدل حفظ شد و فوریت قاعده‌محور جداگانه نمایش داده می‌شود |
| 2026-07-15 | Add age-aware outlier safety rules | یک آستانه ثابت برای نوزاد، کودک و بزرگسال قابل دفاع نبود | قواعد ضربان قلب بر اساس گروه سنی اعمال و مقادیر بسیار دور از محدوده برای تکرار اندازه‌گیری علامت‌گذاری شدند |
| 2026-07-15 | Package an offline signed Android release | نسخه بازار نباید برای ارزیابی به localhost یا اتصال پایدار وابسته باشد | وب‌اپ و مدل در APK/AAB قرار گرفتند؛ هیچ مجوز حساس Android درخواست نشد |
| 2026-07-16 | Limit adaptive thresholds to two validated sparse patterns | کاهش عمومی threshold در ورودی ناقص FPR را تا 0.7840 بالا برد | فقط الگوهای سه و چهارفیلدی اعتبارسنجی‌شده فعال و گزینه core-vitals رد شد |
| 2026-07-16 | Require differential parity before Android packaging | نسخه مرورگر و API نباید در یک بیمار تصمیم متفاوت بدهند | ۱٬۱۶۷ سناریو با صفر اختلاف تصمیمی ثبت شد |
| 2026-07-16 | Keep release evidence separate from clinical claims | ارزیابی گذشته‌نگر داخلی مجوز استفاده درمانی نیست | محدودیت اعتبارسنجی خارجی/بالینی در Model Card، QA و بسته بازار تکرار شد |
</div>
