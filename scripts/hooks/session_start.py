#!/usr/bin/env python3
"""SessionStart hook: back up the literature CSV once per session and put a
one-line knowledge-base status into Claude's context. Never fails the session."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EIDB = ROOT / "scripts" / "eidb.py"


def run(*args: str) -> str:
    try:
        r = subprocess.run([sys.executable, str(EIDB), *args], capture_output=True, text=True, timeout=60)
        return (r.stdout + r.stderr).strip()
    except Exception as e:  # never block the session
        return f"eidb {args[0]} failed: {e}"


def main() -> None:
    try:
        source = json.load(sys.stdin).get("source", "startup")
    except Exception:
        source = "startup"
    lines = [run("backup", "--reason", f"session-{source}"), run("status")]
    print("\n".join(line for line in lines if line))


if __name__ == "__main__":
    main()
    sys.exit(0)
