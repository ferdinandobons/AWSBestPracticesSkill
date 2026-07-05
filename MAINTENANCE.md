# Maintaining AWSBestPracticesSkill

Only AWS best practices, each with an official AWS source link — no service
descriptions, pricing, or tutorials. `catalog.json` is the source of truth;
`scripts/check.py` is the gate.

## Generate / regenerate content
Paste [`GENERATE.md`](GENERATE.md) into a chat with your coding agent (Claude
Code, Codex CLI, or similar) in this repo. It generates a best-practices file
for every `catalog.json` entry still missing one, by researching the official
AWS docs and writing each file, until `python3 scripts/check.py` passes. Limit
the scope by adding a `Scope: <category>` line above the pasted instructions.

## Add a new service
1. Add an entry to `catalog.json` (`name`, `slug`, `path`, `type`, `aws_service_code`).
2. Paste [`GENERATE.md`](GENERATE.md) (with `Scope: <category>`) to generate it.
3. `python3 scripts/check.py --write-index` to refresh `catalog.md` and the SKILL.md index.

## Update an existing doc (diff/review)
1. Regenerate into a staging folder, e.g. `_staging/services/...`.
2. `python3 scripts/check.py --baseline _staging` to see what changed.
3. Replace, validate, commit.

## Validate before commit (gate)
```bash
python3 scripts/check.py                 # per-push: conformance of existing files (missing = warning)
python3 scripts/check.py --strict        # release gate: every catalog entry must have a file
python3 scripts/check.py --check-links    # validate links (network)
```
CI runs the non-strict `check.py` on every push/PR (`.github/workflows/check.yml`),
so the badge stays green while content is being filled in. Run `--strict` (full
coverage) before tagging a release.

## Scripts (utilities only)
The loop logic lives in `GENERATE.md`. The scripts are just utilities the loop
calls:
- `scripts/check.py` — validate (coverage/conformance/links), `--missing [category]`
  to list entries still to generate, `--write-index` to regenerate the indexes,
  `--baseline DIR` to diff a regeneration.
- `scripts/cost.py` — token ledger: `add --name --tokens --agents --files` records a
  workflow run's `subagent_tokens` and re-renders the cost section of the README and
  `docs/build-cost.md`; `render` re-renders from the ledger.

## Release
Bump `version` in `catalog.json`, add a `CHANGELOG.md` entry, sync `README.md`,
tag `vX.Y.Z` only when stable. Never force-push a released tag.
