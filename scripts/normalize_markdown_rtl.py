from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPEN = "<!-- rtl-normalized -->\n<div dir=\"rtl\" align=\"right\">\n\n"
CLOSE = "\n</div>\n"
SKIP_DIRS = {".git", "dist", ".agents", "__pycache__"}
TABLE_LINE = re.compile(r"^\s*\|.*\|\s*$")
LIST_LINE = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+)")


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def tighten_generated_spacing(text: str) -> str:
    lines = text.split("\n")
    output: list[str] = []
    for index, line in enumerate(lines):
        if line == "":
            previous = next((item for item in reversed(output) if item.strip()), "")
            following = next((item for item in lines[index + 1 :] if item.strip()), "")
            if (
                TABLE_LINE.match(previous)
                and TABLE_LINE.match(following)
                or LIST_LINE.match(previous)
                and LIST_LINE.match(following)
            ):
                continue
        output.append(line)
    return "\n".join(output)


def normalize(path: Path) -> bool:
    original_bytes = path.read_bytes()
    original_text = original_bytes.decode("utf-8-sig")
    text = original_text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = tighten_generated_spacing(text)
    changed = text != original_text
    if not text.startswith("<!-- rtl-normalized -->"):
        text = OPEN + text.rstrip() + "\n" + CLOSE
        changed = True

    if original_bytes.startswith(b"\xef\xbb\xbf"):
        changed = True

    if changed:
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    return changed


def main() -> None:
    changed: list[str] = []
    for path in sorted(ROOT.rglob("*.md")):
        if should_skip(path.relative_to(ROOT)):
            continue
        if normalize(path):
            changed.append(str(path.relative_to(ROOT)))

    print(f"Normalized {len(changed)} markdown files for RTL preview.")
    for item in changed:
        print(item)


if __name__ == "__main__":
    main()
