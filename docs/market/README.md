<!-- rtl-normalized -->
<div dir="rtl" align="right">

# بسته انتشار اندروید امداد یار

این پوشه خروجی فنی و محتوایی نسخه ۱.۰.۰ امداد یار برای انتشار آزمایشی در بازارهای اندرویدی را نگهداری می‌کند. برنامه یک WebView آفلاین است؛ رابط فارسی و مدل مرورگری نسخه ۷ داخل APK قرار دارند و ارزیابی بیمار به سرور ارسال نمی‌شود.

## خروجی‌های نهایی

| خروجی | مسیر | کاربرد |
|---|---|---|
| APK امضاشده | `release/Emdadyar-1.0.0-release.apk` | بارگذاری در کافه‌بازار/مایکت و نصب مستقیم |
| AAB امضاشده | `release/Emdadyar-1.0.0-release.aab` | نگهداری برای مارکت‌های پشتیبان App Bundle |
| آیکن ۵۱۲ | `release/Emdadyar-store-icon-512.png` | آیکن صفحه محصول |
| تصویر معرفی ۱۰۲۴×۵۰۰ | `release/Emdadyar-feature-graphic-1024x500.png` | بنر/Feature Graphic صفحه محصول |
| مشخصات و checksum | `release/release-manifest.json` و `release/SHA256SUMS.txt` | کنترل اصالت فایل |
| متن صفحه محصول | `android-market-listing-fa.md` | توضیح کوتاه و کامل |
| پاسخ Data Safety | `store-data-safety-fa.md` | تکمیل فرم حریم خصوصی مارکت |
| گزارش صحت build | `build-verification-fa.md` | شواهد فنی نسخه نهایی |
| راهنمای بازتولید | `android-build-guide.md` | ساخت نسخه‌های بعدی |
| چک‌لیست انتشار | `android-release-checklist.md` | موارد آماده و کارهای پنل مارکت |
| بسته یکپارچه بازار | `Emdadyar_Android_Market_Release_1.0.0.zip` | همه فایل‌های قابل بارگذاری و مستندات بدون کلید خصوصی |

## شناسنامه فنی

- نام بسته: `ir.pourmand.emdadyar`
- نسخه: `1.0.0`، کد نسخه: `1`
- حداقل Android: API 23
- Android هدف: API 36
- مدل: نسخه ۷ با لایه ایمنی سن‌محور `2026.07.2`
- مجوز Android: هیچ مجوز حساسی درخواست نشده است؛ حتی مجوز اینترنت در manifest وجود ندارد.
- وضعیت بالینی: نسخه آزمایشی و آموزشی؛ بدون اعتبارسنجی بالینی و بدون ادعای تشخیص یا درمان.

## کلید انتشار

کلید release و رمز آن خارج از repository و خارج از بسته تحویل عمومی نگهداری می‌شوند. این کلید باید برای تمام به‌روزرسانی‌های آینده حفظ شود؛ گم‌شدن آن می‌تواند انتشار update با همان package name را غیرممکن کند.

## لینک‌های عمومی

- وب‌اپ: `https://aminhatesprogramming.github.io/emergency-triage-mvp/`
- حریم خصوصی: `https://aminhatesprogramming.github.io/emergency-triage-mvp/static/privacy.html`
- مخزن: `https://github.com/AminHatesProgramming/emergency-triage-mvp`

</div>
