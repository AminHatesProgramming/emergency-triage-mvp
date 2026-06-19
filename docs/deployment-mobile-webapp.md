# راهنمای deploy وب‌اپ، موبایل و بازار اندرویدی

## وضعیت فعلی

پروژه اکنون به صورت یک وب‌اپ FastAPI + PWA آماده اجرا است. مدل عملیاتی `v7` داخل `models/triage_model_v7.pkl` نگهداری می‌شود تا deploy بدون دیتاست خام ممکن باشد.

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

مسیر کم‌ریسک و سریع:

1. deploy همین PWA روی HTTPS
2. ساخت Android wrapper با Trusted Web Activity یا Capacitor
3. استفاده از URL وب‌اپ به‌عنوان محتوای اصلی
4. افزودن آیکن، splash screen، privacy policy و متن هشدار پزشکی
5. تست روی حداقل ۵ کاربر پایلوت
6. انتشار آزمایشی در مارکت

برای TWA باید بعد از مشخص شدن package name و SHA-256 امضای اپ، فایل `assetlinks.json` در مسیر زیر قرار بگیرد:

```text
https://your-domain.com/.well-known/assetlinks.json
```

## نقش Laravel در فاز بعد

پیشنهاد معماری این است که ML در Python/FastAPI باقی بماند و Laravel نقش محصولی و عملیاتی بگیرد:

| بخش | نقش |
|---|---|
| FastAPI | inference مدل، `/predict`، `/model-info` |
| Laravel | auth، پنل مدیریت، ثبت بازخورد، audit log، consent، API gateway |
| PWA / Android wrapper | تجربه کاربری موبایل و نصب‌پذیری |
| Database | بازخورد کاربران، تنظیمات نسخه، لاگ‌های غیرحساس |

بازنویسی مدل در Laravel توصیه نمی‌شود. بهتر است Laravel درخواست را به FastAPI proxy کند و خروجی را همراه با audit و consent مدیریت کند.

## چک‌لیست قبل از انتشار عمومی

- [ ] دامنه HTTPS
- [ ] Privacy Policy عمومی
- [ ] متن واضح decision-support بودن
- [ ] حذف هرگونه داده شخصی غیرضروری
- [ ] تست روی Android Chrome
- [ ] ثبت حداقل ۵ بازخورد پایلوت
- [ ] بررسی پاسخ `/health`
- [ ] بررسی پاسخ `/model-info`
- [ ] تست سناریوی بیمار بحرانی
- [ ] تست سناریوی ورودی ناقص

## محدودیت اخلاقی

این محصول هنوز ابزار درمانی تاییدشده نیست. انتشار عمومی باید با عنوان نسخه آزمایشی، آموزشی یا پایلوت انجام شود و خروجی آن نباید جایگزین تصمیم متخصص شود.
