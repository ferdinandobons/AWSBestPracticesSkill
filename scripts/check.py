#!/usr/bin/env python3
"""check.py — validator + index generator for AWSBestPracticesSkill.

Pure stdlib. Commands:
  python scripts/check.py                  # coverage + conformance + freshness summary
  python scripts/check.py --check-links    # also validate links (needs network)
  python scripts/check.py --baseline DIR   # diff service/general files vs DIR (staging)
  python scripts/check.py --missing [cat]  # JSON list of catalog entries with no file yet
  python scripts/check.py --stale [cat]    # JSON list of entries due for a REFRESH.md pass
                                            # (missing/unparseable last_reviewed, or older
                                            # than --stale-days; default 180)
  python scripts/check.py --write-index    # regenerate catalog.md and the SKILL.md index
  python scripts/check.py --json           # JSON output

Exit code != 0 when there are errors (CI gate / `/goal` stop condition).
"""
from __future__ import annotations
import argparse
import datetime
import difflib
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"
SERVICES = ROOT / "services"
GENERAL = ROOT / "general"

PILLARS = {
    "Security", "Reliability", "Performance Efficiency",
    "Cost Optimization", "Operational Excellence", "Sustainability",
}
SCENARIOS_H2 = "Common scenarios"
ALLOWED_SERVICE_H2 = {SCENARIOS_H2} | PILLARS
ALLOWED_SOURCE_HOSTS = ("docs.aws.amazon.com", "aws.amazon.com", "wa.aws.amazon.com")

URL_RE = re.compile(r"\]\((https?://[^)]+)\)")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
H2_LINE_RE = re.compile(r"^##\s+(.+?)\s*$")
H2_FIND_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
BULLET_RE = re.compile(r"^\s*[-*]\s+\S")
LAST_REVIEWED_RE = re.compile(r"last_reviewed=(\d{4}-\d{2}-\d{2})")
DEFAULT_STALE_DAYS = 180


class Report:
    def __init__(self):
        self.errors, self.warnings, self.info = [], [], []
    def err(self, m): self.errors.append(m)
    def warn(self, m): self.warnings.append(m)
    def note(self, m): self.info.append(m)
    def ok(self): return not self.errors


def load_catalog() -> dict:
    if not CATALOG.exists():
        sys.exit(f"catalog.json not found at {CATALOG}")
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def iter_entries(cat: dict):
    for ckey, c in cat.get("categories", {}).items():
        for s in c.get("services", []):
            yield ckey, s


def strip_emoji_h2(h2: str) -> str:
    return re.sub(r"^[^0-9A-Za-z]+", "", h2).strip()


def check_coverage(cat: dict, rep: Report, strict: bool):
    declared = set()
    for _, s in iter_entries(cat):
        declared.add(s["path"])
        if not (ROOT / s["path"]).exists():
            # missing content is a hard error only under --strict (release/coverage gate);
            # by default it's a warning so per-push CI stays green while content is filled in.
            (rep.err if strict else rep.warn)(
                f"[coverage] missing file for {s['name']}: {s['path']}")
    on_disk = set()
    for base in (SERVICES, GENERAL):
        if base.exists():
            on_disk |= {str(p.relative_to(ROOT)) for p in base.rglob("*.md")}
    for orphan in sorted(on_disk - declared):
        rep.warn(f"[coverage] file not in catalog: {orphan}")


