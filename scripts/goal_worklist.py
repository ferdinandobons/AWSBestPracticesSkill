#!/usr/bin/env python3
"""goal_worklist.py — build the args JSON for the `goal` Workflow.

Reads catalog.json, selects pending entries (missing file; with --stale also
files older than the freshness threshold), optionally filters to one category,
groups by category, and prints the Workflow args JSON to stdout.

Usage:
  python3 scripts/goal_worklist.py [--all | --stale | <category>] [--max-age-days N]
"""
from __future__ import annotations
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"
CHILD = ROOT / ".claude" / "workflows" / "goal-category.js"


def main(argv):
    stale = False
    category = None
    max_age = 180
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--all", ""):
            pass
        elif a == "--stale":
            stale = True
        elif a == "--max-age-days":
            i += 1
            max_age = int(argv[i])
        elif a.startswith("--"):
            pass  # ignore unknown flags
        else:
            category = a
        i += 1

    cat = json.loads(CATALOG.read_text(encoding="utf-8"))
    today = datetime.date.today()
    groups = []

    for ckey, c in cat.get("categories", {}).items():
        if category and ckey != category:
            continue
        pending = []
        for s in c.get("services", []):
            path = ROOT / s["path"]
            missing = not path.exists()
            is_stale = False
            if stale and not missing:
                lr = s.get("last_reviewed")
                if not lr:
                    is_stale = True
                else:
                    age = (today - datetime.date.fromisoformat(lr)).days
                    is_stale = age > max_age
            if missing or is_stale:
                pending.append({
                    "name": s["name"],
                    "slug": s["slug"],
                    "path": s["path"],
                    "abspath": str(ROOT / s["path"]),
                    "type": s.get("type", "service"),
                    "aws_service_code": s.get("aws_service_code"),
                })
        if pending:
            groups.append({
                "category": ckey,
                "title": c.get("title", ckey),
                "services": pending,
            })

    out = {"childScriptPath": str(CHILD), "categories": groups}
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
