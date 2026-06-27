<!-- rtl-normalized -->
<div dir="rtl" align="right">

# چک‌لیست انتشار اندرویدی امدادیار

## آماده در پروژه

| مورد | وضعیت |
|---|---|
| لینک HTTPS عمومی | آماده |
| PWA manifest | آماده |
| Service Worker | آماده |
| آیکن 192 و 512 | آماده |
| توضیح حریم خصوصی | آماده |
| QR Code | آماده |
| متن مارکت | آماده |
| تست public URL | آماده |

## موردهای لازم برای APK/AAB

| مورد | وضعیت فعلی | توضیح |
|---|---|---|
| Android SDK | موجود نیست | باید با Android Studio نصب شود |
| Gradle | موجود نیست | همراه Android Studio یا Gradle نصب شود |
| signing key | موجود نیست | برای انتشار در مارکت ضروری است |
| package name | پیشنهادی | `ir.pourmand.emdadyar` |
| TWA wrapper | نیازمند build | پیشنهاد: Bubblewrap / Trusted Web Activity |
| تست روی دستگاه واقعی | نیازمند گوشی/adb | پس از build انجام شود |

## مراحل پیشنهادی پس از نصب Android Studio

1. Android Studio و Android SDK را نصب کنید.
2. `adb` و `gradle` را در PATH قرار دهید.
3. با ابزار Bubblewrap یا یک پروژه TWA، لینک PWA را wrapper کنید.
4. package name را `ir.pourmand.emdadyar` بگذارید.
5. signing key بسازید و AAB/APK release تولید کنید.
6. روی گوشی واقعی نصب و تست کنید.
7. فایل AAB/APK را همراه متن مارکت، آیکن‌ها و screenshotها در بازار بارگذاری کنید.

## لینک محصول

`https://aminhatesprogramming.github.io/emergency-triage-mvp/`

</div>
