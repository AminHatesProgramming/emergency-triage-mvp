from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
DIST = ROOT / "dist"


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    copy_file(FRONTEND / "index.html", DIST / "index.html")
    copy_file(FRONTEND / "manifest.webmanifest", DIST / "manifest.webmanifest")
    copy_file(FRONTEND / "sw.js", DIST / "sw.js")

    static_dir = DIST / "static"
    copy_file(FRONTEND / "app.js", static_dir / "app.js")
    copy_file(FRONTEND / "styles.css", static_dir / "styles.css")
    copy_file(FRONTEND / "privacy.html", static_dir / "privacy.html")
    copy_file(FRONTEND / "model-v7.json", static_dir / "model-v7.json")
    shutil.copytree(FRONTEND / "assets", static_dir / "assets")

    copy_file(ROOT / "README.md", DIST / "README.md")
    print(f"Built GitHub Pages app in {DIST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