def check_conformance(path: Path, is_general: bool, rep: Report):
    text = path.read_text(encoding="utf-8")
    name = path.name
    if not H1_RE.search(text):
        rep.err(f"[conformance] {name}: missing H1 title")
    h2s = [strip_emoji_h2(h) for h in H2_FIND_RE.findall(text)]
    if not h2s:
        rep.err(f"[conformance] {name}: no H2 section")
    if not is_general:
        if SCENARIOS_H2 not in h2s:
            rep.warn(f"[conformance] {name}: missing '## {SCENARIOS_H2}' section")
        if not (set(h2s) & PILLARS):
            rep.err(f"[conformance] {name}: no valid Well-Architected pillar section")
        for h in h2s:
            if h not in ALLOWED_SERVICE_H2:
                rep.warn(f"[conformance] {name}: disallowed section '{h}'")
    # every practice bullet must carry a source link
    current = None
    for line in text.splitlines():
        m = H2_LINE_RE.match(line)
        if m:
            current = strip_emoji_h2(m.group(1))
            continue
        if current is None or current == SCENARIOS_H2:
            continue
        practice = True if is_general else (current in PILLARS)
        if practice and BULLET_RE.match(line) and "](http" not in line:
            rep.warn(f"[conformance] {name}: bullet without source -> {line.strip()[:70]}")


def collect_urls(cat: dict) -> dict:
    urls = {}
    for _, s in iter_entries(cat):
        p = ROOT / s["path"]
        if p.exists():
            urls[s["path"]] = URL_RE.findall(p.read_text(encoding="utf-8"))
    return urls


def check_links(cat: dict, rep: Report):
    seen = {u for lst in collect_urls(cat).values() for u in lst}
    for u in sorted(seen):
        host = re.sub(r"^https?://([^/]+).*", r"\1", u)
        if not any(host == h or host.endswith("." + h) for h in ALLOWED_SOURCE_HOSTS):
            rep.warn(f"[links] non-official source host: {u}")

    def probe(u):
        req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": "awsbp-check"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return u, r.status
        except urllib.error.HTTPError as e:
            return u, e.code
        except Exception as e:  # noqa: BLE001
            return u, str(e)

    with ThreadPoolExecutor(max_workers=8) as ex:
        for u, status in ex.map(probe, sorted(seen)):
            if status != 200:
                rep.warn(f"[links] {status} -> {u}")
    rep.note(f"[links] checked {len(seen)} URLs")


def diff_baseline(cat: dict, baseline: str, rep: Report):
    base = Path(baseline)
    for _, s in iter_entries(cat):
        cur, old = ROOT / s["path"], base / s["path"]
        if not cur.exists():
            continue
        if not old.exists():
            rep.note(f"[diff] new: {s['path']}")
            continue
        a = old.read_text(encoding="utf-8").splitlines(keepends=True)
        b = cur.read_text(encoding="utf-8").splitlines(keepends=True)
        d = list(difflib.unified_diff(a, b, fromfile=f"baseline/{s['path']}", tofile=s["path"]))
        if d:
            added = sum(1 for l in d if l.startswith("+") and not l.startswith("+++"))
            removed = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
            rep.note(f"[diff] {s['path']}: +{added} -{removed}")
            sys.stdout.writelines(d)


def render_index(cat: dict) -> str:
    out = []
    for ckey, c in cat.get("categories", {}).items():
        out.append(f"### {c.get('title', ckey)}\n")
        for s in sorted(c.get("services", []), key=lambda x: x["name"]):
            out.append(f"- [{s['name']}]({s['path']})\n")
        out.append("\n")
    return "".join(out)


def write_index(cat: dict, rep: Report):
    body = render_index(cat)
    header = f"# Service catalog\n\nGenerated by scripts/check.py — {cat.get('generated', '')}\n\n"
    (ROOT / "catalog.md").write_text(header + body, encoding="utf-8")
    rep.note("[index] catalog.md regenerated")
    skill = ROOT / "SKILL.md"
    if skill.exists():
        txt = skill.read_text(encoding="utf-8")
        new = re.sub(r"(<!-- BEGIN:INDEX.*?-->).*?(<!-- END:INDEX -->)",
                     lambda m: f"{m.group(1)}\n{body}{m.group(2)}", txt, flags=re.S)
        if new != txt:
            skill.write_text(new, encoding="utf-8")
            rep.note("[index] SKILL.md index updated")


