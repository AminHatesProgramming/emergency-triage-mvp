<!-- rtl-normalized -->
<div dir="rtl" align="right">

# راهنمای Deploy عمومی پروژه تریاژ هوشمند اورژانس

این سند برای تبدیل پروژه از اجرای local به وب‌اپ عمومی نوشته شده است؛ یعنی صفحه روی موبایل، ویندوز و هر دستگاه دیگری با لینک HTTPS باز شود و وابسته به سرور local نباشد.

## 1. ساختار پروژه

| بخش | مسیر | توضیح |
|---|---|---|
| FastAPI backend | `backend/main.py` | تعریف اپلیکیشن، CORS، endpointهای `/health`، `/model-info`، `/predict` و feedback |
| schemaهای API | `backend/schemas.py` | ورودی بیمار، خروجی prediction و فرم بازخورد |
| منطق inference | `ml/inference.py` | بارگذاری مدل v7، ساخت featureها، threshold، safety flags و خروجی decision-support |
| مدل اصلی backend | `models/triage_model_v7.pkl` | artifact لازم برای prediction در FastAPI |
| متریک‌های مدل | `reports/model/metrics_v7.json` | گزارش عملکرد v7 برای `/model-info` و مستندات |
| frontend | `frontend/` | HTML/CSS/JS، PWA manifest، service worker، privacy page و assetها |
| مدل داخل مرورگر | `frontend/model-v7.json` | نسخه export شده مدل برای static PWA بدون backend |
| build static frontend | `scripts/build_pages.py` | ساخت خروجی قابل deploy در `dist/` |

هیچ فایل مدل، scaler، encoder، pipeline یا artifact لازم برای prediction حذف نشده است.

## 2. دو مسیر deploy

### مسیر سریع برای گرفتن کاربر: Static PWA

در این مسیر frontend روی GitHub Pages، Vercel یا Netlify منتشر می‌شود و مدل v7 داخل مرورگر اجرا می‌شود. این مسیر بدون سرور Python هم روی گوشی کار می‌کند.

لینک هدف GitHub Pages:

```text
https://aminhatesprogramming.github.io/emergency-triage-mvp/
```

ویژگی‌ها:

- قابل باز شدن روی موبایل و ویندوز با لینک عمومی
- قابل نصب به شکل PWA از Chrome Android یا مرورگرهای پشتیبان
- prediction با `frontend/model-v7.json` داخل مرورگر
- بازخوردها در حالت بدون backend روی همان دستگاه ذخیره می‌شوند

### مسیر کامل‌تر: Backend عمومی + Frontend عمومی

در این مسیر backend روی Render یا Railway منتشر می‌شود و frontend با `API_BASE_URL` به backend وصل می‌شود. این حالت برای ثبت متمرکز feedback و API واقعی بهتر است.

## 3. اجرای local

محیط پروژه `qenv` است:

```powershell
cd C:\Users\Webhouse\Desktop\quera\pm
C:\Users\Webhouse\Desktop\quera\qenv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

تست local:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/model-info
```

## 4. آماده‌سازی backend برای Render

فایل‌های آماده:

- `requirements.txt`
- `Dockerfile`
- `render.yaml`
- `Procfile`

Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

اگر از Dockerfile استفاده شود، همین command داخل Dockerfile تنظیم شده است.

مراحل Render:

1. وارد Render شوید و repository را وصل کنید.
2. گزینه `New Web Service` را بزنید.
3. Runtime را Docker انتخاب کنید.
4. Health check path را روی `/health` بگذارید.
5. متغیر محیطی زیر برای تست اولیه قابل قبول است:

```text
ALLOWED_ORIGINS=*
```

بعد از مشخص شدن دامنه frontend، مقدار بالا را محدود کنید:

