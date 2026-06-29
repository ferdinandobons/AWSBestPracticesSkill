#!/usr/bin/env python3
"""goal_apply.py — apply `goal` Workflow results to catalog.json.

Reads a JSON file containing either the workflow return object
({"results": [...]}) or a bare array of result objects. For every result with
status == "written", updates the matching catalog entry's last_reviewed (today),
pillars, and sources.

Usage:
  python3 scripts/goal_apply.py <results.json>
"""
from __future__ import annotations
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"


def main(argv):
    if not argv:
        sys.exit("usage: goal_apply.py <results.json>")
    data = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    results = data.get("results", data) if isinstance(data, dict) else data

    by_path = {}
    by_slug = {}
    for r in results:
        if not isinstance(r, dict) or r.get("status") != "written":
            continue
        if r.get("path"):
            by_path[r["path"]] = r
        if r.get("slug"):
            by_slug[r["slug"]] = r

    today = datetime.date.today().isoformat()
    cat = json.loads(CATALOG.read_text(encoding="utf-8"))
    updated = 0
    for c in cat.get("categories", {}).values():
        for s in c.get("services", []):
            r = by_path.get(s["path"]) or by_slug.get(s.get("slug"))
            if not r:
                continue
            s["last_reviewed"] = today
            if isinstance(r.get("pillars"), list):
                s["pillars"] = r["pillars"]
            if isinstance(r.get("sources"), int):
                s["sources"] = r["sources"]
            updated += 1

    CATALOG.write_text(
        json.dumps(cat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"catalog.json: updated {updated} entries")


if __name__ == "__main__":
    main(sys.argv[1:])
