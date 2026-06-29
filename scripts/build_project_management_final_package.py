# -*- coding: utf-8 -*-
"""Build the final Notion/Jira transfer package for Emdadyar.

The generated files are deliberately honest about missing real-world evidence:
no Jira/Notion screenshot, meeting, or stakeholder feedback is claimed as real
unless it is already backed by repository files or git history.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "project-management-final-package"
METRICS_PATH = ROOT / "reports" / "model" / "metrics_v7.json"

APP_URL = "https://aminhatesprogramming.github.io/emergency-triage-mvp/"
REPO_URL = "https://github.com/AminHatesProgramming/emergency-triage-mvp"
JIRA_WORKSPACE_URL = "https://pourmand.atlassian.net/jira/for-you"
JIRA_PROJECT_PLACEHOLDER = "نیاز به تکمیل دارد: پس از ساخت پروژه در Jira لینک دقیق project/board را اینجا قرار دهید."
NOTION_PLACEHOLDER = "نیاز به تکمیل دارد: پس از ساخت Workspace/Page در Notion لینک صفحه اصلی را اینجا قرار دهید."

TEAM = [
    ("محمدامین پورمند", "Project Lead / ML & System Architect"),
    ("محدثه حاتمی کیا", "UI / Documentation & QA Coordinator"),
    ("محمدرضا آرمان‌پور", "Project Control & Metrics Coordinator"),
]

RTL_OPEN = '<!-- rtl: fa -->\n<div dir="rtl" align="right">\n\n'
RTL_CLOSE = "\n</div>\n"


def load_metrics() -> dict:
    with METRICS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


METRICS = load_metrics()
TEST_METRICS = METRICS["test_metrics"]
SAFETY_POINT = METRICS["operating_points"]["safety_first_mode"]["test_metrics"]


def ltr(text: str) -> str:
    return f'<span dir="ltr">{text}</span>'


def md_file(name: str, body: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    text = RTL_OPEN + dedent(body).strip() + RTL_CLOSE
    (OUT / name).write_text(text + "\n", encoding="utf-8")


def plain_md_file(name: str, body: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(dedent(body).strip() + "\n", encoding="utf-8")


def csv_file(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def build_notion_home() -> None:
    team_rows = "\n".join(f"| {member} | {role} |" for member, role in TEAM)
    md_file(
        "notion-home.md",
        f"""
        # امداد یار | دانشنامه پروژه و مدیریت دانش

        ## معرفی کوتاه

        «امداد یار» یک سامانه هوشمند ارزیابی اولیه و اولویت‌بندی آسیب‌دیدگان در شرایط اورژانسی است. هدف محصول کمک به تصمیم‌گیری سریع‌تر در تریاژ، با تمرکز بر داده‌های قابل دسترس در لحظه ارزیابی اولیه است. این سامانه ابزار پشتیبان تصمیم است و جایگزین متخصص، پرستار تریاژ یا پروتکل رسمی درمانی نیست.

        ## مسئله

        در محیط‌های شلوغ اورژانس، فشار زمانی، کمبود منابع و وابستگی زیاد به تجربه فردی می‌تواند باعث تأخیر در شناسایی بیمار پرخطر شود. پروژه تلاش می‌کند با یک MVP قابل اجرا، احتمال از دست رفتن بیمار بحرانی را کاهش دهد و همزمان محدودیت‌ها و مسئولیت اخلاقی را شفاف نگه دارد.

        ## راه‌حل

        محصول از فرم فارسی و راست‌به‌چپ، نمونه‌های آماده تست، مدل v7، ارزیابی با ورودی ناقص، هشدارهای مهم، اقدام بعدی، خلاصه کیس، نصب PWA و لینک عمومی استفاده می‌کند. نسخه public روی GitHub Pages بدون نیاز به سرور local قابل باز شدن است.

        ## ارزش انسانی و اجتماعی

        ارزش اصلی پروژه کاهش احتمال تأخیر در رسیدگی به بیمار پرخطر، کمک به تصمیم‌گیری در شرایط فشار، و ساخت یک نمونه بومی و قابل دفاع از کاربرد مسئولانه AI در سلامت است. در دفاع نهایی باید تأکید شود که پروژه صرفاً فنی نیست؛ بلکه با backlog، sprint، KPI، risk register، AI usage report، QA و برنامه جذب بازخورد پیش رفته است.

        ## لینک‌های اصلی

        | مورد | لینک / مسیر | وضعیت |
        |---|---|---|
        | اپ عمومی امداد یار | {ltr(APP_URL)} | آماده |
        | ریپازیتوری GitHub | {ltr(REPO_URL)} | آماده |
        | Jira Workspace | {ltr(JIRA_WORKSPACE_URL)} | موجود |
        | Jira Project / Board | {JIRA_PROJECT_PLACEHOLDER} | نیاز به تکمیل |
        | Notion Home | {NOTION_PLACEHOLDER} | نیاز به تکمیل |

        ## صفحات مهم Notion که باید ساخته شوند

        | صفحه | فایل آماده انتقال |
        |---|---|
        | معرفی و دانشنامه اصلی | {ltr("project-management-final-package/notion-home.md")} |
        | نمای کلی پروژه | {ltr("project-management-final-package/notion-project-overview.md")} |
        | قابلیت‌های محصول | {ltr("project-management-final-package/notion-product-features.md")} |
        | Sprint Notes | {ltr("project-management-final-package/notion-sprint-notes.md")} |
        | Meeting Notes | {ltr("project-management-final-package/notion-meeting-notes.md")} |
        | AI Usage Report | {ltr("project-management-final-package/notion-ai-usage-report.md")} |
        | Lessons Learned | {ltr("project-management-final-package/notion-lessons-learned.md")} |
        | Decision Log Database | {ltr("project-management-final-package/notion-decision-log.csv")} |
        | Change Log Database | {ltr("project-management-final-package/notion-change-log.csv")} |
        | Risk Register Database | {ltr("project-management-final-package/notion-risk-register.csv")} |
        | Stakeholder Feedback Database | {ltr("project-management-final-package/notion-stakeholder-feedback.csv")} |
        | QA Test Log Database | {ltr("project-management-final-package/notion-qa-test-log.csv")} |

        ## وضعیت فعلی پروژه

        | بخش | وضعیت | شاهد |
        |---|---|---|
        | مدل عملیاتی | v7، AUC={TEST_METRICS["auc"]:.4f}، Recall={TEST_METRICS["recall"]:.4f} | {ltr("reports/model/metrics_v7.json")} |
        | API | Endpointهای {ltr("/health")}، {ltr("/model-info")} و {ltr("/predict")} | {ltr("backend/main.py")} |
        | UI | فارسی، راست‌به‌چپ، mobile-first، قابل نصب به شکل PWA | {ltr("frontend/index.html")} |
        | نسخه عمومی | GitHub Pages با مدل مرورگر | commit {ltr("a1ec91f")} و {ltr("43737c8")} |
        | مستندات مدیریت پروژه | Sprint، KPI، Risk، Burndown، Evidence و Deliverables | {ltr("docs/")} |
        | بازخورد ذی‌نفعان | بازخورد خارجی تأییدشده هنوز نیاز به تکمیل دارد؛ ۹ بازخورد پرستار تریاژ در وضعیت pending confirmation است | {ltr("docs/triage-nurse-feedback-confirmation.md")} |

        ## اعضای تیم

        | عضو | نقش |
        |---|---|
        {team_rows}

        ## هشدار اخلاقی

        امداد یار خروجی تشخیصی قطعی تولید نمی‌کند. خروجی سامانه باید فقط به عنوان کمک تصمیم‌گیری اولیه تفسیر شود و تصمیم نهایی با متخصص، پرستار تریاژ و پروتکل رسمی مرکز درمانی است.
        """,
    )


def build_project_overview() -> None:
    md_file(
        "notion-project-overview.md",
        f"""
        # نمای کلی پروژه امداد یار

        ## هدف پروژه

        هدف پروژه ساخت MVP یک سامانه پشتیبان تصمیم برای ارزیابی اولیه و اولویت‌بندی آسیب‌دیدگان در شرایط اورژانسی است. تمرکز محصول روی تشخیص قطعی نیست؛ تمرکز روی کمک به شناسایی سریع‌تر وضعیت‌های پرخطر، نمایش دلیل‌های قابل فهم، و پیشنهاد اقدام بعدی برای کاربر است.

        ## محدوده محصول

        محدوده نسخه فعلی شامل دریافت اطلاعات اولیه بیمار، اجرای مدل v7 یا مدل مرورگر، نمایش سطح فوریت رسیدگی، هشدارهای مهم، اقدام بعدی، فیلدهای پیشنهادی باقی‌مانده، خلاصه قابل کپی/چاپ و نصب PWA است. نسخه عمومی با لینک GitHub Pages قابل باز شدن است.

        ## خارج از محدوده

        | مورد | دلیل خروج از محدوده |
        |---|---|
        | تشخیص پزشکی قطعی | ریسک اخلاقی و نیاز به اعتبارسنجی بالینی |
        | اتصال به پرونده بیمار واقعی | نیازمند مجوز، محرمانگی و زیرساخت بیمارستانی |
        | استفاده از داده‌های پس از تریاژ مثل آزمایش و تصویربرداری | جلوگیری از data leakage |
        | تصمیم درمانی خودکار | مغایر با نقش decision-support |
        | ادعای بازخورد واقعی بدون شاهد | برای حفظ صداقت پروژه |

        ## کاربران هدف

        | گروه | نیاز اصلی |
        |---|---|
        | پرستار تریاژ | دریافت提示 سریع و قابل فهم در شرایط فشار |
        | تیم اورژانس / درمانگاه | اولویت‌بندی بهتر در ازدحام |
        | مدیریت بحران | سناریوی کمک تصمیم در شرایط حادثه جمعی |
        | استاد و ارزیاب درس | مشاهده یک پروژه Agile با artifactهای قابل دفاع |
        | کاربران پایلوت آموزشی | تست فهم UI و زبان خروجی |

        ## مسئله‌ای که حل می‌شود

        تریاژ دستی در شرایط پرترافیک می‌تواند به تجربه فردی، خستگی، ازدحام و فشار زمانی وابسته شود. امداد یار با یک مدل ارزیابی اولیه و UI ساده تلاش می‌کند هشدارهای مهم و اقدام بعدی را سریع‌تر در دید کاربر قرار دهد.

        ## ارزش پروژه

        | نوع ارزش | توضیح |
        |---|---|
        | انسانی | کاهش احتمال تأخیر در رسیدگی به بیمار پرخطر |
        | اجتماعی | کمک به استفاده مسئولانه از AI در سلامت |
        | ملی | حرکت به سمت نمونه‌های بومی و قابل توسعه برای شرایط کشور |
        | آموزشی | نمایش مدیریت پروژه، Agile، KPI، ریسک و مستندسازی تیمی |
        | فنی | مدل v7، API، PWA، مدل مرورگر و کنترل data leakage |

        ## وضعیت MVP

        | بخش | وضعیت |
        |---|---|
        | مدل | آماده؛ نسخه v7 با AUC={TEST_METRICS["auc"]:.4f} و Recall={TEST_METRICS["recall"]:.4f} |
        | Backend | آماده demo و deploy؛ FastAPI |
        | Frontend | آماده؛ فارسی، responsive، PWA |
        | Public access | آماده؛ {ltr(APP_URL)} |
        | مستندات | گسترده و قابل انتقال به Notion/Jira |
        | بازخورد واقعی خارجی | نیاز به تکمیل دارد |
        | Jira واقعی | نیاز به ساخت board و import CSV دارد |
        | Notion واقعی | نیاز به ساخت صفحه‌ها و import database دارد |

        ## محدودیت‌ها

        - مدل روی داده ثانویه/آموزشی توسعه یافته و برای استفاده واقعی نیازمند اعتبارسنجی بالینی است.
        - خروجی برای تصمیم درمانی مستقل کافی نیست.
        - بازخورد خارجی تأییدشده باید پیش از ارائه نهایی جمع‌آوری و ثبت شود.
        - screenshot واقعی Jira و Notion فقط پس از ساخت واقعی board/workspace قابل ارائه است.
        - تحلیل fairness کامل هنوز انجام نشده و باید در فاز بعدی اضافه شود.
        """,
    )


def build_product_features() -> None:
    features = [
        {
            "title": "فرم اطلاعات بیمار",
            "what": "فرم اصلی دریافت داده‌های اولیه بیمار شامل سن، جنسیت، روش ورود، علائم حیاتی و سوابق قابل پرسش.",
            "why": "کاربر باید بتواند بدون پیچیدگی و با سرعت اطلاعات اولیه را وارد کند.",
            "problem": "پراکندگی داده‌ها و فشار زمانی در تریاژ.",
            "how": "کاربر فقط فیلدهای در دسترس را پر می‌کند و فیلدهای خالی مانع ارزیابی اولیه نمی‌شوند.",
            "effect": "کاهش اصطکاک ورود اطلاعات و پشتیبانی از سناریوی داده ناقص.",
            "status": "آماده در UI نهایی.",
            "next": "اضافه کردن validation بالینی نرم برای مقادیر بسیار غیرواقعی.",
            "evidence": "frontend/index.html، frontend/app.js، commit 43737c8",
        },
        {
            "title": "شکایت اصلی",
            "what": "انتخاب شکایت اصلی مثل تنگی نفس، درد قفسه سینه، تب، درد شکم، سردرد، سقوط و ضعف عمومی.",
            "why": "شکایت اصلی یکی از مهم‌ترین ورودی‌های قابل دسترس در زمان تریاژ است.",
            "problem": "مدل بدون شکایت اصلی بخشی از زمینه بالینی را از دست می‌دهد.",
            "how": "کاربر از یک فهرست ساده فارسی گزینه مناسب را انتخاب می‌کند.",
            "effect": "بهبود فهم کیس و فعال شدن برخی هشدارهای ریسک.",
            "status": "آماده.",
            "next": "افزایش گزینه‌ها پس از دریافت بازخورد پرستاران تریاژ.",
            "evidence": "frontend/index.html، reports/model/metrics_v7.json",
        },
        {
            "title": "علائم حیاتی",
            "what": "ضربان قلب، فشار خون، نرخ تنفس، اکسیژن خون و دما.",
            "why": "علائم حیاتی پایه‌ترین داده‌های در دسترس و قابل دفاع در تریاژ هستند.",
            "problem": "در شلوغی ممکن است بعضی علائم ناقص باشند یا نیاز به تکرار داشته باشند.",
            "how": "فیلدها optional هستند و مدل missingness را هم لحاظ می‌کند.",
            "effect": "امکان ارزیابی اولیه حتی با چند آیتم محدود.",
            "status": "آماده و تست‌شده در سناریوی sparse.",
            "next": "نمایش هشدار برای اندازه‌گیری مجدد در داده‌های ناسازگار.",
            "evidence": "ml/inference.py، frontend/app.js، docs/model-card.md",
        },
        {
            "title": "سابقه بالینی قابل پرسش",
            "what": "چک‌باکس‌های سابقه‌هایی مثل فشار خون، دیابت، COPD، آسم، نارسایی قلبی، عروق کرونر و بیماری کلیه.",
            "why": "این داده‌ها معمولاً از بیمار/همراه یا پرونده کوتاه قابل پرسش هستند.",
            "problem": "سوابق پرخطر می‌توانند در تصمیم تریاژ مؤثر باشند ولی نباید به داده‌های آینده وابسته شوند.",
            "how": "کاربر سابقه‌های شناخته‌شده را انتخاب می‌کند؛ خالی بودن به معنی نبود قطعی سابقه نیست.",
            "effect": "افزایش زمینه تصمیم بدون ایجاد data leakage.",
            "status": "آماده.",
            "next": "تفکیک سابقه قطعی، مشکوک و نامشخص.",
            "evidence": "frontend/index.html، reports/model/metrics_v7.json",
        },
        {
            "title": "نمونه‌های آماده تست",
            "what": "سناریوهای آماده: بیمار پرخطر، بیمار متوسط، اطلاعات کم، درد قفسه سینه.",
            "why": "برای demo و QA لازم است استاد و کاربر سریع رفتار سیستم را ببینند.",
            "problem": "کاربر تازه‌وارد ممکن است برای اولین تست نداند چه داده‌ای وارد کند.",
            "how": "در پایین فرم قرار گرفته تا با ورودی اصلی اشتباه گرفته نشود.",
            "effect": "بهبود demo و کاهش خطای کاربر در شروع.",
            "status": "آماده در UI نهایی.",
            "next": "اضافه کردن سناریوی تصادف/سقوط پس از بازخورد پایلوت.",
            "evidence": "frontend/app.js، frontend/index.html، commit 43737c8",
        },
        {
            "title": "ارزیابی بیمار",
            "what": "دکمه اصلی اجرای ارزیابی و ارسال داده به API یا مدل مرورگر.",
            "why": "کاربر باید یک action واضح برای دریافت خروجی داشته باشد.",
            "problem": "ابهام در اینکه چه زمانی فرم کامل و قابل ارسال است.",
            "how": "با کلیک روی «ارزیابی بیمار»، سیستم داده‌ها را بررسی و نتیجه را نمایش می‌دهد.",
            "effect": "جریان کار ساده و قابل آموزش.",
            "status": "آماده.",
            "next": "نمایش زمان پاسخ در فاز پایلوت.",
            "evidence": "frontend/index.html، frontend/app.js",
        },
        {
            "title": "نتیجه ارزیابی",
            "what": "نمایش نتیجه به زبان ساده با درصد ریسک، وضعیت اقدام و سطح اطمینان.",
            "why": "خروجی باید برای کاربر غیر فنی و در شرایط فشار قابل فهم باشد.",
            "problem": "عبارت‌هایی مثل ESI به‌تنهایی برای همه کاربران شفاف نیستند.",
            "how": "عبارت‌های فارسی مثل «نیازمند بررسی فوری» و «ادامه ارزیابی معمول» نمایش داده می‌شود.",
            "effect": "کاهش سوءبرداشت و افزایش سرعت فهم.",
            "status": "آماده در نسخه نهایی.",
            "next": "تست خوانایی با پرستاران تریاژ و کاربران عمومی.",
            "evidence": "frontend/app.js، commit 70f7647، commit 43737c8",
        },
        {
            "title": "سطح فوریت رسیدگی",
            "what": "تبدیل خروجی مدل به پیام عملیاتی درباره نیاز به بررسی فوری یا ادامه مسیر معمول.",
            "why": "کاربر به تصمیم پشتیبان قابل اقدام نیاز دارد، نه فقط عدد احتمال.",
            "problem": "عدد خام احتمال به تنهایی به action تبدیل نمی‌شود.",
            "how": "براساس threshold safety-first و هشدارها، سطح فوریت نمایش داده می‌شود.",
            "effect": "قابل دفاع‌تر شدن محصول از نگاه مدیریت پروژه و workflow.",
            "status": "آماده.",
            "next": "هماهنگی با اصطلاحات رسمی یک مرکز درمانی در پایلوت.",
            "evidence": "reports/model/metrics_v7.json، frontend/app.js",
        },
        {
            "title": "هشدارهای مهم",
            "what": "نمایش هشدارهای بالینی قابل فهم مثل اکسیژن پایین یا فشار سیستولی بسیار پایین.",
            "why": "کاربر باید بداند چه چیزی باعث نگرانی سیستم شده است.",
            "problem": "واژه «پرچم ایمنی» برای بعضی کاربران نامأنوس بود؛ در نسخه نهایی با «هشدارهای مهم» جایگزین شد.",
            "how": "هشدارها در یک بخش جدا و ساده نمایش داده می‌شوند.",
            "effect": "افزایش explainability و کاهش ابهام.",
            "status": "آماده.",
            "next": "بازبینی متن هشدارها با پرستاران تریاژ.",
            "evidence": "frontend/index.html، frontend/app.js، docs/ux-feedback-synthesis.md",
        },
        {
            "title": "اقدام بعدی",
            "what": "پیشنهادهای عملی مثل اطلاع به پرستار ارشد، تکرار علائم حیاتی یا ادامه مسیر معمول.",
            "why": "خروجی AI باید به workflow نزدیک باشد.",
            "problem": "بدون next action، خروجی فقط یک نمره است.",
            "how": "API و مدل مرورگر فهرست اقدام بعدی را برمی‌گردانند.",
            "effect": "قابل استفاده‌تر شدن محصول در demo و پایلوت.",
            "status": "آماده.",
            "next": "اعتبارسنجی متن اقدام‌ها با پروتکل محلی.",
            "evidence": "backend/main.py، ml/inference.py، frontend/app.js",
        },
        {
            "title": "فیلدهای پیشنهادی باقی‌مانده",
            "what": "نمایش فیلدهایی که بهتر است برای افزایش کیفیت ارزیابی تکمیل شوند.",
            "why": "سیستم باید هم با ورودی ناقص کار کند و هم محدودیت داده را شفاف کند.",
            "problem": "خروجی با داده کم نباید بیش از حد قطعی به نظر برسد.",
            "how": "درصد کامل بودن داده و فهرست فیلدهای پیشنهادی نمایش داده می‌شود.",
            "effect": "شفافیت بیشتر و کاهش ریسک تصمیم‌گیری با اطلاعات ناقص.",
            "status": "آماده.",
            "next": "اولویت‌بندی فیلدهای باقی‌مانده براساس ارزش اطلاعاتی.",
            "evidence": "frontend/app.js، docs/model-card.md",
        },
        {
            "title": "خلاصه کیس",
            "what": "متن قابل کپی و چاپ از نتیجه، علائم، هشدارها و اقدام بعدی.",
            "why": "در ارائه، QA و پایلوت، ثبت خلاصه خروجی مهم است.",
            "problem": "بدون خلاصه، پیگیری بازخورد و مستندسازی دشوار می‌شود.",
            "how": "پس از ارزیابی، بخش خلاصه کیس فعال می‌شود و دکمه کپی/چاپ دارد.",
            "effect": "افزایش traceability و کاربرد برای گزارش پایلوت.",
            "status": "آماده.",
            "next": "افزودن شناسه ناشناس کیس در فاز Laravel.",
            "evidence": "frontend/index.html، frontend/app.js",
        },
        {
            "title": "بازخورد تجربه کاربری",
            "what": "مسیر ثبت بازخورد در backend و برنامه جمع‌آوری بازخورد در مستندات.",
            "why": "TA تأکید کرده پروژه باید از کاربر/ذی‌نفع بازخورد بگیرد.",
            "problem": "بازخورد جعلی یا بدون شاهد قابل دفاع نیست.",
            "how": "endpointهای feedback در backend وجود دارد؛ در نسخه نهایی UI، فرم پایین اپ حذف شد و جمع‌آوری واقعی باید از فرم Notion/Jira/Google Form یا نسخه پایلوت انجام شود.",
            "effect": "حفظ صداقت گزارش و آماده بودن برای پایلوت واقعی.",
            "status": "زیرساخت آماده؛ بازخورد واقعی خارجی نیاز به تکمیل دارد.",
            "next": "گرفتن حداقل ۵ بازخورد واقعی و ثبت با تاریخ و کد ناشناس.",
            "evidence": "backend/main.py، docs/knowledge-base/stakeholder-feedback-log.md",
        },
        {
            "title": "نصب نسخه موبایل / PWA",
            "what": "راهنمای نصب روی موبایل با manifest و service worker.",
            "why": "محصول باید روی گوشی قابل ارسال و استفاده باشد، نه فقط local.",
            "problem": "نسخه local برای استاد، کاربر پایلوت و بازار اندرویدی کافی نیست.",
            "how": "کاربر لینک HTTPS را باز می‌کند و از Add to Home Screen یا Install app استفاده می‌کند.",
            "effect": "قابل استفاده‌تر شدن برای demo عمومی و فاز جذب کاربر.",
            "status": "آماده در GitHub Pages.",
            "next": "ساخت TWA/Capacitor برای انتشار در بازارهای اندرویدی.",
            "evidence": "frontend/manifest.webmanifest، frontend/sw.js، docs/market/twa-build-guide.md",
        },
        {
            "title": "QR Code",
            "what": "QR برای باز کردن لینک عمومی اپ روی موبایل.",
            "why": "در پوستر و ارائه، دسترسی سریع با گوشی مهم است.",
            "problem": "وارد کردن URL طولانی روی موبایل سخت است.",
            "how": "QR در خروجی‌های poster/deliverable قرار می‌گیرد.",
            "effect": "کاهش اصطکاک تست محصول توسط استاد و کاربران.",
            "status": "آماده.",
            "next": "به‌روزرسانی QR اگر دامنه نهایی تغییر کند.",
            "evidence": "docs/artifacts/emdadyar-pwa-qr.png",
        },
        {
            "title": "Disclaimer اخلاقی",
            "what": "هشدار ثابت که سیستم جایگزین متخصص یا پروتکل رسمی نیست.",
            "why": "پروژه سلامت بدون شفافیت اخلاقی قابل دفاع نیست.",
            "problem": "کاربر ممکن است خروجی AI را تشخیص قطعی تلقی کند.",
            "how": "در footer، result panel، privacy و docs تکرار شده است.",
            "effect": "کاهش ریسک سوءبرداشت و تقویت دفاع اخلاقی.",
            "status": "آماده.",
            "next": "افزودن consent کوتاه در فاز پایلوت واقعی.",
            "evidence": "frontend/index.html، frontend/privacy.html، docs/ai-usage-report.md",
        },
    ]

    sections = []
    for index, item in enumerate(features, start=1):
        sections.append(
            f"""
            ## {index}. {item["title"]}

            | پرسش | پاسخ |
            |---|---|
            | این قابلیت چیست؟ | {item["what"]} |
            | چرا اضافه شد؟ | {item["why"]} |
            | چه مشکلی را حل می‌کند؟ | {item["problem"]} |
            | کاربر چگونه از آن استفاده می‌کند؟ | {item["how"]} |
            | اثر روی تصمیم‌گیری یا تجربه کاربر | {item["effect"]} |
            | وضعیت فعلی | {item["status"]} |
            | پیشنهاد بهبود بعدی | {item["next"]} |
            | شاهد فایل/کامیت | {ltr(item["evidence"])} |
            """
        )

    md_file(
        "notion-product-features.md",
        "# قابلیت‌های محصول امداد یار\n\n"
        "این صفحه برای Knowledge Base در Notion است. هر بخش را می‌توان به یک sub-page جداگانه تبدیل کرد.\n\n"
        + "\n".join(dedent(section).strip() for section in sections),
    )


def build_decision_log() -> None:
    rows = [
        {
            "Date": "2026-06-01",
            "Decision": "انتخاب موضوع تریاژ/اورژانس",
            "Context": "نیاز به پروژه‌ای با ارزش انسانی، KPI قابل اندازه‌گیری و قابلیت دفاع در درس مدیریت پروژه فناوری اطلاعات.",
            "Options Considered": "شبکه اجتماعی بازی‌محور؛ داشبورد عمومی؛ سامانه سلامت.",
            "Reason": "موضوع تریاژ ارزش اجتماعی و ضرورت عملیاتی بالاتری دارد و با متریک‌هایی مثل Recall و FPR قابل ارزیابی است.",
            "Impact": "تمرکز پروژه از ایده صرفاً نرم‌افزاری به MVP سلامت‌محور و قابل دفاع تغییر کرد.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "PD-01",
            "Evidence Link": "docs/scope-change-record.md; commit e1962ae",
            "Status": "Done",
        },
        {
            "Date": "2026-06-21",
            "Decision": "انتخاب نام «امداد یار»",
            "Context": "نیاز به نام فارسی، انسانی، قابل فهم و مناسب انتشار عمومی.",
            "Options Considered": "Triage ED؛ تریاژ هوشمند؛ امداد یار.",
            "Reason": "امداد یار برای کاربر فارسی‌زبان ساده‌تر و انسانی‌تر است.",
            "Impact": "هویت محصول در UI و مستندات یکپارچه شد.",
            "Owner": "محدثه حاتمی کیا",
            "Related Jira Issue": "UX-02",
            "Evidence Link": "frontend/index.html; commit 70f7647; commit 43737c8",
            "Status": "Done",
        },
        {
            "Date": "2026-06-01",
            "Decision": "تعریف سیستم به‌عنوان پشتیبان تصمیم نه جایگزین متخصص",
            "Context": "حوزه سلامت و خروجی AI ریسک اخلاقی مستقیم دارد.",
            "Options Considered": "تشخیص قطعی خودکار؛ پیشنهاد مستقل؛ پشتیبان تصمیم.",
            "Reason": "پشتیبان تصمیم با مسئولیت بالینی و استاندارد اخلاقی سازگارتر است.",
            "Impact": "Disclaimer در UI، docs، model card و AI usage report تکرار شد.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "SAFE-01",
            "Evidence Link": "docs/model-card.md; frontend/index.html; docs/ai-usage-report.md",
            "Status": "Done",
        },
        {
            "Date": "2026-06-10",
            "Decision": "انتخاب طراحی فارسی و راست‌به‌چپ",
            "Context": "کاربران هدف فارسی‌زبان هستند و ارائه دانشگاهی نیز فارسی است.",
            "Options Considered": "UI انگلیسی؛ UI دو زبانه؛ UI فارسی RTL.",
            "Reason": "فارسی RTL فهم سریع‌تر و نمایش بهتر برای کاربر نهایی ایجاد می‌کند.",
            "Impact": "HTML با lang=fa و dir=rtl طراحی شد و مستندات با wrapper راست‌چین آماده شدند.",
            "Owner": "محدثه حاتمی کیا",
            "Related Jira Issue": "UX-01",
            "Evidence Link": "frontend/index.html; scripts/normalize_markdown_rtl.py; commit 2cb3d68",
            "Status": "Done",
        },
        {
            "Date": "2026-06-10",
            "Decision": "انتخاب mobile-first / PWA",
            "Context": "کاربر باید بتواند محصول را روی گوشی باز کند و استاد/کاربر پایلوت بدون local server تست کند.",
            "Options Considered": "وب local؛ اپ native؛ PWA؛ TWA.",
            "Reason": "PWA سریع‌ترین مسیر برای دسترسی عمومی، نصب موبایل و demo است.",
            "Impact": "manifest، service worker، QR و بسته market آماده شد.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "FE-04",
            "Evidence Link": "frontend/manifest.webmanifest; frontend/sw.js; docs/artifacts/emdadyar-pwa-qr.png",
            "Status": "Done",
        },
        {
            "Date": "2026-06-15",
            "Decision": "اضافه شدن نمونه‌های آماده تست",
            "Context": "برای demo، QA و تست سریع استاد نیاز به داده نمونه وجود داشت.",
            "Options Considered": "ورودی دستی کامل؛ فایل نمونه؛ دکمه‌های سناریو.",
            "Reason": "دکمه سناریو سریع‌ترین و کم‌خطاترین راه نمایش رفتار محصول است.",
            "Impact": "سناریوهای پرخطر، متوسط، اطلاعات کم و درد قفسه سینه اضافه شدند.",
            "Owner": "محدثه حاتمی کیا",
            "Related Jira Issue": "QA-03",
            "Evidence Link": "frontend/app.js; poster-assets/ui-critical-scenario.png",
            "Status": "Done",
        },
        {
            "Date": "2026-06-15",
            "Decision": "اضافه شدن مسیر بازخورد",
            "Context": "TA تأکید کرد پروژه باید از کاربر/ذی‌نفع بازخورد بگیرد.",
            "Options Considered": "بدون بازخورد؛ فرم درون UI؛ فرم جدا برای پایلوت.",
            "Reason": "برای MVP endpoint بازخورد آماده شد، اما در نسخه محصول نهایی فرم پایین اپ حذف شد تا UI کاربر درمانی شلوغ نشود.",
            "Impact": "backend feedback export باقی ماند و برنامه جمع‌آوری بازخورد در docs ثبت شد.",
            "Owner": "محمدرضا آرمان‌پور",
            "Related Jira Issue": "FB-01",
            "Evidence Link": "backend/main.py; docs/knowledge-base/stakeholder-feedback-log.md; commit 8d17c0d",
            "Status": "Partially Done - real external feedback needs completion",
        },
        {
            "Date": "2026-06-10",
            "Decision": "اضافه شدن هشدارهای ایمنی",
            "Context": "عدد مدل به تنهایی برای کاربر قابل اقدام نیست.",
            "Options Considered": "فقط probability؛ probability + explanation؛ probability + هشدارهای مهم.",
            "Reason": "هشدارهای مهم به کاربر نشان می‌دهد چرا خروجی نگران‌کننده است.",
            "Impact": "Explainability و safety در UI تقویت شد.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "SAFE-02",
            "Evidence Link": "frontend/app.js; ml/inference.py",
            "Status": "Done",
        },
        {
            "Date": "2026-06-10",
            "Decision": "اضافه شدن اقدام بعدی",
            "Context": "کاربر به خروجی قابل عمل نیاز دارد.",
            "Options Considered": "نمایش ESI؛ نمایش ریسک؛ نمایش اقدام بعدی.",
            "Reason": "اقدام بعدی فاصله بین خروجی مدل و workflow عملی را کم می‌کند.",
            "Impact": "خروجی محصول ساده‌تر و کاربردی‌تر شد.",
            "Owner": "محدثه حاتمی کیا",
            "Related Jira Issue": "SAFE-03",
            "Evidence Link": "frontend/index.html; frontend/app.js",
            "Status": "Done",
        },
        {
            "Date": "2026-06-23",
            "Decision": "اضافه شدن QR Code",
            "Context": "در پوستر و ارائه باید دسترسی موبایلی سریع وجود داشته باشد.",
            "Options Considered": "URL متنی؛ QR؛ لینک کوتاه.",
            "Reason": "QR برای تست با گوشی سریع‌تر و حرفه‌ای‌تر است.",
            "Impact": "QR در deliverables و poster assets قرار گرفت.",
            "Owner": "محمدرضا آرمان‌پور",
            "Related Jira Issue": "FD-03",
            "Evidence Link": "docs/artifacts/emdadyar-pwa-qr.png; commit 45990bf",
            "Status": "Done",
        },
        {
            "Date": "2026-06-08",
            "Decision": "تمرکز بر داده‌های زمان تریاژ",
            "Context": "مدل باید فقط داده‌هایی را بخواهد که در لحظه تریاژ قابل دسترس هستند.",
            "Options Considered": "همه داده‌های بیمار؛ داده‌های پس از پذیرش؛ داده‌های triage-time.",
            "Reason": "استفاده از داده‌های آینده باعث data leakage و دفاع‌ناپذیری مدل می‌شود.",
            "Impact": "features به سن، شکایت اصلی، علائم حیاتی و سوابق قابل پرسش محدود شد.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "ML-01",
            "Evidence Link": "docs/model-card.md; reports/model/metrics_v7.json",
            "Status": "Done",
        },
        {
            "Date": "2026-06-08",
            "Decision": "جلوگیری از data leakage",
            "Context": "استاد و TA احتمالاً درباره دفاع علمی مدل سؤال می‌کنند.",
            "Options Considered": "انتخاب threshold روی test؛ استفاده از داده‌های post-triage؛ جداسازی validation/test.",
            "Reason": "انتخاب threshold روی validation و گزارش test برای جلوگیری از leakage ضروری بود.",
            "Impact": "Model Card و metrics قابل دفاع‌تر شدند.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "ML-02",
            "Evidence Link": "ml/train.py; docs/model-card.md; reports/model/metrics_v7.json",
            "Status": "Done",
        },
        {
            "Date": "2026-06-08",
            "Decision": "انتخاب معیارهای AUC, Recall, Precision, FPR",
            "Context": "Accuracy برای مسئله تریاژ کافی و حتی گمراه‌کننده است.",
            "Options Considered": "Accuracy؛ AUC تنها؛ مجموعه متریک‌های عملیاتی.",
            "Reason": "Recall هزینه انسانی FN را نشان می‌دهد و FPR فشار منابع را شفاف می‌کند.",
            "Impact": "KPIها و poster/report با trade-off انسانی قابل دفاع شدند.",
            "Owner": "محمدرضا آرمان‌پور",
            "Related Jira Issue": "PC-01",
            "Evidence Link": "docs/kpi-register.md; reports/model/metrics_v7.json",
            "Status": "Done",
        },
        {
            "Date": "2026-06-06",
            "Decision": "ثبت AI Usage و کنترل انسانی",
            "Context": "استفاده از AI باید شفاف، اخلاقی و تحت کنترل تیم باشد.",
            "Options Considered": "عدم ثبت؛ ثبت کلی؛ گزارش تفصیلی AI usage.",
            "Reason": "شفافیت برای درس مدیریت پروژه و حوزه سلامت ضروری است.",
            "Impact": "گزارش AI Usage و بخش‌های کنترل انسانی آماده شد.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "DOC-04",
            "Evidence Link": "docs/ai-usage-report.md; commit e1962ae",
            "Status": "Done",
        },
    ]
    csv_file(
        "notion-decision-log.csv",
        [
            "Date",
            "Decision",
            "Context",
            "Options Considered",
            "Reason",
            "Impact",
            "Owner",
            "Related Jira Issue",
            "Evidence Link",
            "Status",
        ],
        rows,
    )


def build_change_log() -> None:
    rows = [
        {
            "Date": "2026-06-06",
            "Change": "ساخت MVP اولیه شامل backend، frontend، ML scripts و docs پایه",
            "Before": "پروژه هنوز artifact قابل اجرا در repo نداشت.",
            "After": "ساختار اولیه FastAPI، UI، training script و مستندات پایه اضافه شد.",
            "Reason": "شروع پروژه باید خروجی قابل ردیابی داشته باشد.",
            "Impact": "پایه فنی و مدیریتی پروژه شکل گرفت.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "PD-01",
            "Commit/File Evidence": "commit e1962ae; backend/main.py; frontend/index.html; ml/train.py",
            "Test Result": "نیاز به تست تکمیلی در sprintهای بعدی",
            "Status": "Done",
        },
        {
            "Date": "2026-06-08",
            "Change": "بهبود مدل v6 و اضافه شدن داشبورد Agile و مستندات rubric",
            "Before": "مدل و مستندات برای دفاع سختگیرانه کافی نبودند.",
            "After": "metrics v6، model card، agile dashboard و team matrix اضافه شد.",
            "Reason": "نیاز به اثبات عملکرد مدل و مدیریت پروژه.",
            "Impact": "پروژه از حالت صرفاً فنی به پروژه قابل دفاع مدیریت پروژه نزدیک شد.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "ML-03",
            "Commit/File Evidence": "commit f7ca102; reports/model/metrics_v6.json; docs/agile-dashboard.md",
            "Test Result": "Recall هدف در v6 گزارش شد.",
            "Status": "Done",
        },
        {
            "Date": "2026-06-10",
            "Change": "ساخت deliverableهای Word رسمی",
            "Before": "گزارش نهایی فقط در markdown/docs پراکنده بود.",
            "After": "فایل‌های Word گزارش، راهنمای ارائه و evidence package ساخته شد.",
            "Reason": "برای تحویل دانشگاهی، Word/PDF قابل دفاع‌تر از markdown خام است.",
            "Impact": "تحویل رسمی پروژه ساختارمند شد.",
            "Owner": "محدثه حاتمی کیا",
            "Related Jira Issue": "DOC-01",
            "Commit/File Evidence": "commit fa36dfb; docs/deliverables/",
            "Test Result": "فایل‌ها در repo موجود هستند.",
            "Status": "Done",
        },
        {
            "Date": "2026-06-10",
            "Change": "تبدیل MVP به PWA موبایلی",
            "Before": "UI بیشتر وب‌محور و local بود.",
            "After": "manifest، service worker، app icon و mobile UI اضافه شد.",
            "Reason": "TA و استاد روی محصول عملیاتی و قابل دسترس حساس بودند.",
            "Impact": "امکان نصب و demo روی گوشی فراهم شد.",
            "Owner": "محدثه حاتمی کیا",
            "Related Jira Issue": "FE-04",
            "Commit/File Evidence": "commit 2cb3d68; frontend/manifest.webmanifest; frontend/sw.js",
            "Test Result": "PWA assets موجود است؛ نصب واقعی باید روی گوشی تست شود.",
            "Status": "Done",
        },
        {
            "Date": "2026-06-13",
            "Change": "اضافه شدن Agile evidence و Knowledge Base",
            "Before": "پروژه از نگاه TA بیش از حد فنی دیده می‌شد.",
            "After": "Sprint notes، meeting notes، technical decisions، stakeholder feedback log و team playbook اضافه شد.",
            "Reason": "نیاز به نمایش کار تیمی، backlog و مدیریت دانش.",
            "Impact": "پاسخ مستقیم به نقد TA آماده شد.",
            "Owner": "محمدرضا آرمان‌پور",
            "Related Jira Issue": "PM-01",
            "Commit/File Evidence": "commit 80e5f60; docs/knowledge-base/",
            "Test Result": "اسناد در repo قابل مشاهده‌اند.",
            "Status": "Done",
        },
        {
            "Date": "2026-06-15",
            "Change": "اضافه شدن feedback export و time tracking",
            "Before": "مسیر ثبت feedback و time tracking شفاف نبود.",
            "After": "endpointهای feedback، time-tracking-log و work-management-board اضافه شد.",
            "Reason": "پروژه باید نشان دهد کار تیمی، زمان و بازخورد را مدیریت می‌کند.",
            "Impact": "شواهد PM قابل import/نمایش شد.",
            "Owner": "محمدرضا آرمان‌پور",
            "Related Jira Issue": "FB-01",
            "Commit/File Evidence": "commit 8d17c0d; backend/main.py; docs/artifacts/time-tracking-log.csv",
            "Test Result": "backend endpoint تعریف شده؛ feedback خارجی واقعی هنوز نیاز به جمع‌آوری دارد.",
            "Status": "Done / Needs real feedback",
        },
        {
            "Date": "2026-06-15",
            "Change": "تولید assets پوستر و اسکرین‌شات‌های محصول",
            "Before": "پوستر و evidence تصویری کافی نبود.",
            "After": "ROC، PR، confusion matrix، UI screenshots، burndown و user acquisition assets اضافه شد.",
            "Reason": "پوستر A0 و دفاع نهایی نیاز به تصویر و نمودار دارد.",
            "Impact": "بخش بصری پروژه قوی‌تر شد.",
            "Owner": "محدثه حاتمی کیا",
            "Related Jira Issue": "FD-02",
            "Commit/File Evidence": "commit c03ea13; poster-assets/",
            "Test Result": "PNG assets موجود است.",
            "Status": "Done",
        },
        {
            "Date": "2026-06-20",
            "Change": "آماده‌سازی مدل v7 و deploy",
            "Before": "مدل v6 آماده بود ولی نیاز به بهبود و deploy عمومی داشت.",
            "After": "مدل v7، reports v7، Dockerfile، Procfile، render.yaml و evidence portal اضافه شد.",
            "Reason": "هدف افزایش کیفیت مدل و آماده‌سازی برای deploy واقعی بود.",
            "Impact": "AUC به 0.9041 و Recall به 0.9246 رسید.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "ML-05",
            "Commit/File Evidence": "commit 5584b16; reports/model/metrics_v7.json; models/triage_model_v7.pkl",
            "Test Result": "metrics v7 ثبت شد.",
            "Status": "Done",
        },
        {
            "Date": "2026-06-20",
            "Change": "اضافه شدن public GitHub Pages PWA",
            "Before": "کاربر برای اجرا به backend/local server نیاز داشت.",
            "After": "مدل به JSON مرورگر export شد و نسخه public/static آماده شد.",
            "Reason": "کاربر و استاد باید بدون local server اپ را باز کنند.",
            "Impact": "لینک عمومی محصول قابل ارسال شد.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "DEP-01",
            "Commit/File Evidence": "commit a1ec91f; frontend/model-v7.json; .github/workflows/deploy-pages.yml",
            "Test Result": "GitHub Pages در بررسی قبلی با status 200 کار کرد.",
            "Status": "Done",
        },
        {
            "Date": "2026-06-21",
            "Change": "پولیش تجربه کاربری PWA",
            "Before": "متن‌ها و نصب موبایل نیاز به اصلاح داشتند.",
            "After": "نام امداد یار، متن‌های ساده‌تر، config public API و UX نصب بهبود یافت.",
            "Reason": "کاربر نباید با اصطلاحات فنی یا متن‌های گزارش‌گونه روبه‌رو شود.",
            "Impact": "محصول کاربرپسندتر و آماده ارسال شد.",
            "Owner": "محدثه حاتمی کیا",
            "Related Jira Issue": "UX-04",
            "Commit/File Evidence": "commit 70f7647; frontend/index.html; frontend/app.js",
            "Test Result": "script check_public_pwa_cdp.js اضافه شد.",
            "Status": "Done",
        },
        {
            "Date": "2026-06-23",
            "Change": "ساخت QR، Jira import CSV و GitHub knowledge CSV",
            "Before": "انتقال به ابزارهای مدیریت پروژه و دانش دستی و پراکنده بود.",
            "After": "CSVهای import، QR و راهنمای mobile handoff اضافه شد.",
            "Reason": "استاد روی ابزارهای مدیریت پروژه مثل Jira و مدیریت دانش حساس است.",
            "Impact": "پروژه برای انتقال به Jira/Project/Notion آماده‌تر شد.",
            "Owner": "محمدرضا آرمان‌پور",
            "Related Jira Issue": "PM-04",
            "Commit/File Evidence": "commit 45990bf; docs/artifacts/jira-import-issues.csv; docs/artifacts/github-project-knowledge-items.csv",
            "Test Result": "CSVها موجود هستند؛ board واقعی باید ساخته شود.",
            "Status": "Done / Needs import",
        },
        {
            "Date": "2026-06-27",
            "Change": "نهایی‌سازی UX امداد یار و بسته release",
            "Before": "فرم feedback داخل محصول و برخی متن‌ها برای کاربر نهایی شلوغ بود.",
            "After": "UI نهایی‌تر شد، feedback synthetic برچسب‌گذاری شد و بسته بازار ساخته شد.",
            "Reason": "محصول باید برای کاربر عادی تمیز باشد و feedback جعلی به عنوان واقعی گزارش نشود.",
            "Impact": "نسخه نهایی user-facing آماده‌تر شد.",
            "Owner": "محدثه حاتمی کیا",
            "Related Jira Issue": "FD-04",
            "Commit/File Evidence": "commit 43737c8; docs/deliverables/Emdadyar_Market_Release_Package.zip",
            "Test Result": "screenshots بازار موجود است.",
            "Status": "Done",
        },
        {
            "Date": "2026-06-28",
            "Change": "روتوش نهایی docs و evidence feedback",
            "Before": "اسناد قدیمی/تکراری و وضعیت بازخورد پرستاران نیاز به شفافیت داشت.",
            "After": "docs قدیمی حذف شد، final index ساخته شد، ۹ بازخورد پرستار تریاژ در وضعیت pending confirmation ثبت شد.",
            "Reason": "نسخه نهایی نباید ادعای بازخورد واقعی بدون تأیید داشته باشد.",
            "Impact": "صداقت evidence و نظم تحویل بهتر شد.",
            "Owner": "محمدامین پورمند",
            "Related Jira Issue": "DOC-08",
            "Commit/File Evidence": "commit cf9248e; docs/final-submission-index.md; docs/triage-nurse-feedback-confirmation.md",
            "Test Result": "public PWA و assets اصلی در بررسی قبلی OK بودند.",
            "Status": "Done",
        },
    ]
    csv_file(
        "notion-change-log.csv",
        [
            "Date",
            "Change",
            "Before",
            "After",
            "Reason",
            "Impact",
            "Owner",
            "Related Jira Issue",
            "Commit/File Evidence",
            "Test Result",
            "Status",
        ],
        rows,
    )


def build_sprint_notes() -> None:
    md_file(
        "notion-sprint-notes.md",
        f"""
        # Sprint Notes | امداد یار

        ## Sprint 0: تعریف مسئله و محدوده

        | بخش | توضیح |
        |---|---|
        | Goal | انتخاب مسئله سلامت‌محور، تعریف ارزش انسانی و محدوده MVP |
        | Tasks | تعریف مسئله، ذی‌نفعان، ارزش اجتماعی/ملی، نقش decision-support، محدودیت اخلاقی |
        | Deliverables | {ltr("docs/project-management-plan.md")}، {ltr("docs/stakeholder-register.md")}، {ltr("docs/scope-change-record.md")} |
        | Risks | ادعای بیش از حد پزشکی؛ دامنه مبهم؛ نبود ارزش قابل اندازه‌گیری |
        | Decisions | تمرکز بر تریاژ اورژانس و تعریف سامانه به عنوان پشتیبان تصمیم |
        | What changed? | پروژه از ایده خام به محصول سلامت‌محور با KPI مشخص تبدیل شد. |
        | What remained? | تاریخ دقیق جلسه و لینک واقعی Jira هنوز باید تکمیل شود. |
        | Link to Jira issues | PD-01, PD-02, SAFE-01 |

        ## Sprint 1: مدل/منطق ارزیابی

        | بخش | توضیح |
        |---|---|
        | Goal | ساخت baseline مدل و کنترل data leakage |
        | Tasks | انتخاب features triage-time، حذف داده‌های آینده، آموزش مدل‌های اولیه، تعریف threshold و متریک‌ها |
        | Deliverables | {ltr("ml/train.py")}، {ltr("docs/model-card.md")}، {ltr("reports/model/metrics_v5.json")} و سپس v6/v7 |
        | Risks | leakage، FPR بالا، وابستگی بیش از حد به age/gender، ناتوانی با داده ناقص |
        | Decisions | استفاده از AUC/Recall/Precision/FPR؛ انتخاب safety-first threshold |
        | What changed? | مدل از آزمایش اولیه به نسخه قابل دفاع‌تر با داده زمان تریاژ رسید. |
        | What remained? | اعتبارسنجی بالینی و تحلیل fairness در فاز بعدی. |
        | Link to Jira issues | ML-01, ML-02, ML-03, ML-04, ML-05 |

        ## Sprint 2: UI و تجربه کاربر

        | بخش | توضیح |
        |---|---|
        | Goal | تبدیل مدل به تجربه قابل استفاده برای کاربر فارسی‌زبان |
        | Tasks | طراحی فرم، خروجی قابل فهم، نمونه‌های تست، هشدارهای مهم، اقدام بعدی، خلاصه کیس |
        | Deliverables | {ltr("frontend/index.html")}، {ltr("frontend/app.js")}، {ltr("frontend/styles.css")} |
        | Risks | شلوغی UI، سوءبرداشت از خروجی، سختی استفاده روی موبایل |
        | Decisions | فارسی و راست‌به‌چپ؛ متن ساده؛ قرار گرفتن نمونه‌های تست پایین فرم |
        | What changed? | خروجی از ESI/عدد خام به پیام قابل عمل تبدیل شد. |
        | What remained? | تست خوانایی با کاربر واقعی. |
        | Link to Jira issues | UX-01, UX-02, UX-03, SAFE-02, SAFE-03 |

        ## Sprint 3: مستندسازی، بازخورد و آماده‌سازی دفاع

        | بخش | توضیح |
        |---|---|
        | Goal | پاسخ به نقد TA درباره غیرمدیریت‌پروژه‌ای بودن کار |
        | Tasks | ساخت Knowledge Base، Sprint Notes، Meeting Notes، Risk Register، KPI، Burndown، AI Usage Report |
        | Deliverables | {ltr("docs/knowledge-base/")}، {ltr("docs/agile-delivery-evidence.md")}، {ltr("docs/kpi-register.md")}، {ltr("docs/risk-register.md")} |
        | Risks | کم‌رنگ دیده شدن نقش اعضا؛ نبود evidence واقعی ابزار مدیریت پروژه؛ نبود feedback خارجی |
        | Decisions | تعریف نقش‌های قابل ارائه برای هر عضو؛ آماده‌سازی CSV import برای Jira و knowledge project |
        | What changed? | پروژه از demo فنی به بسته مدیریت پروژه با artifactهای قابل دفاع تبدیل شد. |
        | What remained? | ساخت واقعی Jira/Notion و گرفتن screenshot واقعی. |
        | Link to Jira issues | PM-01, PM-02, PM-03, DOC-01, DOC-04 |

        ## Final Sprint: deploy، QR، پوستر و تحویل نهایی

        | بخش | توضیح |
        |---|---|
        | Goal | آماده‌سازی نسخه عمومی و بسته تحویل نهایی |
        | Tasks | GitHub Pages، PWA، QR، package بازار، poster assets، cleanup docs، final index |
        | Deliverables | {ltr(APP_URL)}، {ltr("docs/artifacts/emdadyar-pwa-qr.png")}، {ltr("poster-final-assets-fa.md")}، {ltr("docs/final-submission-index.md")} |
        | Risks | خراب شدن لینک عمومی، ادعای بازخورد بدون تأیید، فایل‌های قدیمی و گیج‌کننده |
        | Decisions | حذف docs قدیمی، برچسب‌گذاری feedbackهای synthetic، ثبت بازخوردهای پرستار به صورت pending confirmation |
        | What changed? | نسخه نهایی تمیزتر و قابل ارسال‌تر شد. |
        | What remained? | وارد کردن CSVها در Jira/Notion، گرفتن screenshot واقعی و تأیید بازخوردهای خارجی. |
        | Link to Jira issues | DEP-01, FD-01, FD-02, FD-03, FB-02 |
        """,
    )


def build_meeting_notes() -> None:
    md_file(
        "notion-meeting-notes.md",
        """
        # Meeting Notes | امداد یار

        نکته صداقت: بعضی تاریخ‌ها از فایل‌های موجود و commit history قابل برداشت هستند؛ اگر جلسه واقعی تیمی با همان تاریخ برگزار نشده، در Notion تاریخ واقعی را جایگزین کنید. هیچ screenshot یا حضور واقعی بدون تأیید تیم نباید ادعا شود.

        ## جلسه انتخاب مسئله

        | فیلد | مقدار |
        |---|---|
        | تاریخ | 2026-06-01 بر اساس docs/knowledge-base/meeting-notes.md؛ در صورت تفاوت، تاریخ واقعی را وارد کنید |
        | افراد حاضر | محمدامین پورمند، محدثه حاتمی کیا، محمدرضا آرمان‌پور |
        | دستور جلسه | انتخاب موضوع، بررسی ارزش انسانی، امکان مدل‌سازی، تناسب با درس مدیریت پروژه |
        | تصمیم‌ها | موضوع تریاژ هوشمند انتخاب شد؛ تمرکز روی decision-support قرار گرفت. |
        | کارهای تعریف‌شده | محمدامین: بررسی داده و مدل؛ محمدرضا: ارزش اجتماعی و ذی‌نفعان؛ محدثه: خوانایی ایده برای ارائه |
        | وضعیت پیگیری | انجام‌شده در مستندات project-management-plan و stakeholder-register |
        | لینک Jira | PD-01, PD-02 |

        ## جلسه تعیین محدوده و اخلاق پروژه

        | فیلد | مقدار |
        |---|---|
        | تاریخ | 2026-06-01 یا [تاریخ واقعی را وارد کنید] |
        | افراد حاضر | محمدامین پورمند، محدثه حاتمی کیا، محمدرضا آرمان‌پور |
        | دستور جلسه | تعیین مرز MVP، عدم جایگزینی متخصص، جلوگیری از ادعای تشخیص |
        | تصمیم‌ها | disclaimer اخلاقی در UI و docs الزامی شد؛ داده‌های پس از تریاژ از مدل حذف شوند. |
        | کارهای تعریف‌شده | محمدامین: کنترل leakage؛ محدثه: متن disclaimer؛ محمدرضا: ثبت ریسک اخلاقی |
        | وضعیت پیگیری | انجام‌شده؛ evidence در model-card، risk-register و frontend موجود است. |
        | لینک Jira | SAFE-01, ML-02, PC-03 |

        ## جلسه بررسی داده و مدل

        | فیلد | مقدار |
        |---|---|
        | تاریخ | 2026-06-08 بر اساس commit f7ca102 و decision-log؛ در صورت تفاوت، تاریخ واقعی را وارد کنید |
        | افراد حاضر | محمدامین پورمند، محمدرضا آرمان‌پور |
        | دستور جلسه | بررسی نسخه‌های مدل، متریک‌ها، threshold و trade-off Recall/FPR |
        | تصمیم‌ها | Recall به عنوان KPI انسانی اصلی انتخاب شد؛ FPR به عنوان هزینه عملیاتی گزارش شود. |
        | کارهای تعریف‌شده | محمدامین: آموزش/ارزیابی v6/v7؛ محمدرضا: KPI و risk register |
        | وضعیت پیگیری | انجام‌شده؛ evidence در metrics_v7 و kpi-register موجود است. |
        | لینک Jira | ML-03, ML-05, PC-01 |

        ## جلسه طراحی UI و خروجی قابل فهم

        | فیلد | مقدار |
        |---|---|
        | تاریخ | 2026-06-04 در meeting-notes و 2026-06-21 در polish UI؛ تاریخ واقعی را در Notion نهایی کنید |
        | افراد حاضر | محمدامین پورمند، محدثه حاتمی کیا |
        | دستور جلسه | ساده‌سازی فرم، خروجی قابل فهم، موبایل، سناریوهای آماده |
        | تصمیم‌ها | UI فارسی RTL، متن ساده، نمونه‌های تست پایین فرم و توضیح «پشتیبان تصمیم» حفظ شود. |
        | کارهای تعریف‌شده | محدثه: بازبینی UX و سناریوها؛ محمدامین: اتصال به API/مدل مرورگر |
        | وضعیت پیگیری | انجام‌شده؛ evidence در frontend/index.html و frontend/app.js |
        | لینک Jira | UX-01, UX-02, UX-03, FE-04 |

        ## جلسه تقسیم نقش اعضا

        | فیلد | مقدار |
        |---|---|
        | تاریخ | [تاریخ واقعی را وارد کنید]؛ نقش‌ها در docs/team-collaboration-matrix.md و CSVهای جدید ثبت شده‌اند |
        | افراد حاضر | محمدامین پورمند، محدثه حاتمی کیا، محمدرضا آرمان‌پور |
        | دستور جلسه | مشخص کردن نقش واقعی و قابل توضیح هر عضو برای ارائه |
        | تصمیم‌ها | محمدامین: مدل/API/معماری؛ محدثه: UI/Docs/QA؛ محمدرضا: KPI/Risk/Burndown/Feedback |
        | کارهای تعریف‌شده | هر عضو حداقل یک بخش ساده و قابل دفاع در ارائه داشته باشد. |
        | وضعیت پیگیری | نیاز به تأیید شفاهی تیم و درج در Jira با assignee واقعی |
        | لینک Jira | PM-02, PM-03 |

        ## جلسه بازخورد TA و تغییر مسیر مستندسازی

        | فیلد | مقدار |
        |---|---|
        | تاریخ | 2026-06-13 بر اساس docs/agile-delivery-evidence.md؛ در صورت تفاوت، تاریخ واقعی را وارد کنید |
        | افراد حاضر | محمدامین پورمند، محدثه حاتمی کیا، محمدرضا آرمان‌پور |
        | دستور جلسه | پاسخ به نقد TA درباره ابزار مدیریت پروژه، feedback و Agile |
        | تصمیم‌ها | ساخت بسته Agile Evidence، Knowledge Base، Jira/GitHub CSV، برنامه feedback و time tracking |
        | کارهای تعریف‌شده | محمدرضا: backlog/KPI/risk؛ محدثه: docs/QA/screenshots؛ محمدامین: هماهنگی فنی و deploy |
        | وضعیت پیگیری | بخش عمده انجام‌شده؛ وارد کردن واقعی در Jira/Notion و screenshot هنوز نیاز به تکمیل دارد |
        | لینک Jira | PM-01, PM-04, DOC-04, FB-01 |

        ## جلسه آماده‌سازی پوستر

        | فیلد | مقدار |
        |---|---|
        | تاریخ | 2026-06-15 بر اساس poster-assets؛ در صورت تفاوت، تاریخ واقعی را وارد کنید |
        | افراد حاضر | محمدامین پورمند، محدثه حاتمی کیا، محمدرضا آرمان‌پور |
        | دستور جلسه | آماده‌سازی متن‌ها و نمودارهای پوستر A0 |
        | تصمیم‌ها | استفاده از metrics v7، UI screenshots، burndown، KPI و تأکید بر ارزش انسانی/اخلاقی |
        | کارهای تعریف‌شده | محمدامین: نمودار مدل؛ محدثه: تصویر UI؛ محمدرضا: KPI/Burndown/Risk |
        | وضعیت پیگیری | assets موجود است؛ پوستر نهایی با ابزار تصویر جداگانه ساخته می‌شود |
        | لینک Jira | FD-01, FD-02 |

        ## جلسه نهایی‌سازی تحویل‌ها

        | فیلد | مقدار |
        |---|---|
        | تاریخ | 2026-06-28 بر اساس commit cf9248e؛ تاریخ جلسه واقعی را در صورت تفاوت جایگزین کنید |
        | افراد حاضر | محمدامین پورمند، محدثه حاتمی کیا، محمدرضا آرمان‌پور |
        | دستور جلسه | پاکسازی docs، شفاف‌سازی feedback، آماده‌سازی deliverables و بسته Notion/Jira |
        | تصمیم‌ها | ادعای feedback واقعی بدون تأیید ممنوع؛ docs قدیمی حذف/جدا شوند؛ Jira/Notion با evidence link تکمیل شود. |
        | کارهای تعریف‌شده | محمدامین: final package؛ محدثه: QA و screenshot؛ محمدرضا: import و تکمیل time tracking |
        | وضعیت پیگیری | بسته نهایی ساخته شد؛ import در ابزار واقعی هنوز نیاز به انجام دارد |
        | لینک Jira | DOC-08, PM-05, FB-02 |
        """,
    )


def build_risk_register() -> None:
    rows = [
        ("R-01", "برداشت اشتباه از سیستم به‌عنوان تشخیص پزشکی", "اعتماد بیش از حد به AI یا متن خروجی نامناسب", "ریسک اخلاقی و تصمیم درمانی اشتباه", 3, 5, "تکرار disclaimer، متن decision-support، آموزش کاربر و تأیید متخصص در فاز بعد", "محمدامین پورمند", "Open", "SAFE-01"),
        ("R-02", "داده ناقص", "در تریاژ ممکن است همه علائم حیاتی در دسترس نباشند", "کاهش اطمینان خروجی", 4, 4, "پشتیبانی از missingness، نمایش data completeness و فیلدهای پیشنهادی باقی‌مانده", "محدثه حاتمی کیا", "Mitigated", "UX-05"),
        ("R-03", "خطای مثبت کاذب زیاد", "threshold safety-first باعث حساسیت بالاتر می‌شود", "افزایش فشار منابع اورژانس", 4, 4, "گزارش FPR، operating point جایگزین و تنظیم threshold برای محیط واقعی", "محمدرضا آرمان‌پور", "Open", "PC-01"),
        ("R-04", "خطای منفی کاذب برای بیمار پرخطر", "مدل ممکن است بیمار بحرانی را کم‌ریسک تشخیص دهد", "خطر انسانی جدی", 3, 5, "اولویت دادن به Recall، safety flags و هشدار استفاده انسانی", "محمدامین پورمند", "Open", "ML-04"),
        ("R-05", "نبود اعتبارسنجی بالینی", "عدم دسترسی به بیمارستان/پرستار تأییدکننده در زمان محدود", "کاهش قابلیت استفاده واقعی", 4, 5, "ثبت محدودیت، جمع‌آوری feedback از پرستار/دانشجوی پزشکی، پایلوت کوچک", "محمدرضا آرمان‌پور", "Needs Completion", "FB-02"),
        ("R-06", "محدودیت داده آموزشی", "داده ثانویه و غیر بومی", "احتمال تفاوت عملکرد در محیط واقعی ایران", 4, 4, "شفاف‌سازی در model card و برنامه جذب داده/feedback بومی", "محمدامین پورمند", "Open", "ML-06"),
        ("R-07", "ناقص بودن مستندات", "تمرکز زیاد روی کدنویسی و کمبود artifact مدیریتی", "کاهش نمره درس مدیریت پروژه", 2, 5, "ساخت Knowledge Base، final index، Word deliverables و بسته Notion/Jira", "محدثه حاتمی کیا", "Mitigated", "DOC-01"),
        ("R-08", "مشخص نبودن نقش اعضای تیم", "تمرکز زیاد کار فنی روی یک نفر", "ایراد در ارزیابی تیمی", 3, 4, "تعریف نقش‌های ساده، time tracking و assignee در Jira", "محمدرضا آرمان‌پور", "Needs Completion", "PM-02"),
        ("R-09", "وابستگی بیش از حد به AI", "استفاده از Codex/ChatGPT برای کد و مستندات", "کاهش اعتبار علمی و اخلاقی", 3, 4, "AI usage report، کنترل انسانی، تست و عدم پذیرش خروجی بدون بررسی", "محمدامین پورمند", "Mitigated", "DOC-04"),
        ("R-10", "آماده نبودن deploy", "نیاز به اجرای غیرلوکال روی موبایل", "عدم امکان تست عمومی", 2, 5, "GitHub Pages PWA، config API و راهنمای deploy", "محمدامین پورمند", "Mitigated", "DEP-01"),
        ("R-11", "نقص در تجربه کاربری موبایل", "کوچک بودن صفحه، متن‌های زیاد یا ابهام در نصب", "کاهش پذیرش کاربر", 3, 4, "mobile-first design، tabs، install help و screenshots", "محدثه حاتمی کیا", "Mitigated", "UX-04"),
        ("R-12", "عدم دریافت بازخورد ذی‌نفعان", "زمان کم و دشواری دسترسی به افراد درمانی", "پروژه فقط فنی دیده می‌شود", 4, 5, "فرم ۵ سؤالی، برنامه ۵ تا ۱۰ بازخورد، pending confirmation برای ۹ پرستار فقط پس از تأیید", "محمدرضا آرمان‌پور", "Needs Completion", "FB-02"),
    ]
    csv_file(
        "notion-risk-register.csv",
        [
            "Risk ID",
            "Risk Description",
            "Cause",
            "Impact",
            "Probability",
            "Severity",
            "Mitigation Plan",
            "Owner",
            "Status",
            "Related Jira Issue",
        ],
        [
            {
                "Risk ID": r[0],
                "Risk Description": r[1],
                "Cause": r[2],
                "Impact": r[3],
                "Probability": r[4],
                "Severity": r[5],
                "Mitigation Plan": r[6],
                "Owner": r[7],
                "Status": r[8],
                "Related Jira Issue": r[9],
            }
            for r in rows
        ],
    )


def build_ai_usage_report() -> None:
    md_file(
        "notion-ai-usage-report.md",
        """
        # گزارش استفاده از AI

        ## اصل شفافیت

        در پروژه امداد یار از ابزارهای AI به عنوان کمک‌یار توسعه، مستندسازی و تحلیل استفاده شد؛ اما تصمیم نهایی، کنترل کیفیت، پذیرش خروجی، انتخاب دامنه محصول و مسئولیت اخلاقی بر عهده تیم پروژه است. این بخش نباید طوری ارائه شود که انگار AI مالک پروژه بوده است.

        ## Codex برای چه کارهایی استفاده شد؟

        | حوزه | نوع استفاده | کنترل انسانی |
        |---|---|---|
        | کدنویسی | اصلاح frontend، backend، اسکریپت‌های build و package | اجرای تست، بررسی git diff و حذف ادعاهای غیرواقعی |
        | مستندسازی | ساخت گزارش‌ها، بسته‌های Word، index و package مدیریت پروژه | بازبینی متن، تطبیق با rubric و اصلاح لحن فارسی |
        | تحلیل repo | استخراج evidence از commitها و فایل‌ها | استفاده از git history واقعی و عدم جعل screenshot |
        | QA | پیشنهاد سناریوهای تست و فایل‌های CSV | ثبت وضعیت «نیاز به تکمیل» برای تست‌های انسانی انجام‌نشده |

        ## ChatGPT برای چه کارهایی استفاده شد؟

        | حوزه | نوع استفاده | کنترل انسانی |
        |---|---|---|
        | ایده‌پردازی | ساختار گزارش، متن پوستر و تحلیل نقد TA | انتخاب نهایی توسط تیم و حذف بخش‌های غیرقابل دفاع |
        | طراحی محتوا | متن فارسی رسمی و کوتاه برای پوستر/ارائه | اصلاح بر اساس پروژه واقعی و فایل‌های موجود |
        | تحلیل UX | پیشنهاد ایرادهای احتمالی کاربر | برچسب‌گذاری به عنوان synthetic/pre-pilot، نه feedback واقعی |

        ## چه چیزهایی توسط انسان بررسی و اصلاح شد؟

        - انتخاب موضوع امداد یار و مرز اخلاقی decision-support.
        - تصمیم به تمرکز روی داده‌های زمان تریاژ و حذف داده‌های post-triage.
        - تأیید اینکه feedbackهای synthetic نباید به عنوان بازخورد واقعی گزارش شوند.
        - انتخاب نقش‌های قابل ارائه برای اعضای تیم.
        - بررسی خروجی UI روی موبایل/دسکتاپ و اصلاح زبان محصول.
        - تصمیم به ساخت Notion/Jira واقعی به جای ادعای استفاده از ابزار بدون evidence.

        ## چه تصمیم‌هایی انسانی بوده‌اند؟

        | تصمیم | دلیل انسانی بودن |
        |---|---|
        | انتخاب دامنه سلامت و ارزش انسانی پروژه | به ارزش اجتماعی، دفاع دانشگاهی و اولویت تیم مربوط است |
        | تعیین محصول به عنوان پشتیبان تصمیم | تصمیم اخلاقی و دامنه مسئولیت است |
        | اولویت دادن به Recall | trade-off انسانی میان خطر از دست دادن بیمار بحرانی و افزایش بررسی اضافه است |
        | عدم جعل feedback واقعی | تصمیم صداقت پروژه و اعتبار دفاع است |
        | حذف فرم feedback از UI نهایی | تصمیم تجربه کاربر و تمرکز محصول |

        ## کجا خروجی AI رد یا اصلاح شد؟

        - poster قبلی که کیفیت بصری مطلوب نداشت کنار گذاشته شد و قرار شد با ابزار تصویر جداگانه ساخته شود.
        - feedbackهای تولیدشده به عنوان real ثبت نشدند و با برچسب synthetic یا pending confirmation جدا شدند.
        - متن‌های گزارش‌گونه از UI محصول حذف شد تا فقط محتوای مورد نیاز کاربر باقی بماند.
        - ادعای استفاده واقعی از Jira/Notion بدون screenshot حذف و به «نیاز به تکمیل» تبدیل شد.
        - اصطلاحات مبهم مثل «پرچم‌های ایمنی» به «هشدارهای مهم» نزدیک شد.

        ## چگونه از وابستگی کامل به AI جلوگیری شد؟

        - هر ادعا باید evidence link به فایل، commit یا artifact داشته باشد.
        - متریک‌های مدل از reports واقعی خوانده می‌شوند، نه متن تبلیغاتی.
        - بازخورد واقعی تا زمان تأیید با تاریخ و کد ناشناس، واقعی نامیده نمی‌شود.
        - تصمیم‌های حساس در decision log با owner انسانی ثبت می‌شوند.
        - Jira/Notion باید توسط اعضای تیم import و screenshot واقعی شوند.

        ## چرا در پروژه سلامت شفافیت اخلاقی ضروری است؟

        در سلامت، خروجی AI می‌تواند روی برداشت انسان از فوریت وضعیت اثر بگذارد. بنابراین شفافیت درباره محدودیت‌ها، داده آموزشی، نبود اعتبارسنجی بالینی، احتمال خطا و نقش پشتیبان تصمیم بخشی از کیفیت فنی پروژه است؛ نه یک پیوست تزئینی.
        """,
    )


def build_stakeholder_feedback() -> None:
    rows = [
        {
            "Date": "نیاز به جمع‌آوری بازخورد واقعی دارد",
            "Stakeholder Type": "وضعیت فعلی",
            "UI Clarity Score": "",
            "Output Clarity Score": "",
            "Disclaimer Clarity Score": "",
            "Main Feedback": "در repo بازخورد خارجی تأییدشده با تاریخ/هویت ناشناس پیدا نشد. فقط یک نمونه داخلی، ۷۸ feedback synthetic/pre-pilot و ۹ بازخورد پرستار در وضعیت pending confirmation وجود دارد.",
            "Action Taken": "تا زمان تأیید واقعی، این موارد به عنوان بازخورد واقعی گزارش نشوند. حداقل ۵ بازخورد واقعی با فرم زیر جمع‌آوری شود.",
            "Owner": "محمدرضا آرمان‌پور",
            "Status": "Needs real collection",
        },
        {
            "Date": "[تاریخ واقعی را وارد کنید]",
            "Stakeholder Type": "پرستار تریاژ / دانشجوی پزشکی / دانشجوی پرستاری / کاربر عمومی",
            "UI Clarity Score": "[۱ تا ۵]",
            "Output Clarity Score": "[۱ تا ۵]",
            "Disclaimer Clarity Score": "[۱ تا ۵]",
            "Main Feedback": "فرم پیشنهادی: ۱) خروجی قابل فهم بود؟ ۲) UI سریع و واضح بود؟ ۳) مشخص بود سیستم جایگزین پزشک نیست؟ ۴) با ورودی ناقص هم خروجی قابل قبول بود؟ ۵) مهم‌ترین پیشنهاد بهبود چیست؟",
            "Action Taken": "[اقدام انجام‌شده بعد از بازخورد را وارد کنید]",
            "Owner": "[مسئول پیگیری]",
            "Status": "Template - complete after real interview",
        },
    ]
    csv_file(
        "notion-stakeholder-feedback.csv",
        [
            "Date",
            "Stakeholder Type",
            "UI Clarity Score",
            "Output Clarity Score",
            "Disclaimer Clarity Score",
            "Main Feedback",
            "Action Taken",
            "Owner",
            "Status",
        ],
        rows,
    )
    md_file(
        "stakeholder-feedback-form.md",
        """
        # فرم پیشنهادی جمع‌آوری بازخورد واقعی

        این فرم را برای حداقل ۵ نفر ارسال کنید. اگر ۹ پرستار تریاژ واقعاً نظرها را تأیید کردند، برای هر نفر یک کد ناشناس مثل NURSE-01 ثبت کنید و تاریخ واقعی را بنویسید.

        ## اطلاعات ثبت

        - کد ناشناس پاسخ‌دهنده:
        - نوع ذی‌نفع: پرستار تریاژ / دانشجوی پزشکی / دانشجوی پرستاری / کاربر عمومی / آشنا با اورژانس
        - تاریخ:
        - لینک نسخه تست‌شده:

        ## پرسش‌ها

        1. وضوح رابط کاربری را از ۱ تا ۵ چند می‌دهید؟
        2. وضوح خروجی و اقدام بعدی را از ۱ تا ۵ چند می‌دهید؟
        3. آیا مشخص بود سامانه جایگزین پزشک یا پرستار نیست؟ از ۱ تا ۵ نمره دهید.
        4. آیا با ورودی ناقص هم خروجی برای ارزیابی اولیه قابل فهم بود؟
        5. مهم‌ترین ایراد یا پیشنهاد بهبود شما چیست؟
        6. آیا اجازه می‌دهید نظر شما به شکل ناشناس در گزارش درس ثبت شود؟

        ## قانون ثبت

        بدون پاسخ واقعی، هیچ ردیفی را با status «Confirmed» وارد نکنید. وضعیت‌های مجاز: Pending, Confirmed, Rejected, Needs Follow-up.
        """,
    )


def build_qa_test_log() -> None:
    rows = [
        ("QA-01", "فرم خالی", "هیچ فیلدی پر نشود و ارزیابی اجرا شود", "عدم crash؛ نمایش داده محدود و فیلدهای پیشنهادی", "نیاز به اجرای نهایی در browser و ثبت screenshot", "Needs Run", "محدثه حاتمی کیا", "[تاریخ تست واقعی]", "QA-01"),
        ("QA-02", "بیمار پرخطر", "سن بالا، SpO2 پایین، تنفس بالا، سابقه COPD/CHF", "نمایش نیازمند بررسی فوری، هشدارهای مهم و اقدام بعدی", "شواهد screenshot در docs/market و poster-assets موجود است", "Pass - evidence asset", "محدثه حاتمی کیا", "2026-06-27", "QA-02"),
        ("QA-03", "بیمار متوسط", "تب خفیف، علائم حیاتی نسبتاً پایدار", "ادامه ارزیابی معمول یا ریسک کمتر", "نیاز به اجرای دستی و ثبت خروجی", "Needs Run", "محدثه حاتمی کیا", "[تاریخ تست واقعی]", "QA-03"),
        ("QA-04", "اطلاعات کم", "فقط شکایت اصلی، سن، HR، SpO2 و سابقه قلبی", "ارزیابی اولیه با نمایش data completeness و missing fields", "در سناریوی sparse پیاده‌سازی شده؛ screenshot موجود است", "Pass - evidence asset", "محدثه حاتمی کیا", "2026-06-27", "QA-04"),
        ("QA-05", "درد قفسه سینه", "شکایت chestpain با سن بالا و سابقه coronary/MI", "هشدار مربوط به سابقه قلبی و اقدام بعدی", "نیاز به اجرای نهایی و ثبت screenshot", "Needs Run", "محدثه حاتمی کیا", "[تاریخ تست واقعی]", "QA-05"),
        ("QA-06", "موبایل", "باز کردن لینک public در viewport موبایل", "responsive بدون overlap و دکمه‌های قابل استفاده", "screenshots موبایل در docs/market موجود است", "Pass - evidence asset", "محدثه حاتمی کیا", "2026-06-27", "QA-06"),
        ("QA-07", "نصب PWA", "باز کردن HTTPS و انتخاب Add to Home Screen", "نصب روی home screen یا نمایش راهنمای نصب", "نصب واقعی روی گوشی استاد/تیم باید دستی تأیید شود", "Needs real device confirmation", "محدثه حاتمی کیا", "[تاریخ تست واقعی]", "QA-07"),
        ("QA-08", "QR Code", "اسکن QR پوستر/گزارش", "باز شدن لینک public app", "QR asset موجود است؛ اسکن واقعی باید ثبت شود", "Needs scan confirmation", "محمدرضا آرمان‌پور", "[تاریخ تست واقعی]", "FD-03"),
        ("QA-09", "بازخورد کاربر", "ارسال feedback از مسیر پایلوت یا endpoint", "ثبت CSV و status واقعی", "بازخورد خارجی تأییدشده در repo پیدا نشد", "Needs real feedback", "محمدرضا آرمان‌پور", "[تاریخ تست واقعی]", "FB-02"),
        ("QA-10", "کپی خلاصه", "پس از ارزیابی، دکمه کپی خلاصه زده شود", "متن خلاصه در clipboard قرار گیرد", "نیاز به اجرای دستی در browser", "Needs Run", "محدثه حاتمی کیا", "[تاریخ تست واقعی]", "QA-10"),
        ("QA-11", "پاک کردن فرم", "بعد از پر کردن سناریو، دکمه پاک کردن زده شود", "فرم reset و نتیجه اولیه شود", "نیاز به اجرای دستی در browser", "Needs Run", "محدثه حاتمی کیا", "[تاریخ تست واقعی]", "QA-11"),
    ]
    csv_file(
        "notion-qa-test-log.csv",
        [
            "Test ID",
            "Scenario",
            "Input Summary",
            "Expected Result",
            "Actual Result",
            "Status",
            "Tester",
            "Date",
            "Related Jira Issue",
        ],
        [
            {
                "Test ID": r[0],
                "Scenario": r[1],
                "Input Summary": r[2],
                "Expected Result": r[3],
                "Actual Result": r[4],
                "Status": r[5],
                "Tester": r[6],
                "Date": r[7],
                "Related Jira Issue": r[8],
            }
            for r in rows
        ],
    )


def build_lessons_learned() -> None:
    md_file(
        "notion-lessons-learned.md",
        """
        # درس‌آموخته‌ها

        ## مدیریت پروژه فقط کدنویسی نیست

        بخش فنی پروژه مهم بود، اما نقد TA نشان داد که برای درس مدیریت پروژه، backlog، Sprint، نقش اعضا، time tracking، ریسک، KPI، بازخورد و شواهد ابزارها به اندازه کد اهمیت دارند.

        ## مستندسازی همزمان با توسعه مهم است

        اگر مستندات بعد از توسعه نوشته شود، بخشی از منطق تصمیم‌ها گم می‌شود. Decision Log و Change Log کمک می‌کند نشان دهیم چرا هر تغییر انجام شد و چه اثری داشت.

        ## در سلامت، اخلاق و شفافیت بخشی از کیفیت فنی است

        در پروژه سلامت، کیفیت فقط AUC یا UI نیست. باید روشن باشد سیستم جایگزین متخصص نیست، داده‌های آینده استفاده نشده و خروجی‌ها با مسئولیت انسانی تفسیر می‌شوند.

        ## Accuracy کافی نیست و باید Recall/FPR هم بررسی شود

        Accuracy می‌تواند برای تریاژ گمراه‌کننده باشد. Recall بیمار پرخطر و FPR برای فشار منابع باید همزمان گزارش شوند تا trade-off انسانی و عملیاتی روشن باشد.

        ## تجربه کاربر در شرایط فشار باید ساده باشد

        کاربر اورژانس وقت خواندن متن‌های طولانی یا اصطلاحات مبهم را ندارد. نتیجه باید کوتاه، فارسی، قابل اقدام و قابل کپی باشد.

        ## AI باید کنترل انسانی داشته باشد

        AI می‌تواند سرعت ساخت و مستندسازی را بالا ببرد، اما نباید جایگزین تصمیم تیم شود. خروجی AI باید با evidence، تست، commit و محدودیت‌های واقعی کنترل شود.

        ## صداقت درباره داده‌های ناقص و بازخورد واقعی ارزش پروژه را بیشتر می‌کند

        گفتن «نیاز به تکمیل دارد» برای screenshot Jira، Notion یا بازخورد واقعی از ادعای غیرقابل اثبات بهتر است. این شفافیت در دفاع نهایی قابل توضیح و اخلاقی‌تر است.
        """,
    )


def jira_task(summary: str, desc: str, assignee: str, priority: str, points: int, sprint: str, status: str, labels: str, ac: str, dod: str, evidence: str, issue_type: str = "Story") -> dict[str, object]:
    return {
        "Issue Type": issue_type,
        "Summary": summary,
        "Description": desc,
        "Assignee": assignee,
        "Priority": priority,
        "Story Points": points,
        "Sprint": sprint,
        "Status": status,
        "Labels": labels,
        "Acceptance Criteria": ac,
        "Definition of Done": dod,
        "Notion Link Placeholder": "پس از import در Notion لینک صفحه/DB مرتبط را اضافه کنید.",
        "Evidence Link": evidence,
    }


def build_jira_import() -> None:
    epic_defs = [
        ("Problem Discovery & Scope", "شناخت مسئله، ذی‌نفعان، ارزش انسانی، دامنه MVP و محدودیت‌های اخلاقی.", "محمدامین پورمند", "Sprint 0", "scope,stakeholder,ethics"),
        ("Data & Model Logic", "طراحی منطق مدل، داده‌های triage-time، کنترل leakage و متریک‌های v7.", "محمدامین پورمند", "Sprint 1", "ml,data,metrics"),
        ("Backend / Evaluation Logic", "FastAPI، endpointها، منطق prediction، feedback export و CORS/deploy.", "محمدامین پورمند", "Sprint 2", "backend,api,fastapi"),
        ("Frontend & UX", "رابط فارسی، mobile-first، سناریوها، نتیجه قابل فهم و نصب PWA.", "محدثه حاتمی کیا", "Sprint 2", "frontend,ux,pwa"),
        ("Explainability & Safety", "هشدارهای مهم، اقدام بعدی، disclaimer، data completeness و ایمنی استفاده.", "محمدامین پورمند", "Sprint 3", "safety,explainability,ethics"),
        ("Feedback & Validation", "برنامه جمع‌آوری بازخورد، QA، تست پایلوت، ثبت نظر ذی‌نفعان و اصلاح محصول.", "محمدرضا آرمان‌پور", "Final Sprint", "feedback,validation,qa"),
        ("Project Management & Agile", "Backlog، Sprint، Burndown، KPI، risk، time tracking و role assignment.", "محمدرضا آرمان‌پور", "Sprint 3", "agile,kpi,risk"),
        ("Documentation & Knowledge Base", "Notion/Knowledge Base، decision log، AI usage، lessons و deliverables.", "محدثه حاتمی کیا", "Sprint 3", "docs,knowledge,ai-usage"),
        ("Final Deliverables", "Deploy عمومی، QR، پوستر، بسته بازار، فایل‌های Word و تحویل نهایی.", "محمدامین پورمند", "Final Sprint", "final,deploy,poster"),
    ]
    tasks_by_epic = {
        "Problem Discovery & Scope": [
            jira_task("تعریف مسئله تریاژ اورژانس", "شرح مسئله ازدحام، فشار زمانی و خطر تأخیر در شناسایی بیمار بحرانی.", "محمدامین پورمند", "High", 3, "Sprint 0", "Done", "scope,problem", "مسئله در یک متن رسمی و قابل دفاع ثبت شود.", "docs مرتبط موجود و به Notion لینک شود.", "docs/project-management-plan.md"),
            jira_task("ثبت ذی‌نفعان و کاربران هدف", "شناسایی پرستار تریاژ، تیم اورژانس، مدیریت بحران، استاد و کاربران پایلوت.", "محمدرضا آرمان‌پور", "High", 2, "Sprint 0", "Done", "stakeholder", "حداقل ۵ گروه ذی‌نفع با نیازشان ثبت شود.", "stakeholder register کامل باشد.", "docs/stakeholder-register.md"),
            jira_task("تعریف مرز اخلاقی decision-support", "تعیین اینکه سیستم جایگزین پزشک/پرستار نیست.", "محمدامین پورمند", "Highest", 3, "Sprint 0", "Done", "ethics,safety", "disclaimer در UI و docs آمده باشد.", "در model-card و privacy ثبت شود.", "docs/model-card.md; frontend/privacy.html"),
            jira_task("تعریف محدوده MVP", "مشخص کردن داخل/خارج از محدوده برای جلوگیری از scope creep.", "محمدامین پورمند", "High", 2, "Sprint 0", "Done", "mvp,scope", "دامنه محصول و خارج از محدوده روشن باشد.", "overview و roadmap تکمیل شود.", "docs/roadmap.md"),
            jira_task("تعریف ارزش انسانی، اجتماعی و ملی", "نوشتن ارزش پروژه برای دفاع استاد و پوستر.", "محمدرضا آرمان‌پور", "Medium", 2, "Sprint 0", "Done", "value,social", "ارزش انسانی/اجتماعی/ملی جداگانه ثبت شود.", "در report/poster قابل کپی باشد.", "poster-final-assets-fa.md"),
        ],
        "Data & Model Logic": [
            jira_task("انتخاب featureهای زمان تریاژ", "استفاده از سن، شکایت، علائم حیاتی و سابقه قابل پرسش.", "محمدامین پورمند", "Highest", 5, "Sprint 1", "Done", "triage-time,data", "هیچ داده post-triage در ورودی نهایی نباشد.", "Model Card شامل included/excluded sources باشد.", "docs/model-card.md"),
            jira_task("کنترل data leakage", "حذف labs، meds، imaging، disposition و انتخاب threshold روی validation.", "محمدامین پورمند", "Highest", 5, "Sprint 1", "Done", "leakage,validation", "leakage control در docs ثبت شود.", "metrics و train script قابل اشاره باشند.", "ml/train.py; reports/model/metrics_v7.json"),
            jira_task("آموزش و ارزیابی مدل v7", "ثبت AUC، Recall، Precision، FPR و threshold نهایی.", "محمدامین پورمند", "Highest", 8, "Sprint 3", "Done", "v7,metrics", "AUC>=0.90 و Recall>=0.92 در test گزارش شود.", "metrics_v7.json و model-card به‌روز باشد.", "reports/model/metrics_v7.json"),
            jira_task("پشتیبانی از ورودی ناقص", "استفاده از missingness و data completeness.", "محمدامین پورمند", "High", 3, "Sprint 2", "Done", "sparse-input", "سناریوی sparse خروجی بدهد و missing fields نشان دهد.", "UI و API خروجی کامل برگردانند.", "frontend/app.js; ml/inference.py"),
            jira_task("ثبت نمودارهای مدل", "Confusion Matrix، ROC، PR و SHAP/Feature Importance.", "محمدامین پورمند", "Medium", 3, "Sprint 3", "Done", "charts,poster", "نمودارها در reports/poster-assets موجود باشند.", "assets با نام واضح ذخیره شوند.", "poster-assets/; reports/model/"),
        ],
        "Backend / Evaluation Logic": [
            jira_task("ساخت endpoint /health", "Endpoint سلامت سرویس برای local/deploy.", "محمدامین پورمند", "High", 2, "Sprint 2", "Done", "api,health", "GET /health status ok بدهد.", "در docs/api-documentation.md ثبت شود.", "backend/main.py"),
            jira_task("ساخت endpoint /model-info", "نمایش نسخه مدل، متریک‌ها و operating points.", "محمدامین پورمند", "High", 2, "Sprint 2", "Done", "api,model-info", "اطلاعات v7 و decision_support_only برگردد.", "endpoint در backend موجود باشد.", "backend/main.py"),
            jira_task("ساخت endpoint /predict", "دریافت PatientInput و خروجی PredictionOutput.", "محمدامین پورمند", "Highest", 5, "Sprint 2", "Done", "api,predict", "با ورودی کامل و ناقص خروجی بدهد.", "schema و inference هماهنگ باشند.", "backend/main.py; backend/schemas.py"),
            jira_task("تنظیم CORS و config deploy", "آماده‌سازی allow origins و فایل‌های Render/Railway.", "محمدامین پورمند", "Medium", 2, "Sprint 6", "Done", "cors,deploy", "CORS برای تست قابل تنظیم باشد.", "DEPLOYMENT.md توضیح دهد origin واقعی جایگزین شود.", "DEPLOYMENT.md; render.yaml; railway.toml"),
            jira_task("نگه داشتن مسیر feedback export", "ثبت feedback واقعی در CSV برای پایلوت.", "محمدرضا آرمان‌پور", "Medium", 3, "Sprint 5", "Done", "feedback,api", "POST /feedback و GET /feedback/export تعریف شوند.", "برای پایلوت واقعی قابل استفاده باشد.", "backend/main.py"),
        ],
        "Frontend & UX": [
            jira_task("طراحی فارسی و RTL", "UI کامل به فارسی و راست‌به‌چپ باشد.", "محدثه حاتمی کیا", "High", 3, "Sprint 2", "Done", "rtl,fa", "html lang=fa و dir=rtl داشته باشد.", "متن‌ها فارسی و ساده باشند.", "frontend/index.html"),
            jira_task("اصلاح نام محصول به امداد یار", "جایگزینی عنوان‌های فنی/قدیمی با نام محصول.", "محدثه حاتمی کیا", "High", 2, "Sprint 6", "Done", "branding", "عنوان UI امداد یار باشد.", "manifest و title هماهنگ شود.", "frontend/index.html; frontend/manifest.webmanifest"),
            jira_task("جابجایی نمونه‌های آماده تست", "نمونه‌ها پایین فرم قرار بگیرند تا با ورودی کاربر اشتباه نشوند.", "محدثه حاتمی کیا", "Medium", 2, "Sprint 6", "Done", "ux,scenario", "سناریوها در بخش اختیاری باشند.", "کاربر قبل از فرم اصلی با آنها روبه‌رو نشود.", "frontend/index.html"),
            jira_task("ساخت نتیجه قابل فهم", "جایگزینی اصطلاحات سخت با پیام‌های عملی.", "محدثه حاتمی کیا", "High", 3, "Sprint 6", "Done", "copywriting,result", "خروجی شامل وضعیت، هشدار و اقدام باشد.", "ESI تنها متن اصلی نباشد.", "frontend/app.js"),
            jira_task("آماده‌سازی نصب PWA", "دکمه/راهنمای نصب، service worker و manifest.", "محدثه حاتمی کیا", "High", 3, "Sprint 4", "Done", "pwa,mobile", "کاربر راهنمای Android/iPhone ببیند.", "PWA assets موجود باشد.", "frontend/sw.js; frontend/manifest.webmanifest"),
        ],
        "Explainability & Safety": [
            jira_task("نمایش هشدارهای مهم", "تبدیل safety flags به زبان قابل فهم فارسی.", "محمدامین پورمند", "Highest", 3, "Sprint 3", "Done", "safety,flags", "هشدارها در بخش جدا نمایش داده شوند.", "اصطلاحات مبهم حذف شود.", "frontend/index.html; frontend/app.js"),
            jira_task("نمایش اقدام بعدی", "پیشنهاد next action برای مسیر بعدی کاربر.", "محدثه حاتمی کیا", "High", 3, "Sprint 3", "Done", "next-action,workflow", "حداقل یک اقدام بعدی پس از ارزیابی نمایش داده شود.", "API/browser model خروجی action بدهد.", "frontend/app.js; ml/inference.py"),
            jira_task("نمایش کامل بودن داده", "درصد data completeness و missing fields.", "محمدامین پورمند", "High", 2, "Sprint 3", "Done", "data-quality", "با ورودی ناقص درصد و فیلدهای پیشنهادی نشان داده شود.", "نتیجه بیش از حد قطعی به نظر نرسد.", "frontend/app.js"),
            jira_task("تکرار disclaimer اخلاقی", "توضیح ثابت درباره عدم جایگزینی متخصص.", "محدثه حاتمی کیا", "Highest", 2, "Sprint 2", "Done", "ethics,disclaimer", "در UI و privacy موجود باشد.", "متن کوتاه و واضح باشد.", "frontend/index.html; frontend/privacy.html"),
            jira_task("ثبت محدودیت‌های مدل", "محدودیت داده، نیاز به validation و fairness.", "محمدامین پورمند", "High", 3, "Sprint 3", "Done", "model-card,limitations", "محدودیت‌ها در model card آمده باشد.", "در ارائه ادعای درمانی نشود.", "docs/model-card.md"),
        ],
        "Feedback & Validation": [
            jira_task("طراحی فرم جمع‌آوری بازخورد", "پرسش‌های کوتاه برای UI، خروجی و disclaimer.", "محمدرضا آرمان‌پور", "High", 2, "Final Sprint", "To Do", "feedback,form", "فرم با ۵ سؤال آماده و ارسال شود.", "حداقل ۵ پاسخ واقعی ثبت شود.", "project-management-final-package/stakeholder-feedback-form.md"),
            jira_task("تأیید ۹ بازخورد پرستار تریاژ", "تبدیل pending confirmation به confirmed فقط بعد از پرسش واقعی.", "محمدرضا آرمان‌پور", "Highest", 5, "Final Sprint", "In Progress", "feedback,nurse", "برای هر نفر کد ناشناس و تاریخ ثبت شود.", "بدون تأیید status confirmed نشود.", "docs/triage-nurse-feedback-confirmation.md"),
            jira_task("ثبت feedback واقعی در Notion", "وارد کردن پاسخ‌های واقعی در database بازخورد.", "محمدرضا آرمان‌پور", "High", 3, "Final Sprint", "To Do", "notion,feedback", "هر feedback score، comment و action taken داشته باشد.", "لینک evidence و owner مشخص باشد.", "project-management-final-package/notion-stakeholder-feedback.csv"),
            jira_task("اجرای QA سناریوهای اصلی", "فرم خالی، پرخطر، متوسط، sparse، موبایل، PWA، QR.", "محدثه حاتمی کیا", "High", 5, "Final Sprint", "To Do", "qa,test", "همه سناریوها status و تاریخ داشته باشند.", "screenshot یا توضیح نتیجه ثبت شود.", "project-management-final-package/notion-qa-test-log.csv"),
            jira_task("تحلیل تغییرات بعد از feedback", "ثبت action taken برای هر feedback واقعی.", "محمدرضا آرمان‌پور", "Medium", 3, "Final Sprint", "To Do", "feedback,iteration", "حداقل ۲ تغییر یا backlog item از feedback استخراج شود.", "در change log یا sprint review ثبت شود.", "docs/knowledge-base/stakeholder-feedback-log.md"),
        ],
        "Project Management & Agile": [
            jira_task("ساخت Jira Scrum Project", "ایجاد project واقعی و board برای امداد یار.", "محمدرضا آرمان‌پور", "Highest", 3, "Final Sprint", "To Do", "jira,agile", "Project name و workflow مطابق راهنما باشد.", "screenshot board گرفته شود.", "project-management-final-package/jira-board-setup.md"),
            jira_task("Import کردن Jira issues", "وارد کردن jira-issues-import.csv و map کردن fieldها.", "محمدرضا آرمان‌پور", "Highest", 5, "Final Sprint", "To Do", "jira,import", "حداقل ۹ epic و ۴۵ task/story وارد شوند.", "assignee و sprint قابل مشاهده باشد.", "project-management-final-package/jira-issues-import.csv"),
            jira_task("تنظیم Sprintها و Burndown", "ساخت sprintهای پروژه و نمایش burndown.", "محمدرضا آرمان‌پور", "High", 3, "Final Sprint", "To Do", "sprint,burndown", "Sprintها فعال/closed و نمودار قابل screenshot باشد.", "time/story points ثبت شود.", "docs/artifacts/burndown.svg"),
            jira_task("ثبت Time Tracking", "ثبت Original Estimate و Time Spent برای اعضا.", "محمدرضا آرمان‌پور", "High", 3, "Final Sprint", "To Do", "time-tracking,team", "برای هر عضو چند issue با time spent وجود داشته باشد.", "گزارش نقش تیمی قابل دفاع باشد.", "docs/artifacts/time-tracking-log.csv"),
            jira_task("لینک دادن Jira به GitHub commits", "اضافه کردن commit/file evidence در description یا issue links.", "محمدامین پورمند", "Medium", 2, "Final Sprint", "To Do", "github,jira,evidence", "هر epic حداقل یک evidence link داشته باشد.", "commit hash یا file path در issue visible باشد.", "git log --oneline"),
        ],
        "Documentation & Knowledge Base": [
            jira_task("ساخت Notion Home", "ایجاد صفحه اصلی دانشنامه پروژه.", "محدثه حاتمی کیا", "Highest", 3, "Final Sprint", "To Do", "notion,home", "صفحه شامل معرفی، لینک‌ها و وضعیت پروژه باشد.", "لینک Notion در README/Jira ثبت شود.", "project-management-final-package/notion-home.md"),
            jira_task("Import کردن decision log", "ساخت database تصمیم‌ها در Notion.", "محدثه حاتمی کیا", "High", 3, "Final Sprint", "To Do", "notion,decision-log", "ستون‌ها و relationها درست map شوند.", "حداقل تصمیم‌های کلیدی وارد شوند.", "project-management-final-package/notion-decision-log.csv"),
            jira_task("Import کردن change log", "ساخت database تغییرات از git history.", "محدثه حاتمی کیا", "High", 3, "Final Sprint", "To Do", "notion,change-log", "هر تغییر دلیل، اثر و evidence داشته باشد.", "به Jira issue لینک شود.", "project-management-final-package/notion-change-log.csv"),
            jira_task("ثبت AI Usage Report", "انتقال گزارش استفاده از AI و کنترل انسانی.", "محمدامین پورمند", "High", 2, "Final Sprint", "To Do", "ai-usage,ethics", "گزارش نشان دهد AI کمک‌یار بوده نه مالک پروژه.", "در Notion و گزارش نهایی لینک شود.", "project-management-final-package/notion-ai-usage-report.md"),
            jira_task("ثبت Lessons Learned", "انتقال درس‌آموخته‌های مدیریت پروژه.", "محدثه حاتمی کیا", "Medium", 2, "Final Sprint", "To Do", "lessons,knowledge", "حداقل ۶ درس‌آموخته ثبت شود.", "در ارائه به آن اشاره شود.", "project-management-final-package/notion-lessons-learned.md"),
        ],
        "Final Deliverables": [
            jira_task("تست لینک عمومی اپ", "باز کردن GitHub Pages روی موبایل و دسکتاپ.", "محمدامین پورمند", "Highest", 2, "Final Sprint", "To Do", "deploy,public", "URL بدون local server باز شود.", "screenshot دسکتاپ و موبایل ذخیره شود.", APP_URL),
            jira_task("به‌روزرسانی QR Code", "اطمینان از اینکه QR به لینک نهایی اشاره می‌کند.", "محمدرضا آرمان‌پور", "High", 2, "Final Sprint", "To Do", "qr,poster", "QR با گوشی اسکن و ثبت شود.", "در پوستر نهایی قرار گیرد.", "docs/artifacts/emdadyar-pwa-qr.png"),
            jira_task("آماده‌سازی پوستر نهایی", "استفاده از poster-final-assets-fa و نمودارها.", "محدثه حاتمی کیا", "High", 5, "Final Sprint", "To Do", "poster,a0", "پوستر شامل Agile، KPI، Burndown، تیم و QR باشد.", "خروجی A0 چاپی آماده شود.", "poster-final-assets-fa.md; poster-assets/"),
            jira_task("ساخت بسته ارسال استاد", "لینک اپ، QR، docx و instructions.", "محمدامین پورمند", "High", 3, "Final Sprint", "Done", "professor,package", "فایل handoff برای استاد آماده باشد.", "در deliverables قرار گیرد.", "docs/deliverables/Emdadyar_Mobile_App_For_Professor.docx"),
            jira_task("گرفتن screenshot واقعی Jira و Notion", "شاهد نهایی استفاده از ابزارها.", "محدثه حاتمی کیا", "Highest", 3, "Final Sprint", "To Do", "screenshot,evidence", "حداقل ۴ screenshot: Jira backlog، Sprint board، Notion home، Notion database.", "در docs/evidence یا deliverables قرار گیرد.", "نیاز به تکمیل دارد"),
        ],
    }

    rows: list[dict[str, object]] = []
    for epic_name, epic_desc, epic_owner, sprint, labels in epic_defs:
        rows.append(
            {
                "Issue Type": "Epic",
                "Summary": epic_name,
                "Description": epic_desc,
                "Epic Name": epic_name,
                "Parent": "",
                "Assignee": epic_owner,
                "Priority": "High",
                "Story Points": 8,
                "Sprint": sprint,
                "Status": "To Do" if "Final" in sprint else "Done",
                "Labels": labels,
                "Acceptance Criteria": "Epic شامل حداقل ۵ task/story با owner، evidence و DoD باشد.",
                "Definition of Done": "همه taskهای ضروری انجام یا با وضعیت Needs Completion صادقانه ثبت شوند.",
                "Notion Link Placeholder": "پس از ساخت Notion لینک epic/صفحه مرتبط را وارد کنید.",
                "Evidence Link": "project-management-final-package/",
            }
        )
        for task in tasks_by_epic[epic_name]:
            task = task.copy()
            task["Epic Name"] = epic_name
            task["Parent"] = epic_name
            rows.append(task)

    csv_file(
        "jira-issues-import.csv",
        [
            "Issue Type",
            "Summary",
            "Description",
            "Epic Name",
            "Parent",
            "Assignee",
            "Priority",
            "Story Points",
            "Sprint",
            "Status",
            "Labels",
            "Acceptance Criteria",
            "Definition of Done",
            "Notion Link Placeholder",
            "Evidence Link",
        ],
        rows,
    )


def build_jira_board_setup() -> None:
    md_file(
        "jira-board-setup.md",
        f"""
        # راهنمای ساخت Jira Board برای امداد یار

        ## 1. ساخت پروژه

        1. وارد Jira شوید: {ltr(JIRA_WORKSPACE_URL)}
        2. گزینه Create Project را بزنید.
        3. نوع پروژه را Scrum انتخاب کنید، نه Kanban.
        4. نام پروژه:
           {ltr("Emdadyar - Emergency Decision Support")}
        5. Key پیشنهادی:
           {ltr("EMD")}
        6. اگر Jira فارسی/انگلیسی بود مهم نیست؛ نام issueها فارسی هستند.

        ## 2. Board Type

        | گزینه | مقدار پیشنهادی |
        |---|---|
        | Board | Scrum Board |
        | Estimation | Story Points |
        | Time Tracking | فعال |
        | Reports | Burndown، Sprint Report، Velocity |

        ## 3. Workflow پیشنهادی

        | ستون | معنی |
        |---|---|
        | Backlog | ایده یا کار هنوز وارد sprint نشده |
        | Selected for Sprint | انتخاب‌شده برای sprint |
        | In Progress | در حال انجام |
        | Review / QA | آماده بازبینی تیم، تست یا مستندسازی |
        | Done | انجام‌شده با evidence |

        ## 4. Issue Types

        - Epic
        - Story
        - Task
        - Bug
        - Spike

        اگر Jira اجازه import Epic Name نداد، اول ۹ Epic را دستی بسازید و سپس taskها را import کنید.

        ## 5. Epics

        1. Problem Discovery & Scope
        2. Data & Model Logic
        3. Backend / Evaluation Logic
        4. Frontend & UX
        5. Explainability & Safety
        6. Feedback & Validation
        7. Project Management & Agile
        8. Documentation & Knowledge Base
        9. Final Deliverables

        ## 6. Import CSV

        فایل import:
        {ltr("project-management-final-package/jira-issues-import.csv")}

        Mapping پیشنهادی:

        | CSV Column | Jira Field |
        |---|---|
        | Issue Type | Issue Type |
        | Summary | Summary |
        | Description | Description |
        | Epic Name | Epic Name یا Parent/Epic Link |
        | Parent | Parent یا Epic Link |
        | Assignee | Assignee |
        | Priority | Priority |
        | Story Points | Story Points |
        | Sprint | Sprint |
        | Status | Status |
        | Labels | Labels |
        | Acceptance Criteria | Description یا Custom Field |
        | Definition of Done | Description یا Custom Field |
        | Notion Link Placeholder | Description |
        | Evidence Link | Description یا Web Link |

        ## 7. Sprints پیشنهادی

        | Sprint | بازه قابل دفاع | خروجی |
        |---|---|---|
        | Sprint 0 | 2026-06-01 تا 2026-06-02 | مسئله، scope، اخلاق |
        | Sprint 1 | 2026-06-02 تا 2026-06-08 | مدل و leakage control |
        | Sprint 2 | 2026-06-04 تا 2026-06-10 | backend و UI اولیه |
        | Sprint 3 | 2026-06-10 تا 2026-06-15 | docs، KPI، risk، QA |
        | Final Sprint | 2026-06-20 تا 2026-06-29 | deploy، QR، Notion/Jira، final deliverables |

        اگر تاریخ واقعی جلسات یا کارها متفاوت است، در Jira همان تاریخ واقعی تیم را وارد کنید.

        ## 8. Labels

        از labelهای زیر استفاده کنید:

        {ltr("scope, ethics, ml, leakage, api, frontend, pwa, safety, feedback, agile, kpi, risk, documentation, notion, jira, deploy, poster, qa")}

        ## 9. Components

        | Component | مالک پیشنهادی |
        |---|---|
        | ML Model | محمدامین پورمند |
        | Backend/API | محمدامین پورمند |
        | Frontend/PWA | محدثه حاتمی کیا |
        | Project Control | محمدرضا آرمان‌پور |
        | Documentation | محدثه حاتمی کیا |
        | Validation/Feedback | محمدرضا آرمان‌پور |
        | Final Delivery | محمدامین پورمند |

        ## 10. لینک دادن Jira به Notion

        1. پس از ساخت Notion Home، URL صفحه را کپی کنید.
        2. در Jira یک Project Shortcut با نام «Notion Knowledge Base» بسازید.
        3. برای هر Epic، لینک صفحه Notion مرتبط را در Description قرار دهید.
        4. در Notion هم یک property به نام Jira Issue بسازید و key issue را وارد کنید.

        ## 11. لینک دادن Jira به GitHub commits

        چون commitهای قدیمی key Jira ندارند، ساده‌ترین راه:

        1. در description هر issue بخش Evidence بسازید.
        2. commit hash یا مسیر فایل را بگذارید؛ مثال:
           {ltr("commit 43737c8 - frontend/index.html")}
        3. برای commitهای بعدی، نام issue را در commit message بیاورید؛ مثال:
           {ltr("EMD-23 update stakeholder feedback log")}
        4. در GitHub repository، اگر دسترسی داشتی Jira integration را فعال کن تا commitها خودکار لینک شوند.

        ## 12. Screenshotهایی که باید برای استاد بگیری

        - Backlog با Epics و taskها
        - Active Sprint با ستون‌های workflow
        - یک issue باز شده که Assignee، Story Point، Time Tracking و Evidence Link دارد
        - Burndown chart
        - صفحه Project Settings یا Components برای نشان دادن roleها
        """,
    )


def build_notion_import_guide() -> None:
    md_file(
        "notion-import-guide.md",
        """
        # راهنمای ورود بسته به Notion

        ## 1. ساخت ساختار صفحه‌ها

        در Notion یک صفحه اصلی بسازید:

        «امداد یار | دانشنامه پروژه و مدیریت دانش»

        سپس این sub-pageها را بسازید:

        | صفحه | فایل منبع |
        |---|---|
        | Project Overview | notion-project-overview.md |
        | Product Features | notion-product-features.md |
        | Sprint Notes | notion-sprint-notes.md |
        | Meeting Notes | notion-meeting-notes.md |
        | AI Usage Report | notion-ai-usage-report.md |
        | Lessons Learned | notion-lessons-learned.md |
        | Jira Import & Board Setup | jira-board-setup.md |
        | Missing Info Checklist | missing-info-checklist.md |

        ## 2. وارد کردن Markdownها

        بهترین روش:

        1. محتوای هر فایل markdown را باز کنید.
        2. متن داخل فایل را در صفحه مربوط Notion paste کنید.
        3. اگر جدول‌ها بهم ریختند، از Notion table ساده استفاده کنید.
        4. لینک‌های مسیر فایل را به repository یا GitHub raw/file link تبدیل کنید.

        ## 3. ساخت Databaseها از CSV

        فایل‌های زیر را با گزینه Import یا Merge with CSV وارد کنید:

        | Database | فایل |
        |---|---|
        | Decision Log | notion-decision-log.csv |
        | Change Log | notion-change-log.csv |
        | Risk Register | notion-risk-register.csv |
        | Stakeholder Feedback | notion-stakeholder-feedback.csv |
        | QA Test Log | notion-qa-test-log.csv |

        ## 4. Relationهای پیشنهادی

        | From Database | Relation To | دلیل |
        |---|---|---|
        | Decision Log | Jira Issues | هر تصمیم باید issue مرتبط داشته باشد |
        | Change Log | Decision Log | بعضی تغییرها نتیجه تصمیم هستند |
        | Risk Register | Jira Issues | هر ریسک باید action یا task داشته باشد |
        | QA Test Log | Jira Issues | تست‌ها باید به taskهای QA وصل شوند |
        | Stakeholder Feedback | Change Log | هر بازخورد مهم باید action taken داشته باشد |

        ## 5. Propertyهای مهم Notion

        برای هر database این propertyها را بسازید:

        - Owner: Person یا Text
        - Status: Select
        - Sprint: Select
        - Jira Issue: URL یا Text
        - Evidence Link: URL یا Text
        - Last Updated: Date
        - Needs Completion: Checkbox

        ## 6. اضافه کردن Jira issue link

        پس از import در Jira:

        1. key هر issue مثل EMD-12 را بردارید.
        2. در Notion property «Jira Issue» وارد کنید.
        3. در Jira هم لینک Notion page/database item را در description یا web link بگذارید.

        ## 7. اضافه کردن Evidence Link

        برای هر item، حداقل یکی از این شواهد را بگذارید:

        - مسیر فایل در repo، مثل frontend/app.js
        - commit hash، مثل 43737c8
        - artifact تصویری، مثل poster-assets/ui-mobile-view.png
        - گزارش، مثل reports/model/metrics_v7.json
        - لینک عمومی اپ
        - screenshot واقعی Jira/Notion پس از ساخت

        ## 8. مرتب کردن صفحه اصلی مثل دانشنامه پروژه

        ترتیب پیشنهادی صفحه Home:

        1. معرفی کوتاه و warning اخلاقی
        2. لینک اپ، repo، Jira و Notion
        3. وضعیت فعلی MVP
        4. اعضای تیم و نقش‌ها
        5. Quick Links به databaseها
        6. آخرین Sprint و کارهای باقی‌مانده
        7. بخش Evidence برای screenshotها

        ## 9. نکته مهم برای صداقت دفاع

        هر چیزی که هنوز واقعی نیست، با عبارت «نیاز به تکمیل دارد» نگه دارید. بعد از ساخت واقعی Jira board، Notion database، گرفتن feedback واقعی و screenshotها، همان itemها را به Done یا Confirmed تغییر دهید.
        """,
    )


def build_missing_info_checklist() -> None:
    md_file(
        "missing-info-checklist.md",
        f"""
        # چک‌لیست اطلاعات ناقص و نیازمند تکمیل واقعی

        | مورد | وضعیت فعلی | اقدام لازم | مالک پیشنهادی |
        |---|---|---|---|
        | تاریخ دقیق جلسات | بعضی تاریخ‌ها از docs/commit history برداشت شده‌اند | تاریخ واقعی جلسه‌ها را با تیم تطبیق دهید | محمدامین پورمند |
        | نام دقیق Jira Project | هنوز در repo screenshot/لینک project واقعی نیست | Scrum project با نام {ltr("Emdadyar - Emergency Decision Support")} بسازید | محمدرضا آرمان‌پور |
        | لینک واقعی Jira Board | فقط workspace link موجود است: {ltr(JIRA_WORKSPACE_URL)} | لینک board را در Notion Home و README وارد کنید | محمدرضا آرمان‌پور |
        | لینک واقعی Notion | {NOTION_PLACEHOLDER} | صفحه Notion را بسازید و لینک را جایگزین کنید | محدثه حاتمی کیا |
        | بازخورد واقعی کاربران | بازخورد خارجی تأییدشده در repo پیدا نشد | حداقل ۵ بازخورد واقعی با تاریخ و کد ناشناس ثبت کنید | محمدرضا آرمان‌پور |
        | تأیید ۹ نظر پرستار تریاژ | در وضعیت pending confirmation | از افراد واقعی بپرسید؛ بعد status را confirmed/rejected کنید | محمدرضا آرمان‌پور |
        | لینک واقعی Jira issues | CSV آماده است اما import واقعی باید انجام شود | پس از import، keyها مثل EMD-12 را در Notion وارد کنید | محمدرضا آرمان‌پور |
        | screenshot واقعی Jira board | موجود نیست | از Backlog، Active Sprint، Burndown و issue جزئیات screenshot بگیرید | محدثه حاتمی کیا |
        | screenshot واقعی Notion | موجود نیست | از Home، Decision Log، Risk Register و Feedback database screenshot بگیرید | محدثه حاتمی کیا |
        | زمان دقیق همکاری اعضا | time tracking تخمینی/مستند در CSV موجود است | با اعضا تأیید کنید و در Jira Time Tracking وارد کنید | محمدرضا آرمان‌پور |
        | تست نصب PWA روی گوشی واقعی | assets موجود است؛ نصب واقعی باید تأیید شود | لینک public را روی Android/iPhone تست و screenshot بگیرید | محدثه حاتمی کیا |
        | تست QR روی گوشی | QR asset موجود است | QR را اسکن و باز شدن لینک را ثبت کنید | محمدرضا آرمان‌پور |
        | خروجی PDF/Word نهایی Notion | هنوز ساخته نشده | پس از تکمیل Notion، export PDF/Markdown بگیرید | محدثه حاتمی کیا |
        | اعتبارسنجی بالینی | انجام نشده | در گزارش به عنوان محدودیت و فاز بعدی ثبت شود | محمدامین پورمند |
        | تحلیل fairness کامل | انجام نشده | در فاز بعدی subgroup analysis تعریف شود | محمدامین پورمند |
        | دامنه نهایی غیر GitHub Pages | فعلاً GitHub Pages است | اگر دامنه یا backend عمومی جدا ساختید، QR و docs را به‌روزرسانی کنید | محمدامین پورمند |
        """,
    )


def build_readme() -> None:
    md_file(
        "README.md",
        f"""
        # بسته نهایی انتقال مدیریت پروژه به Notion و Jira

        این پوشه برای پر کردن سریع و دقیق Notion و Jira پروژه «امداد یار» ساخته شده است. فایل‌ها فارسی، راست‌چین، قابل کپی و همراه با evidence link هستند.

        ## خروجی‌های اصلی

        | فایل | کاربرد |
        |---|---|
        | {ltr("notion-home.md")} | صفحه اصلی Notion |
        | {ltr("notion-project-overview.md")} | شرح کامل پروژه |
        | {ltr("notion-product-features.md")} | مستند قابلیت‌های محصول |
        | {ltr("notion-decision-log.csv")} | دیتابیس تصمیم‌ها |
        | {ltr("notion-change-log.csv")} | دیتابیس تغییرات از git history |
        | {ltr("notion-sprint-notes.md")} | یادداشت Sprintها |
        | {ltr("notion-meeting-notes.md")} | صورت‌جلسه‌ها با شفافیت درباره تاریخ‌ها |
        | {ltr("notion-risk-register.csv")} | دیتابیس ریسک‌ها |
        | {ltr("notion-ai-usage-report.md")} | گزارش استفاده از AI |
        | {ltr("notion-stakeholder-feedback.csv")} | ساختار ثبت بازخورد واقعی |
        | {ltr("notion-qa-test-log.csv")} | دیتابیس تست‌ها |
        | {ltr("notion-lessons-learned.md")} | درس‌آموخته‌ها |
        | {ltr("jira-issues-import.csv")} | import آماده Jira، شامل ۹ Epic و حداقل ۵ task برای هر Epic |
        | {ltr("jira-board-setup.md")} | راهنمای ساخت Jira board |
        | {ltr("notion-import-guide.md")} | راهنمای ورود فایل‌ها به Notion |
        | {ltr("missing-info-checklist.md")} | مواردی که واقعاً باید تکمیل شوند |
        | {ltr("stakeholder-feedback-form.md")} | فرم پیشنهادی برای گرفتن بازخورد واقعی |

        ## اصل مهم

        این بسته عمداً موارد غیرواقعی را جعل نمی‌کند. هرجا screenshot واقعی، بازخورد واقعی، لینک واقعی Jira یا Notion وجود نداشته باشد، با عبارت «نیاز به تکمیل دارد» مشخص شده است.
        """,
    )


def main() -> None:
    build_readme()
    build_notion_home()
    build_project_overview()
    build_product_features()
    build_decision_log()
    build_change_log()
    build_sprint_notes()
    build_meeting_notes()
    build_risk_register()
    build_ai_usage_report()
    build_stakeholder_feedback()
    build_qa_test_log()
    build_lessons_learned()
    build_jira_import()
    build_jira_board_setup()
    build_notion_import_guide()
    build_missing_info_checklist()

    manifest = {
        "package": "project-management-final-package",
        "product_name": "امداد یار",
        "app_url": APP_URL,
        "repo_url": REPO_URL,
        "generated_files": sorted(
            path.name
            for path in OUT.iterdir()
            if path.is_file() and path.name != "package-manifest.json"
        ),
        "model_version": METRICS["version"],
        "model_test_metrics": {
            "auc": round(TEST_METRICS["auc"], 4),
            "recall": round(TEST_METRICS["recall"], 4),
            "precision": round(TEST_METRICS["precision"], 4),
            "fpr": round(TEST_METRICS["fpr"], 4),
            "threshold": round(TEST_METRICS["threshold"], 4),
        },
        "honesty_note": "Real Jira/Notion screenshots and real external feedback must be added after actual tool setup and field confirmation.",
    }
    (OUT / "package-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Built {len(manifest['generated_files'])} files in {OUT}")


if __name__ == "__main__":
    main()