```text
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

Endpointهای ضروری بعد از deploy:

```text
https://your-render-service.onrender.com/health
https://your-render-service.onrender.com/model-info
https://your-render-service.onrender.com/predict
```

برای `/predict` باید درخواست `POST` با JSON ارسال شود.

## 5. آماده‌سازی backend برای Railway

فایل آماده:

- `railway.toml`

مراحل Railway:

1. روی Railway پروژه جدید از GitHub بسازید.
2. repository را انتخاب کنید.
3. Railway از `Dockerfile` و `railway.toml` استفاده می‌کند.
4. متغیر محیطی زیر را برای تست اولیه بگذارید:

```text
ALLOWED_ORIGINS=*
```

5. بعد از deploy، آدرس عمومی Railway را تست کنید:

```text
https://your-railway-domain.up.railway.app/health
https://your-railway-domain.up.railway.app/model-info
```

## 6. تنظیم CORS

در `backend/main.py` مقدار `ALLOWED_ORIGINS` از env خوانده می‌شود.

برای تست عمومی:

```text
ALLOWED_ORIGINS=*
```

برای نسخه قابل دفاع‌تر:

```text
ALLOWED_ORIGINS=https://aminhatesprogramming.github.io,https://your-vercel-domain.vercel.app
```

نکته دفاعی: `*` برای pilot و تست اولیه قابل قبول است، اما برای محصول واقعی باید فقط دامنه frontend مجاز باشد.

## 7. تنظیم API در frontend

frontend دیگر به آدرس local وابسته نیست. تنظیمات مرکزی در این فایل است:

```text
frontend/config.js
```

نمونه برای حالت بدون backend:

```js
window.TRIAGE_APP_CONFIG = {
  API_BASE_URL: "",
  BROWSER_MODEL_URL: "static/model-v7.json",
  TRY_SAME_ORIGIN_API: "auto",
};
```

نمونه برای اتصال به backend عمومی:

```js
window.TRIAGE_APP_CONFIG = {
  API_BASE_URL: "https://your-render-service.onrender.com",
  BROWSER_MODEL_URL: "static/model-v7.json",
  TRY_SAME_ORIGIN_API: false,
};
```

در build static، این مقدار می‌تواند از env ساخته شود:

```text
TRIAGE_API_BASE_URL=https://your-render-service.onrender.com
```

همچنین برای سازگاری با محیط‌های frontend، `API_BASE_URL` و `VITE_API_BASE_URL` هم پشتیبانی می‌شوند.

## 8. Deploy frontend روی GitHub Pages

فایل workflow:

```text
.github/workflows/deploy-pages.yml
```

مراحل:

1. در GitHub وارد repository شوید.
2. مسیر `Settings > Pages` را باز کنید.
3. Source را روی `GitHub Actions` قرار دهید.
4. هر push روی `main` خروجی static را deploy می‌کند.
5. لینک عمومی:

```text
https://aminhatesprogramming.github.io/emergency-triage-mvp/
```

اگر backend عمومی جداگانه ساخته شد و خواستید همین GitHub Pages به آن وصل شود، در GitHub از مسیر `Settings > Secrets and variables > Actions > Variables` یک variable با نام زیر بسازید:

```text
TRIAGE_API_BASE_URL=https://your-render-service.onrender.com
```

سپس workflow را دوباره اجرا کنید. اگر این variable خالی باشد، نسخه GitHub Pages به شکل static PWA و بدون backend کار می‌کند.

Build local:

```powershell
C:\Users\Webhouse\Desktop\quera\qenv\Scripts\python.exe scripts\build_pages.py
```

خروجی در `dist/` ساخته می‌شود.

## 9. Deploy frontend روی Vercel

فایل آماده:

```text
vercel.json
```

تنظیمات:

| مورد | مقدار |
|---|---|
| Build Command | `python scripts/build_pages.py` |
| Output Directory | `dist` |
| Install Command | خالی |

اگر backend عمومی دارید، در Environment Variables مقدار زیر را بگذارید:

```text
TRIAGE_API_BASE_URL=https://your-render-service.onrender.com
```

اگر backend ندارید، این env را خالی بگذارید تا نسخه static PWA با مدل مرورگر کار کند.

## 10. Deploy frontend روی Netlify

فایل آماده:

```text
netlify.toml
```

تنظیمات:

| مورد | مقدار |
|---|---|
| Build Command | `python scripts/build_pages.py` |
| Publish Directory | `dist` |
| Python Version | `3.11` |

Environment variable اختیاری برای اتصال به backend:

```text
TRIAGE_API_BASE_URL=https://your-render-service.onrender.com
```

## 11. تست endpointها بعد از deploy

Backend:

```text
GET  https://your-api-domain/health
GET  https://your-api-domain/model-info
POST https://your-api-domain/predict
```

نمونه payload برای `/predict`:

```json
{
  "chief_complaint": "chestpain",
  "age": 63,
  "heart_rate": 112,
  "oxygen_saturation": 91,
  "history_conditions": ["coronathero"]
}
```

Frontend:

```text
https://your-frontend-domain/
```

سناریوهای تست:

- باز شدن صفحه روی موبایل با اینترنت غیرمشترک با لپ‌تاپ
- اجرای سناریوی بیمار بحرانی
- اجرای سناریوی ورودی ناقص
- ثبت feedback
- نصب PWA با `Add to Home screen`

## 12. ساخت QR Code برای لینک frontend

بعد از مشخص شدن لینک نهایی frontend، QR Code را با یکی از این روش‌ها بسازید:

روش سریع آنلاین:

```text
https://www.qr-code-generator.com/
```

روش local با Node، اگر پکیج `qrcode` نصب باشد:

```bash
npx qrcode "https://your-frontend-domain/" -o docs/artifacts/frontend-qr.png
```

لینک QR باید به frontend عمومی اشاره کند، نه backend و نه آدرس local.

## 13. چک‌لیست نهایی

- [x] FastAPI endpointهای اصلی آماده‌اند.
- [x] مدل v7 برای backend در `models/triage_model_v7.pkl` موجود است.
- [x] مدل browser برای static PWA در `frontend/model-v7.json` موجود است.
- [x] frontend از config مرکزی برای API استفاده می‌کند.
- [x] CORS با env قابل تنظیم است.
- [x] Render با `render.yaml` آماده است.
- [x] Railway با `railway.toml` آماده است.
- [x] Vercel با `vercel.json` آماده است.
- [x] Netlify با `netlify.toml` آماده است.
- [x] GitHub Pages workflow آماده است.
- [ ] در GitHub Settings، Pages Source روی `GitHub Actions` تنظیم شود.
- [ ] اگر backend جدا deploy شد، `TRIAGE_API_BASE_URL` در frontend hosting تنظیم شود.

## 14. نکته اخلاقی و محصولی

این سامانه ابزار پشتیبان تصمیم است و جایگزین پزشک، پرستار یا پروتکل رسمی درمانی نیست. برای استفاده واقعی باید اعتبارسنجی بیمارستانی، بررسی محرمانگی داده، تایید متخصص و ارزیابی نهادی انجام شود.
</div>
