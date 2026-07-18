from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "project-management-final-package"
REPORT = ROOT / "reports" / "project-management-package-audit.json"

REQUIRED_FILES = {
    "notion-home.md",
    "notion-project-overview.md",
    "notion-product-features.md",
    "notion-decision-log.csv",
    "notion-change-log.csv",
    "notion-sprint-notes.md",
    "notion-meeting-notes.md",
    "notion-risk-register.csv",
    "notion-ai-usage-report.md",
    "notion-stakeholder-feedback.csv",
    "notion-qa-test-log.csv",
    "notion-lessons-learned.md",
    "jira-issues-import.csv",
    "jira-board-setup.md",
    "notion-import-guide.md",
    "missing-info-checklist.md",
}

MOJIBAKE_MARKERS = ("Ã", "Â", "Ø", "Ù", "â€", "ï¿½", "\ufffd", "提示")
CONVERSATIONAL_MARKERS = (
    "chatgpt",
    "codex",
    "به من بگو",
    "به چت",
    "انجام بده",
    "کپی کن و",
    "original status",
    "notion link placeholder",
)
PERSIAN_RE = re.compile(r"[\u0600-\u06ff]")


def audit_csv(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    width = len(rows[0]) if rows else 0
    bad_rows = [index + 1 for index, row in enumerate(rows) if len(row) != width]
    return {
        "rows_including_header": len(rows),
        "data_rows": max(0, len(rows) - 1),
        "columns": width,
        "inconsistent_rows": bad_rows,
    }


def main() -> None:
    files = sorted(path for path in PACKAGE.iterdir() if path.is_file())
    missing = sorted(REQUIRED_FILES - {path.name for path in files})
    encoding_errors: list[str] = []
    mojibake: dict[str, list[str]] = {}
    conversational: dict[str, list[str]] = {}
    rtl_missing: list[str] = []
    csv_results: dict[str, dict[str, object]] = {}
    json_errors: dict[str, str] = {}

    for path in files:
        if path.suffix.lower() not in {".md", ".csv", ".json"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            encoding_errors.append(f"{path.name}: {exc}")
            continue

        marker_hits = [marker for marker in MOJIBAKE_MARKERS if marker in text]
        if marker_hits:
            mojibake[path.name] = marker_hits

        lowered = text.casefold()
        conversation_hits = [marker for marker in CONVERSATIONAL_MARKERS if marker in lowered]
        if conversation_hits:
            conversational[path.name] = conversation_hits

        if path.suffix.lower() == ".md" and PERSIAN_RE.search(text):
            if 'dir="rtl"' not in text and "rtl:" not in text and "rtl-normalized" not in text:
                rtl_missing.append(path.name)

        if path.suffix.lower() == ".csv":
            csv_results[path.name] = audit_csv(path)

        if path.suffix.lower() == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                json_errors[path.name] = str(exc)

    inconsistent_csv = {
        name: result["inconsistent_rows"]
        for name, result in csv_results.items()
        if result["inconsistent_rows"]
    }
    passed = not any(
        [missing, encoding_errors, mojibake, conversational, rtl_missing, inconsistent_csv, json_errors]
    )
    report = {
        "package": str(PACKAGE),
        "file_count": len(files),
        "required_files_missing": missing,
        "utf8_decode_errors": encoding_errors,
        "mojibake_hits": mojibake,
        "conversational_marker_hits": conversational,
        "markdown_rtl_missing": rtl_missing,
        "csv": csv_results,
        "json_errors": json_errors,
        "passed": passed,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
