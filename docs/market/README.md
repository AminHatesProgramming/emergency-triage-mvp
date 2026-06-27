<!-- rtl-normalized -->
<div dir="rtl" align="right">

# بسته آماده‌سازی انتشار امدادیار

این پوشه برای آماده‌سازی انتشار عمومی امدادیار ساخته شده است. نسخه فعلی محصول یک PWA عمومی و قابل نصب است و با لینک HTTPS روی موبایل اجرا می‌شود.

## خروجی‌های موجود

| خروجی | مسیر |
|---|---|
| لینک عمومی PWA | `https://aminhatesprogramming.github.io/emergency-triage-mvp/` |
| متن آماده مارکت | `docs/market/android-market-listing-fa.md` |
| چک‌لیست انتشار | `docs/market/android-release-checklist.md` |
| راهنمای تبدیل PWA به APK/AAB | `docs/market/twa-build-guide.md` |
| فایل Word ارسال به استاد | `docs/deliverables/Emdadyar_Mobile_App_For_Professor.docx` |
| QR Code | `docs/artifacts/emdadyar-pwa-qr.png` |
| اسکرین‌شات موبایل آماده | `docs/market/screenshots/emdadyar-mobile-critical.png` |
| اسکرین‌شات ورودی ناقص | `docs/market/screenshots/emdadyar-mobile-partial-input.png` |
| اسکرین‌شات دسکتاپ | `docs/market/screenshots/emdadyar-desktop-critical.png` |

## نکته مهم

فایل APK یا AAB در این workspace ساخته نشده است، چون Android SDK، Gradle و `adb` روی سیستم موجود نیستند. برای بازارهایی مثل کافه‌بازار یا مایکت، باید پس از نصب Android Studio/SDK و ساخت signing key، نسخه TWA یا WebView wrapper تولید شود.

</div>
