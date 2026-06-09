# پوستر A0 پروژه

فایل اصلی پوستر:

- `docs/poster/a0-poster.html`
- `docs/poster/current-poster.png`

این نسخه فعلاً از تصویر پوستر ساخته‌شده با ChatGPT به عنوان placeholder استفاده می‌کند تا بعداً با نسخه نهایی جایگزین شود.

نسخه موقت شامل موارد اصلی rubric است:

- عنوان و شرح پروژه
- نمایش محصول
- معماری MVP
- KPIهای فعلی
- ماتریس همکاری و ساعات
- Burndown
- مسیر Agile
- پیش‌بینی جذب کاربر تا پایان تیر
- KPIهای آینده
- ریسک، اخلاق و لینک GitHub

## خروجی PDF / چاپ

برای گرفتن PDF، فایل `a0-poster.html` را در Chrome یا Edge باز کنید و Print بگیرید:

- Paper size: A0
- Layout: Landscape
- Margins: None
- Background graphics: On
- Scale: 100%

یا از اسکریپت زیر استفاده کنید:

```powershell
powershell -ExecutionPolicy Bypass -File .\docs\poster\export-poster.ps1
```
