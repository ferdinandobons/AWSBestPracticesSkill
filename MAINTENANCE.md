# Maintaining AWSBestPracticesSkill

Only AWS best practices, each with an official AWS source link: no service
descriptions, pricing, or tutorials. `catalog.json` is the source of truth;
`scripts/check.py` is the gate.

## Generate missing content
Paste [`GENERATE.md`](GENERATE.md) into a chat with your coding agent (Claude
Code, Codex CLI, or similar) in this repo. It generates a best-practices file
for every `catalog.json` entry still missing one, by researching the official
AWS docs and writing each file, until `python3 scripts/check.py` passes. Limit
the scope by adding a `Scope: <category>` line above the pasted instructions.

## Keep the catalog current (new services + stale content)
Paste [`REFRESH.md`](REFRESH.md) into the same kind of chat. It's the sibling
of `GENERATE.md`: instead of filling gaps, it (1) diffs `catalog.json` against
AWS's current service list to add new services, rename/recategorize changed
ones, and drop fully-retired ones, then (2) re-reviews existing files flagged
by `python3 scripts/check.py --stale` (missing or >180-day-old `last_reviewed`)
against current official docs, updating content and bumping `last_reviewed`.

Run it:
- **Periodically**: every 3–6 months.
- **When you notice a new AWS service** that isn't in the catalog yet.
- **When `check.py --stale` reports entries** (it always runs as part of the
  default `check.py`, as a non-blocking summary line).
- **When `check.py --check-links` reports broken links.**

## Add a new service manually
1. Add an entry to `catalog.json` (`name`, `slug`, `path`, `type`, `aws_service_code`).
2. Paste [`GENERATE.md`](GENERATE.md) (with `Scope: <category>`) to generate it.
3. `python3 scripts/check.py --write-index` to refresh `catalog.md` and the SKILL.md index.

(`REFRESH.md` does steps 1–2 for you, across the whole catalog, by discovering
what's missing instead of you spotting it manually.)

## Update an existing doc (diff/review)
1. Regenerate into a staging folder, e.g. `_staging/services/...`.
2. `python3 scripts/check.py --baseline _staging` to see what changed.
3. Replace, validate, commit.

(`REFRESH.md` does this in place, targeted at whatever `--stale` flags, rather
than a full staging-folder regeneration.)

## Validate before commit (gate)
```bash
python3 scripts/check.py                 # per-push: conformance + freshness summary (missing = warning)
python3 scripts/check.py --strict        # release gate: every catalog entry must have a file
python3 scripts/check.py --check-links    # validate links (network)
python3 scripts/check.py --stale          # list entries due for a REFRESH.md pass
```
CI runs the non-strict `check.py` on every push/PR (`.github/workflows/check.yml`),
so the badge stays green while content is being filled in. Run `--strict` (full
coverage) before tagging a release.

## Scripts (utilities only)
The loop logic lives in `GENERATE.md` and `REFRESH.md`. The scripts are just
utilities the loops call:
- `scripts/check.py`: validate (coverage/conformance/links/freshness),
  `--missing [category]` to list entries still to generate, `--stale
  [category] [--stale-days N]` to list entries due for a `REFRESH.md` pass,
  `--write-index` to regenerate the indexes, `--baseline DIR` to diff a
  regeneration.
- `scripts/cost.py`: token ledger. `add --name --tokens --agents --files` records a
  workflow run's `subagent_tokens` and re-renders the cost section of the README and
  `docs/build-cost.md`; `render` re-renders from the ledger.

## Release
Bump `version` in `catalog.json`, add a `CHANGELOG.md` entry, sync `README.md`,
tag `vX.Y.Z` only when stable. Never force-push a released tag.
