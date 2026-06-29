# Maintaining AWSBestPracticesSkill

This skill contains **only AWS best practices**. Every update must preserve that
constraint: no service descriptions, pricing, or tutorials — only best
practices, each with an official AWS source link.

`catalog.json` is the source of truth. `scripts/check.py` is the gate.

## 1. When to update (triggers)
- **Periodic**: full review every 3–6 months.
- **New AWS service**: when AWS announces / GAs a new service.
- **Changed guidance**: AWS updates Well-Architented or a service's
  "best practices" / "security" pages.
- **Broken links**: reported by `scripts/check.py --check-links`.
- **Freshness**: files whose `last_reviewed` is older than 180 days.

## 2. Research procedure (regenerating content)
Run inside a Claude Code or Codex session with the AWS MCP tools connected.

### 2.1 Refresh the service catalog
1. Get the authoritative service list: AWS Pricing MCP `get_pricing_service_codes`.
2. Diff against `catalog.json`:
   ```bash
   # dump AWS service codes, one per line, to /tmp/aws_codes.txt first
   python scripts/check.py --aws-codes /tmp/aws_codes.txt
   ```
   It flags **new** services (in AWS, not in the catalog) and **disappeared** ones.
3. Add missing entries to `catalog.json` (category, slug, path, aws_service_code,
   `type: "service"` or `"general"`).

### 2.2 Extract best practices from official sources (per service)
For each service, with the **AWS Knowledge MCP**:
1. `search_documentation` with queries like `"<service> best practices"`,
   `"<service> security best practices"`, `"<service> Well-Architected"`.
2. `read_documentation` on the relevant pages (best practices, security,
   resilience, cost optimization, operational guidance).
3. Extract **only best practices**. For each: imperative action,
   `[when-it-applies]` tag, short rationale, source URL.
4. Drop anything that is a description / price / tutorial.

### 2.3 Write the file from the template
1. Start from `_TEMPLATE.md`.
2. Fill `## Common scenarios` (2–4 use cases → pillars) and the pillars that have
   real practices. (For `general/` docs, sections may be topic-based.)
3. Update the `<!-- meta: last_reviewed=... -->` footer and the
   `last_reviewed` / `sources` / `pillars` fields in `catalog.json`.

### 2.4 At scale — the `/goal` command (autonomous loop)
For many services at once, run **`/goal`** (see `.claude/commands/goal.md`). It is
a Codex-style goal loop ("Ralph loop"): **work → check → continue or complete**.
Each iteration it reads the remaining work-list (`scripts/goal_worklist.py`),
generates a batch of files in **parallel** (one subagent per service, each
researching via the AWS Knowledge MCP and writing from the template), validates
with `check.py`, updates `catalog.json` (`scripts/goal_apply.py`), commits, and
keeps going until `check.py` reports full coverage. On Claude Code you can wrap it
with `/loop /goal` to self-pace across turns; on Codex, feed the GOAL block to the
native `/goal` command.

Variants:
- `/goal --all` — every missing service/general doc.
- `/goal <category>` — only one category (e.g. `/goal database`).
- `/goal --stale` — also regenerate docs past the freshness threshold.

## 3. Adding a new service
1. Add the entry to `catalog.json`.
2. Create `services/<category>/<slug>.md` from `_TEMPLATE.md`.
3. Run the research (§2.2–2.3) — or `/goal <category>`.
4. Regenerate indexes: `python scripts/check.py --write-index`.
5. Validate: `python scripts/check.py`.

## 4. Updating an existing doc (diff/review flow)
1. Regenerate content into a staging folder, e.g. `_staging/services/...`.
2. Diff against the committed version:
   ```bash
   python scripts/check.py --baseline _staging
   ```
   It prints per-file diffs (practices added/removed).
3. Review the diff, replace the files, bump `last_reviewed`.
4. Validate and commit.

## 5. Validation before commit (gate)
```bash
python scripts/check.py                 # coverage + conformance + freshness
python scripts/check.py --check-links   # validate links (network)
```
Everything green **before** bumping the version.

## 6. Versioning & release
- Bump `version` in `catalog.json` + add a `CHANGELOG.md` entry.
- Sync `README.md` (service count, structure, commands).
- Annotated tag `vX.Y.Z` **only** when the work is stable and checks are green.
- Never force-push an already-released tag — ship a follow-up patch instead.

## 7. CI
`.github/workflows/check.yml` runs `python scripts/check.py` on every push/PR.
