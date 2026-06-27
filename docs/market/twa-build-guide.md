<!-- rtl-normalized -->
<div dir="rtl" align="right">

# راهنمای تبدیل PWA امدادیار به APK/AAB

مسیر پیشنهادی برای انتشار در بازارهای اندرویدی، ساخت یک wrapper با Trusted Web Activity است. TWA باعث می‌شود همان PWA عمومی با ظاهر نزدیک به اپ native در Android اجرا شود.

## پیش‌نیازها

- Android Studio
- Android SDK
- Gradle
- Node.js
- Bubblewrap CLI
- signing key برای release

## دستورهای پیشنهادی

```powershell
npm install -g @bubblewrap/cli
bubblewrap init --manifest https://aminhatesprogramming.github.io/emergency-triage-mvp/manifest.webmanifest
bubblewrap build
```

در زمان `init` مقدارهای پیشنهادی:

| فیلد | مقدار پیشنهادی |
|---|---|
| Application name | امدادیار |
| Package ID | `ir.pourmand.emdadyar` |
| Launcher name | امدادیار |
| Start URL | `https://aminhatesprogramming.github.io/emergency-triage-mvp/` |
| Theme color | `#064e5f` |

## تست پس از build

```powershell
adb install app-release-signed.apk
```

سپس این سناریوها تست شوند:

1. باز شدن صفحه اصلی بدون خطا
2. سناریوی بیمار پرخطر
3. سناریوی اطلاعات کم
4. نصب/بازگشت از Home Screen
5. نمایش حریم خصوصی
6. نبود درخواست به `localhost`

## محدودیت فعلی

در این workspace به دلیل نبود Android SDK، Gradle و `adb`، build واقعی APK/AAB انجام نشده است. خروجی آماده فعلی، PWA عمومی و بسته آماده انتشار است.

</div>
