#!/usr/bin/env python3
"""cost.py: token-ledger utility for AWSBestPracticesSkill.

A utility called after each GENERATE.md/REFRESH.md batch; it holds no
orchestration logic. Extracts nothing itself: you pass the workflow run's
`subagent_tokens` / `agent_count`; it stores them and re-renders the cost view.

Commands:
  python scripts/cost.py add --name NAME --tokens N --agents N --files N
  python scripts/cost.py render

Reads/writes docs/build-cost.json, regenerates docs/build-cost.md and the
<!-- BUILD-COST --> block in README.md.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "docs" / "build-cost.json"
MD = ROOT / "docs" / "build-cost.md"
README = ROOT / "README.md"


def load() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    return {"note": "Token usage extracted from GENERATE.md generation runs (subagent_tokens).",
            "phases": []}


def human(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def render(L: dict):
    ph = L["phases"]
    tt = sum(p["tokens"] for p in ph)
    ta = sum(p["agents"] for p in ph)
    tf = sum(p.get("files", 0) for p in ph)
    md = ["# Build cost (token usage)\n\n",
          "Tokens are extracted from each `GENERATE.md` generation run (`subagent_tokens`)\n",
          "and accumulated here: generation agents only (research + write + verify).\n\n",
          "| Phase | Files | Agents | Tokens |\n|---|--:|--:|--:|\n"]
    for p in ph:
        md.append(f"| {p['name']} | {p.get('files', 0)} | {p['agents']} | {p['tokens']:,} |\n")
    md.append(f"| **Total** | **{tf}** | **{ta}** | **{tt:,} (~{human(tt)})** |\n")
    MD.write_text("".join(md), encoding="utf-8")

    line = (f"**Generation cost so far: ~{human(tt)} tokens** ({tt:,}) across {ta} "
            f"workflow agents · {tf} files. See [`docs/build-cost.md`](docs/build-cost.md) "
            f"for the per-phase breakdown.")
    r = README.read_text(encoding="utf-8")
    r = re.sub(r"(<!-- BUILD-COST -->).*?(<!-- /BUILD-COST -->)",
               lambda m: f"{m.group(1)}\n{line}\n{m.group(2)}", r, flags=re.S)
    README.write_text(r, encoding="utf-8")
    return tt, ta, tf


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--name", required=True)
    a.add_argument("--tokens", type=int, required=True)
    a.add_argument("--agents", type=int, required=True)
    a.add_argument("--files", type=int, default=0)
    sub.add_parser("render")
    args = ap.parse_args()

    L = load()
    if args.cmd == "add":
        L["phases"].append({"name": args.name, "agents": args.agents,
                            "tokens": args.tokens, "files": args.files})
        LEDGER.write_text(json.dumps(L, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tt, ta, tf = render(L)
    print(f"total: {tt:,} tokens (~{human(tt)}), {ta} agents, {tf} files")


if __name__ == "__main__":
    main()
