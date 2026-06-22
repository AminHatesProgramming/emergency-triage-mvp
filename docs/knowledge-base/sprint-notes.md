<!-- rtl-normalized -->
<div dir="rtl" align="right">

# Sprint Notes

## Sprint 0 - Project Framing

Goal: تعریف مسئله، pivot و ارزش انسانی پروژه.

Deliverables:
- `docs/scope-change-record.md`
- `docs/stakeholder-register.md`
- `docs/project-idea-one-page.md`

Review:
- موضوع از ایده شبکه اجتماعی بازی‌محور به تریاژ هوشمند تغییر کرد، چون با بحران، ارزش اجتماعی و KPIهای کمی هم‌راستاتر بود.

## Sprint 1 - Model Baseline

Goal: ساخت baseline مدل و کنترل leakage.

Deliverables:
- مدل‌های اولیه v2/v3
- مستندات model card اولیه
- حذف داده‌های post-triage مثل labs، meds، imaging و disposition

Review:
- یادگیری اصلی این بود که AUC بالا بدون triage-time بودن داده، قابل دفاع نیست.

## Sprint 2 - API MVP

Goal: عملیاتی کردن مدل از طریق API.

Deliverables:
- `backend/main.py`
- `backend/schemas.py`
- endpointهای `/health`, `/model-info`, `/predict`

Review:
- محصول از notebook/model به سرویس قابل demo تبدیل شد.

## Sprint 3 - v6 and Metrics

Goal: رسیدن به نسخه قابل دفاع مدل.

Deliverables:
- `reports/model/metrics_v6.json`
- `docs/model-card.md`
- `docs/kpi-register.md`

Review:
- Recall هدف پاس شد و حالت safety-first به عنوان mode عملیاتی انتخاب شد.

## Sprint 4 - Mobile/PWA and Delivery Package

Goal: تبدیل MVP به تجربه mobile-first قابل ارائه.

Deliverables:
- `frontend/manifest.webmanifest`
- `frontend/sw.js`
- `frontend/assets/app-icon.svg`
- Word deliverables in `docs/deliverables/`

Review:
- اپ روی موبایل قابل نصب شد و با چند ورودی محدود هم خروجی قابل فهم می‌دهد.

## Sprint 5 - PM Evidence and Stakeholder Feedback

Goal: پوشش نقد TA درباره مدیریت پروژه، ابزارها و بازخورد کاربر.

Deliverables:
- `docs/agile-delivery-evidence.md`
- `docs/artifacts/github-issues-seed.csv`
- `docs/knowledge-base/stakeholder-feedback-log.md`
- feedback capture in MVP

Review criteria:
- حداقل 5 feedback واقعی جمع‌آوری شود.
- GitHub Issues/Project view با taskها و ownerها قابل نمایش باشد.
- در ارائه، نقش هر عضو تیم با یک بخش ساده و قابل توضیح مشخص شود.
</div>
