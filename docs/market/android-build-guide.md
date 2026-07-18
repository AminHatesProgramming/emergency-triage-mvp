<!-- rtl-normalized -->
<div dir="rtl" align="right">

# راهنمای بازتولید APK و AAB امداد یار

## پیش‌نیاز

- JDK 17
- Android SDK Platform 36
- Android Build Tools 36.0.0
- Gradle 8.14.3 یا wrapper پروژه
- کلید release اصلی پروژه و فایل محلی `keystore.properties`

## ساخت وب‌اپ قابل بسته‌بندی

از ریشه repository اجرا شود:

```powershell
C:\Users\Webhouse\Desktop\quera\qenv\Scripts\python.exe scripts\build_pages.py
```

Gradle محتوای `dist/` را هنگام build به `assets/www/` منتقل می‌کند. اگر `dist/index.html` وجود نداشته باشد، build عمداً متوقف می‌شود.

## تنظیم SDK

فایل محلی و ignoreشده `android-app/local.properties`:

```properties
sdk.dir=C:/Users/Webhouse/AppData/Local/Android/Sdk
```

## تنظیم امضا

فایل محلی و ignoreشده `android-app/keystore.properties`:

```properties
storeFile=C:/private/path/emdadyar-release.jks
storePassword=[رمز خصوصی]
keyAlias=emdadyar
keyPassword=[رمز خصوصی]
```

کلید release را هرگز داخل Git، ZIP تحویل یا پیام عمومی قرار ندهید و برای نسخه بعدی کلید جدید نسازید.

## build نهایی

```powershell
cd android-app
.\gradlew.bat assembleRelease bundleRelease --no-problems-report
```

خروجی‌ها:

```text
android-app/app/build/outputs/apk/release/app-release.apk
android-app/app/build/outputs/bundle/release/app-release.aab
```

## بررسی امضا

```powershell
apksigner verify --verbose --print-certs app-release.apk
jarsigner -verify -verbose -certs app-release.aab
```

برای انتشار update، مقدار `versionCode` باید افزایش یابد و همان keystore استفاده شود.

</div>
