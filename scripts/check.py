#!/usr/bin/env python3
"""check.py — validator and diff-checker for AWSBestPracticesSkill.

Pure stdlib (Python 3.8+). Commands:
  python scripts/check.py                  # coverage + conformance + freshness
  python scripts/check.py --check-links    # also validate links (needs network)
  python scripts/check.py --baseline DIR   # diff service/general files vs DIR (staging)
  python scripts/check.py --aws-codes F    # compare catalog vs AWS service codes (one/line)
  python scripts/check.py --write-index    # regenerate catalog.md and the index in SKILL.md
  python scripts/check.py --max-age-days N # freshness threshold (default 180)
  python scripts/check.py --json           # JSON output

Exit code != 0 when there are errors (CI gate).
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
    "Security",
    "Reliability",
    "Performance Efficiency",
    "Cost Optimization",
    "Operational Excellence",
    "Sustainability",
}
SCENARIOS_H2 = "Common scenarios"
ALLOWED_SERVICE_H2 = {SCENARIOS_H2} | PILLARS

URL_RE = re.compile(r"\]\((https?://[^)]+)\)")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
H2_LINE_RE = re.compile(r"^##\s+(.+?)\s*$")
H2_FIND_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
BULLET_RE = re.compile(r"^\s*[-*]\s+\S")

ALLOWED_SOURCE_HOSTS = (
    "docs.aws.amazon.com",
    "aws.amazon.com",
    "wa.aws.amazon.com",
)


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def err(self, m):
        self.errors.append(m)

    def warn(self, m):
        self.warnings.append(m)

    def note(self, m):
        self.info.append(m)

    def ok(self):
        return not self.errors


def load_catalog() -> dict:
    if not CATALOG.exists():
        sys.exit(f"catalog.json not found at {CATALOG}")
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def iter_entries(cat: dict):
    """Yield (category_key, service_dict) for every catalog entry."""
    for ckey, c in cat.get("categories", {}).items():
        for s in c.get("services", []):
            yield ckey, s


def entry_type(s: dict) -> str:
    return s.get("type", "service")


def strip_emoji_h2(h2: str) -> str:
    """'🔒 Security' -> 'Security'."""
    return re.sub(r"^[^0-9A-Za-z]+", "", h2).strip()


def check_coverage(cat: dict, rep: Report):
    declared = set()
    for _, s in iter_entries(cat):
        declared.add(s["path"])
        if not (ROOT / s["path"]).exists():
            rep.err(f"[coverage] missing file for {s['name']}: {s['path']}")
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
                rep.warn(
                    f"[conformance] {name}: disallowed section '{h}' "
                    f"(possible non-best-practice content)"
                )

    # Source requirement: every bullet inside a 'practice' section must carry a link.
    current = None
    for line in text.splitlines():
        m = H2_LINE_RE.match(line)
        if m:
            current = strip_emoji_h2(m.group(1))
            continue
        if current is None or current == SCENARIOS_H2:
            continue
        if is_general:
            practice_section = True  # all non-scenario sections are practices
        else:
            practice_section = current in PILLARS
        if practice_section and BULLET_RE.match(line) and "](http" not in line:
            rep.warn(
                f"[conformance] {name}: bullet without source -> {line.strip()[:70]}"
            )


def check_freshness(cat: dict, max_age: int, rep: Report):
    today = datetime.date.today()
    for _, s in iter_entries(cat):
        lr = s.get("last_reviewed")
        if not lr:
            rep.warn(f"[freshness] {s['name']}: missing last_reviewed")
            continue
        age = (today - datetime.date.fromisoformat(lr)).days
        if age > max_age:
            rep.warn(
                f"[freshness] {s['name']}: {age}d since last review (>{max_age})"
            )


def collect_urls(cat: dict) -> dict:
    urls = {}
    for _, s in iter_entries(cat):
        p = ROOT / s["path"]
        if p.exists():
            urls[s["path"]] = URL_RE.findall(p.read_text(encoding="utf-8"))
    return urls


def check_links(cat: dict, rep: Report):
    by_file = collect_urls(cat)
    seen = {u for lst in by_file.values() for u in lst}
    for u in sorted(seen):
        host = re.sub(r"^https?://([^/]+).*", r"\1", u)
        if not any(host == h or host.endswith("." + h) for h in ALLOWED_SOURCE_HOSTS):
            rep.warn(f"[links] non-official source host: {u}")

    def probe(u):
        req = urllib.request.Request(
            u, method="HEAD", headers={"User-Agent": "awsbp-check"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return u, r.status
        except urllib.error.HTTPError as e:
            return u, e.code
        except Exception as e:  # noqa: BLE001 - report any failure as a warning
            return u, str(e)

    with ThreadPoolExecutor(max_workers=8) as ex:
        for u, status in ex.map(probe, sorted(seen)):
            if status != 200:
                rep.warn(f"[links] {status} -> {u}")
    rep.note(f"[links] checked {len(seen)} URLs")


def compare_aws_codes(cat: dict, codes_file: str, rep: Report):
    aws = {l.strip() for l in Path(codes_file).read_text().splitlines() if l.strip()}
    have = {
        s.get("aws_service_code")
        for _, s in iter_entries(cat)
        if s.get("aws_service_code")
    }
    for new in sorted(aws - have):
        rep.note(f"[aws] AWS service not yet covered: {new}")
    for gone in sorted(have - aws):
        rep.warn(f"[aws] in catalog but absent from AWS list: {gone}")


def diff_baseline(cat: dict, baseline: str, rep: Report):
    base = Path(baseline)
    for _, s in iter_entries(cat):
        cur = ROOT / s["path"]
        old = base / s["path"]
        if not cur.exists():
            continue
        if not old.exists():
            rep.note(f"[diff] new: {s['path']}")
            continue
        a = old.read_text(encoding="utf-8").splitlines(keepends=True)
        b = cur.read_text(encoding="utf-8").splitlines(keepends=True)
        d = list(
            difflib.unified_diff(
                a, b, fromfile=f"baseline/{s['path']}", tofile=s["path"]
            )
        )
        if d:
            added = sum(1 for l in d if l.startswith("+") and not l.startswith("+++"))
            removed = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
            rep.note(f"[diff] {s['path']}: +{added} -{removed}")
            sys.stdout.writelines(d)


def render_index(cat: dict) -> str:
    lines = []
    for ckey, c in cat.get("categories", {}).items():
        lines.append(f"### {c.get('title', ckey)}\n")
        for s in sorted(c.get("services", []), key=lambda x: x["name"]):
            lines.append(f"- [{s['name']}]({s['path']})\n")
        lines.append("\n")
    return "".join(lines)


def write_index(cat: dict, rep: Report):
    body = render_index(cat)
    header = (
        "# Service catalog\n\n"
        f"Generated by scripts/check.py — {cat.get('generated', '')}\n\n"
    )
    (ROOT / "catalog.md").write_text(header + body, encoding="utf-8")
    rep.note("[index] catalog.md regenerated")
    skill = ROOT / "SKILL.md"
    if skill.exists():
        txt = skill.read_text(encoding="utf-8")
        new = re.sub(
            r"(<!-- BEGIN:INDEX.*?-->).*?(<!-- END:INDEX -->)",
            lambda m: f"{m.group(1)}\n{body}{m.group(2)}",
            txt,
            flags=re.S,
        )
        if new != txt:
            skill.write_text(new, encoding="utf-8")
            rep.note("[index] SKILL.md index updated")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-links", action="store_true")
    ap.add_argument("--baseline")
    ap.add_argument("--aws-codes")
    ap.add_argument("--write-index", action="store_true")
    ap.add_argument("--max-age-days", type=int, default=180)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    cat = load_catalog()
    rep = Report()

    if args.write_index:
        write_index(cat, rep)

    check_coverage(cat, rep)
    for _, s in iter_entries(cat):
        p = ROOT / s["path"]
        if p.exists():
            check_conformance(p, entry_type(s) == "general", rep)
    check_freshness(cat, args.max_age_days, rep)
    if args.check_links:
        check_links(cat, rep)
    if args.aws_codes:
        compare_aws_codes(cat, args.aws_codes, rep)
    if args.baseline:
        diff_baseline(cat, args.baseline, rep)

    if args.json:
        print(
            json.dumps(
                {"errors": rep.errors, "warnings": rep.warnings, "info": rep.info},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for m in rep.info:
            print("·  " + m)
        for m in rep.warnings:
            print("⚠  " + m)
        for m in rep.errors:
            print("✗  " + m)
        print(f"\n{len(rep.errors)} errors, {len(rep.warnings)} warnings.")
    sys.exit(0 if rep.ok() else 1)


if __name__ == "__main__":
    main()
