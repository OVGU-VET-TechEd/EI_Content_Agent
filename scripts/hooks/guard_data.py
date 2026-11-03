#!/usr/bin/env python3
"""PreToolUse hook (Write|Edit|MultiEdit|NotebookEdit): block direct edits of the
literature CSV and of anything in its backups folder. The CSV must be written
only through scripts/eidb.py so that APA/BibTeX, ids and validation stay consistent.
Exit 2 blocks the tool call and shows stderr to Claude."""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def data_dir() -> Path | None:
    if os.environ.get("EI_DATA_DIR"):
        return Path(os.environ["EI_DATA_DIR"]).expanduser().resolve()
    cfg = Path(os.environ.get("EI_CONFIG", ROOT / "ei.config.json"))
    try:
        return Path(json.loads(cfg.read_text("utf-8"))["data_dir"]).expanduser().resolve()
    except Exception:
        return (ROOT / "data").resolve()


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = payload.get("tool_input") or {}
    raw = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not raw:
        return 0
    path = Path(raw).expanduser().resolve()
    name = path.name
    dd = data_dir()
    in_backups = dd is not None and (dd / "backups") in path.parents
    is_db = name.startswith("ei_literature") and name.endswith((".csv", ".csv.tmp"))
    if is_db or in_backups:
        print(
            f"Blocked: {name} is the EI literature database (or a backup). Do not edit it directly. "
            "Use `python3 scripts/eidb.py add | update | rename | restore` instead.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
