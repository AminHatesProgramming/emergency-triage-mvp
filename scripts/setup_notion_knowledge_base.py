from __future__ import annotations

import json
import os
import textwrap
from pathlib import Path
from urllib import request


ROOT = Path(__file__).resolve().parents[1]
NOTION_VERSION = "2022-06-28"


PAGES = {
    "Project Home": [
        "Emergency Triage MVP Knowledge Base",
        "Purpose: maintain project-management knowledge, sprint evidence, decisions, stakeholder feedback, and final-delivery references.",
        "Repository: https://github.com/AminHatesProgramming/emergency-triage-mvp",
    ],
    "Sprint Notes": (ROOT / "docs" / "knowledge-base" / "sprint-notes.md").read_text(encoding="utf-8").splitlines(),
    "Meeting Notes": (ROOT / "docs" / "knowledge-base" / "meeting-notes.md").read_text(encoding="utf-8").splitlines(),
    "Technical Decisions": (ROOT / "docs" / "knowledge-base" / "technical-decisions.md").read_text(encoding="utf-8").splitlines(),
    "Stakeholder Feedback Log": (ROOT / "docs" / "knowledge-base" / "stakeholder-feedback-log.md").read_text(encoding="utf-8").splitlines(),
    "Team Playbook": (ROOT / "docs" / "knowledge-base" / "team-playbook.md").read_text(encoding="utf-8").splitlines(),
    "Agile Delivery Evidence": (ROOT / "docs" / "agile-delivery-evidence.md").read_text(encoding="utf-8").splitlines(),
}


def notion_request(method: str, path: str, payload: dict | None = None) -> dict:
    token = os.environ["NOTION_TOKEN"]
    url = f"https://api.notion.com/v1{path}"
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Notion-Version", NOTION_VERSION)
    req.add_header("Content-Type", "application/json")
    with request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def text_block(line: str) -> dict:
    line = line.strip()
    if not line:
        line = " "
    if len(line) > 1800:
        line = line[:1800] + "..."
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": line}}]},
    }


def heading_block(line: str, level: int = 2) -> dict:
    content = line.strip("# ").strip()[:1800] or "Untitled"
    block_type = "heading_1" if level == 1 else "heading_2"
    return {
        "object": "block",
        "type": block_type,
        block_type: {"rich_text": [{"type": "text", "text": {"content": content}}]},
    }


def to_blocks(lines: list[str]) -> list[dict]:
    blocks: list[dict] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# "):
            blocks.append(heading_block(line, 1))
        elif line.startswith("## "):
            blocks.append(heading_block(line, 2))
        elif line.startswith("- "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:][:1800]}}]
                },
            })
        else:
            blocks.append(text_block(line))
    return blocks[:90]


def create_page(parent_page_id: str, title: str, lines: list[str]) -> str:
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": title}}]
            }
        },
        "children": to_blocks(lines),
    }
    created = notion_request("POST", "/pages", payload)
    return created["url"]


def create_task_database(parent_page_id: str) -> str:
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "Emergency Triage MVP - Task Board"}}],
        "properties": {
            "Task": {"title": {}},
            "Owner": {"select": {"options": [
                {"name": "محمدامین", "color": "blue"},
                {"name": "محمدرضا", "color": "green"},
                {"name": "محدثه", "color": "purple"},
            ]}},
            "Sprint": {"select": {"options": [{"name": f"Sprint {i}", "color": "gray"} for i in range(6)]}},
            "Status": {"select": {"options": [
                {"name": "Backlog", "color": "gray"},
                {"name": "To Do", "color": "yellow"},
                {"name": "In Progress", "color": "blue"},
                {"name": "Review", "color": "purple"},
                {"name": "Done", "color": "green"},
            ]}},
            "Story Points": {"number": {"format": "number"}},
            "Deliverable": {"rich_text": {}},
            "Evidence": {"url": {}},
        },
    }
    db = notion_request("POST", "/databases", payload)
    return db["id"], db["url"]


def add_tasks(database_id: str) -> None:
    seed = ROOT / "docs" / "artifacts" / "github-issues-seed.csv"
    import csv
    with seed.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            status = "Done" if row["Status"] == "Done" else "To Do"
            payload = {
                "parent": {"database_id": database_id},
                "properties": {
                    "Task": {"title": [{"type": "text", "text": {"content": row["Title"]}}]},
                    "Owner": {"select": {"name": row["Owner"]}},
                    "Sprint": {"select": {"name": row["Sprint"]}},
                    "Status": {"select": {"name": status}},
                    "Story Points": {"number": int(row["Story Points"])},
                    "Deliverable": {"rich_text": [{"type": "text", "text": {"content": row["Deliverable"]}}]},
                    "Evidence": {"url": f"https://github.com/AminHatesProgramming/emergency-triage-mvp/blob/main/{row['Evidence'].rstrip('/')}"},
                },
            }
            notion_request("POST", "/pages", payload)


def main() -> None:
    if not os.environ.get("NOTION_TOKEN") or not os.environ.get("NOTION_PARENT_PAGE_ID"):
        raise SystemExit(textwrap.dedent("""
        Missing Notion credentials.

        1. Create a Notion integration: https://www.notion.so/my-integrations
        2. Copy its Internal Integration Secret.
        3. Create/open a parent page in Notion and Share it with the integration.
        4. Set:
           $env:NOTION_TOKEN='secret_...'
           $env:NOTION_PARENT_PAGE_ID='page_id_without_dashes_or_with_dashes'
        5. Run this script again.
        """).strip())

    parent = os.environ["NOTION_PARENT_PAGE_ID"]
    urls = {}
    for title, lines in PAGES.items():
        urls[title] = create_page(parent, title, list(lines))

    db_id, db_url = create_task_database(parent)
    add_tasks(db_id)
    urls["Task Board Database"] = db_url

    out = ROOT / "docs" / "artifacts" / "notion-links.json"
    out.write_text(json.dumps(urls, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(urls, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
