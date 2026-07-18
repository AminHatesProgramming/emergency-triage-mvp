<!-- rtl-normalized -->
<div dir="rtl" align="right">

# راهنمای عملیاتی‌سازی ابزارهای مدیریت پروژه و مدیریت دانش

این سند برای اجرای دقیق خواسته TA است: پروژه باید یک ابزار واقعی برای مدیریت کار شبیه Jira و یک ابزار واقعی برای مدیریت دانش شبیه Notion داشته باشد.

## 1. ابزار مدیریت پروژه: GitHub Issues / GitHub Projects

انتخاب دفاعی: GitHub Issues/Projects برای مقیاس پروژه مناسب‌تر از Jira است، چون کد، commit، issue، task و evidence در یک جا قرار می‌گیرند. این انتخاب معادل سبک Jira است و شامل backlog، sprint، assignee/owner، status، story point و evidence link می‌شود.

### اجرای سریع

پیش‌نیاز:

```powershell
winget install --id GitHub.cli
gh auth login
gh auth refresh -s project
```

سپس:

```powershell
cd C:\Users\Webhouse\Desktop\quera\pm
.\scripts\setup_github_work_management.ps1
```

خروجی:

- GitHub labels برای sprint/status/area
- issueهای واقعی از روی `docs/artifacts/github-issues-seed.csv`
- فایل board قابل import در ابزارهای مشابه: `docs/artifacts/work-management-board.csv`
- time tracking قابل بررسی: `docs/artifacts/time-tracking-log.csv`
- بسته شدن issueهای Done
- ساخت GitHub Project board، اگر scope مربوط به project در GitHub CLI فعال باشد

اگر ساخت Project خطا داد:

```powershell
gh auth refresh -s project
.\scripts\setup_github_work_management.ps1
```

## 2. ابزار مدیریت دانش: Notion Knowledge Base

انتخاب دفاعی: Notion برای Knowledge Base مناسب است چون صفحات تصمیم‌ها، جلسات، Sprint notes، feedback و team playbook را کنار هم نگه می‌دارد.

### اجرای سریع

1. در Notion یک integration بسازید: https://www.notion.so/my-integrations
2. Internal Integration Secret را کپی کنید.
3. یک صفحه parent بسازید، مثلا:
   `Emergency Triage MVP - Knowledge Base`
4. از Share همان صفحه، integration را invite کنید.
5. Page ID را از URL بردارید.

سپس:

```powershell
cd C:\Users\Webhouse\Desktop\quera\pm
$env:NOTION_TOKEN='secret_...'
$env:NOTION_PARENT_PAGE_ID='your_parent_page_id'
python scripts\setup_notion_knowledge_base.py
```

خروجی:

- Notion pages:
  - Project Home
  - Sprint Notes
  - Meeting Notes
  - Technical Decisions
  - Stakeholder Feedback Log
  - Team Playbook
  - Agile Delivery Evidence
- Notion database:
  - Emergency Triage MVP - Task Board
- فایل لینک‌ها:
  - `docs/artifacts/notion-links.json`

## جمله دفاعی آماده برای ارائه

> برای مدیریت پروژه از GitHub Issues/Projects به عنوان ابزار واقعی Work Management استفاده کردیم؛ هر task دارای sprint، owner، status، story point و evidence link است. برای مدیریت دانش نیز Knowledge Base را در Notion ساختیم که شامل sprint notes، meeting notes، technical decisions، stakeholder feedback و team playbook است. بنابراین پروژه فقط یک خروجی فنی نیست و فرآیند Agile و دانش تولیدشده آن قابل مشاهده و قابل ارزیابی است.

## ثبت لینک‌های نهایی

پس از اجرای ابزارها، لینک‌ها را اینجا و در گزارش نهایی ثبت کنید:

| خروجی | لینک |
|---|---|
| GitHub Issues | `https://github.com/AminHatesProgramming/emergency-triage-mvp/issues` |
| GitHub Project Board | بعد از اجرای اسکریپت اینجا قرار گیرد |
| Notion Knowledge Base | بعد از اجرای اسکریپت اینجا قرار گیرد |
| Notion Task Board Database | بعد از اجرای اسکریپت اینجا قرار گیرد |
| Feedback CSV Export | `http://127.0.0.1:8000/feedback/export` |
</div>
