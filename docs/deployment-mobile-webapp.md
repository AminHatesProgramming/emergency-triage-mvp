<!-- rtl-normalized -->
<div dir="rtl" align="right">

# راهنمای deploy وب‌اپ، موبایل و بازار اندرویدی

## وضعیت فعلی

پروژه اکنون به صورت یک وب‌اپ FastAPI + PWA آماده اجرا است. مدل عملیاتی `v7` داخل `models/triage_model_v7.pkl` نگهداری می‌شود تا deploy بدون دیتاست خام ممکن باشد.

علاوه بر نسخه API، یک نسخه public/static هم آماده شده که روی GitHub Pages منتشر می‌شود و مدل v7 را داخل مرورگر اجرا می‌کند:

```text
https://aminhatesprogramming.github.io/emergency-triage-mvp/
```

در این حالت، کاربر با گوشی لینک را باز می‌کند و prediction بدون سرور پایتونی انجام می‌شود. بازخوردها در نسخه static روی همان دستگاه ذخیره می‌شوند؛ برای feedback مرکزی باید backend یا Laravel gateway جدا deploy شود.

## اجرای سریع روی گوشی در شبکه داخلی

روی لپ‌تاپ:

```powershell
cd C:\Users\Webhouse\Desktop\quera\pm
.\scripts\start_public_webapp.ps1
```

اسکریپت URLهای قابل باز کردن روی گوشی را چاپ می‌کند، مثلا:

```text
http://192.168.1.25:8000/
```

گوشی و لپ‌تاپ باید روی یک Wi-Fi باشند. اگر صفحه باز نشد، Windows Firewall باید اجازه دسترسی به پورت `8000` بدهد.

## اجرای ابری با Docker

```powershell
docker build -t emergency-triage-mvp .
docker run --rm -p 8000:8000 emergency-triage-mvp
```

برای VPS یا سرویس‌های Docker-based، فقط باید پورت `8000` یا متغیر `PORT` به سرویس داده شود.

## انتشار عمومی با GitHub Pages

فایل workflow آماده است:

```text
.github/workflows/deploy-pages.yml
```

مراحل:

1. در GitHub وارد repository شوید.
2. از مسیر `Settings > Pages`، Source را روی `GitHub Actions` بگذارید.
3. آخرین push روی branch `main` workflow را اجرا می‌کند.
4. خروجی در آدرس زیر منتشر می‌شود:

```text
https://aminhatesprogramming.github.io/emergency-triage-mvp/
```

ساخت local خروجی Pages:

```powershell
C:\Users\Webhouse\Desktop\quera\qenv\Scripts\python.exe scripts\export_browser_model.py
C:\Users\Webhouse\Desktop\quera\qenv\Scripts\python.exe scripts\build_pages.py
```

خروجی در `dist/` ساخته می‌شود. این پوشه شامل `index.html`، `manifest.webmanifest`، `sw.js`، آیکن‌ها، privacy page و `model-v7.json` است.

## Render / Railway / Heroku-like

فایل‌های آماده:

- `Dockerfile`
- `render.yaml`
- `Procfile`

در Render، repository را وصل کنید و نوع سرویس را Docker Web Service بگذارید. مسیر health check:

```text
/health
```

برای دامنه نهایی، اگر frontend و API روی یک دامنه باشند نیازی به CORS اضافی نیست. اگر Laravel یا frontend جدا روی دامنه دیگر باشد، متغیر زیر را تنظیم کنید:

```text
ALLOWED_ORIGINS=https://your-domain.com,https://api.your-domain.com
```

## نصب PWA روی موبایل

برای تست محلی، صفحه روی گوشی باز می‌شود؛ اما نصب کامل PWA در Android معمولا HTTPS می‌خواهد. مسیر پیشنهادی:

1. deploy روی دامنه HTTPS
2. باز کردن دامنه در Chrome Android
3. انتخاب `Install app` یا `Add to Home screen`
4. تست offline shell، فرم، feedback و endpoint `/model-info`

## مسیر انتشار در بازارهای اندرویدی

مسیر اجراشده برای نسخه `1.0.0`:

1. ساخت PWA عمومی روی HTTPS
2. ساخت Android wrapper بومی با شناسه `ir.pourmand.emdadyar`
3. قرار دادن رابط و مدل v7 داخل بسته برای اجرای آفلاین
4. افزودن آیکن، privacy policy و هشدار استفاده مسئولانه
5. امضای APK/AAB با کلید انتشار و راستی‌آزمایی امضا
6. آماده‌سازی متن، تصویر شاخص و اسکرین‌شات‌های بازار

این نسخه از TWA استفاده نمی‌کند و در نتیجه به `assetlinks.json` یا در دسترس بودن URL برای اجرای اصلی وابسته نیست. آزمون نصب روی دستگاه فیزیکی و انتشار آزمایشی در مارکت هنوز باید با حساب مالک انجام شود.

## نقش سرویس مرکزی در فاز بعد

پیشنهاد معماری این است که ML در Python/FastAPI باقی بماند و Laravel نقش محصولی و عملیاتی بگیرد:

| بخش | نقش |
|---|---|
| FastAPI | inference مدل، `/predict`، `/model-info` |
| Laravel اختیاری | auth، پنل مدیریت، ثبت بازخورد، audit log، consent، API gateway |
| PWA / Android wrapper | تجربه کاربری موبایل و نصب‌پذیری |
| Database | بازخورد کاربران، تنظیمات نسخه، لاگ‌های غیرحساس |

بازنویسی مدل در Laravel توصیه نمی‌شود. در صورت نیاز به سرویس مرکزی، Laravel می‌تواند درخواست را به FastAPI منتقل کند و خروجی را همراه با audit و consent مدیریت کند.

## چک‌لیست قبل از انتشار عمومی

- [x] دامنه HTTPS برای PWA
- [x] Privacy Policy عمومی و نسخه داخل برنامه
- [x] متن واضح decision-support بودن
- [x] عدم دریافت نام، شماره تماس یا شناسه بیمار در نسخه فعلی
- [x] تست رابط در viewport موبایل Chrome
- [x] ثبت ۹ بازخورد کیفی پرستاران تریاژ
- [x] بررسی پاسخ `/health`
- [x] بررسی پاسخ `/model-info`
- [x] تست سناریوی بیمار بحرانی
- [x] تست سناریوی ورودی ناقص
- [x] ساخت و راستی‌آزمایی APK/AAB امضاشده
- [ ] نصب APK روی حداقل یک دستگاه فیزیکی
- [ ] پایلوت کمی با حداقل ۵ کاربر جدید

## محدودیت اخلاقی

این محصول هنوز ابزار درمانی تاییدشده نیست. انتشار عمومی باید با عنوان نسخه آزمایشی، آموزشی یا پایلوت انجام شود و خروجی آن نباید جایگزین تصمیم متخصص شود.
</div>
