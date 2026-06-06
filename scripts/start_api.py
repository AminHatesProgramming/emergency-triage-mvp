from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

stdout = (LOG_DIR / "api.out.log").open("ab")
stderr = (LOG_DIR / "api.err.log").open("ab")

creationflags = 0
if sys.platform.startswith("win"):
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

process = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
        "--log-level",
        "info",
    ],
    cwd=ROOT,
    stdout=stdout,
    stderr=stderr,
    stdin=subprocess.DEVNULL,
    creationflags=creationflags,
    close_fds=True,
)

print(process.pid)