def list_missing(cat: dict, scope):
    out = []
    for ckey, s in iter_entries(cat):
        if scope and ckey != scope:
            continue
        if not (ROOT / s["path"]).exists():
            out.append({"name": s["name"], "slug": s["slug"], "path": s["path"],
                        "abspath": str(ROOT / s["path"]),
                        "type": s.get("type", "service"), "category": ckey})
    return out


def last_reviewed(path: Path) -> datetime.date | None:
    m = LAST_REVIEWED_RE.search(path.read_text(encoding="utf-8"))
    if not m:
        return None
    try:
        return datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def list_stale(cat: dict, scope, max_age_days: int):
    """Entries whose file exists but is due for a REFRESH.md pass: either the
    trailing `<!-- meta: last_reviewed=... -->` line is missing/unparseable, or
    its date is older than max_age_days. Missing files are NOT included here —
    those are `--missing`'s job (generate first, then refresh)."""
    today = datetime.date.today()
    out = []
    for ckey, s in iter_entries(cat):
        if scope and ckey != scope:
            continue
        p = ROOT / s["path"]
        if not p.exists():
            continue
        lr = last_reviewed(p)
        age_days = (today - lr).days if lr else None
        if lr is None or age_days > max_age_days:
            out.append({"name": s["name"], "slug": s["slug"], "path": s["path"],
                        "abspath": str(p), "type": s.get("type", "service"),
                        "category": ckey,
                        "last_reviewed": lr.isoformat() if lr else None,
                        "age_days": age_days})
    out.sort(key=lambda e: (e["age_days"] is not None, e["age_days"] or 0), reverse=True)
    return out


def check_freshness(cat: dict, rep: Report, max_age_days: int):
    stale = list_stale(cat, None, max_age_days)
    total = sum(1 for _, s in iter_entries(cat) if (ROOT / s["path"]).exists())
    if stale:
        rep.note(f"[freshness] {len(stale)}/{total} files due for review "
                 f"(missing or >{max_age_days}d old last_reviewed) — see --stale")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scope", nargs="?", help="optional category to scope --missing/--stale")
    ap.add_argument("--missing", action="store_true", help="print missing entries as JSON and exit")
    ap.add_argument("--stale", action="store_true",
                     help="print entries due for a REFRESH.md pass as JSON and exit")
    ap.add_argument("--stale-days", type=int, default=DEFAULT_STALE_DAYS,
                     help=f"freshness threshold in days for --stale (default {DEFAULT_STALE_DAYS})")
    ap.add_argument("--strict", action="store_true", help="treat missing files as errors (release/coverage gate)")
    ap.add_argument("--check-links", action="store_true")
    ap.add_argument("--baseline")
    ap.add_argument("--write-index", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    cat = load_catalog()
    if args.missing:
        print(json.dumps(list_missing(cat, args.scope), ensure_ascii=False, indent=2))
        sys.exit(0)
    if args.stale:
        print(json.dumps(list_stale(cat, args.scope, args.stale_days), ensure_ascii=False, indent=2))
        sys.exit(0)
    rep = Report()
    if args.write_index:
        write_index(cat, rep)
    check_coverage(cat, rep, args.strict)
    for _, s in iter_entries(cat):
        p = ROOT / s["path"]
        if p.exists():
            check_conformance(p, s.get("type") == "general", rep)
    check_freshness(cat, rep, args.stale_days)
    if args.check_links:
        check_links(cat, rep)
    if args.baseline:
        diff_baseline(cat, args.baseline, rep)

    if args.json:
        print(json.dumps({"errors": rep.errors, "warnings": rep.warnings, "info": rep.info},
                         ensure_ascii=False, indent=2))
    else:
        for m in rep.info: print("·  " + m)
        for m in rep.warnings: print("⚠  " + m)
        for m in rep.errors: print("✗  " + m)
        print(f"\n{len(rep.errors)} errors, {len(rep.warnings)} warnings.")
    sys.exit(0 if rep.ok() else 1)


if __name__ == "__main__":
    main()
