# AWS Best Practices Skill

**Ask your AI coding agent "how should I secure my S3 bucket" and get a sourced, current best practice — not a guess from stale training data.**

A skill for **Claude Code** and **OpenAI Codex CLI** that collects the **best
practices of every AWS service** — and nothing else. Find recommendations by
**use case**: security, reliability, performance, cost, operations,
sustainability, each one linked to its official AWS source.

> **Scope:** this skill contains **only best practices**. No service
> descriptions, no pricing, no tutorials, no code walkthroughs. Just what AWS
> recommends you do, organized so you can act on it, each item linked to its
> official AWS source.

## Why this instead of just asking the model directly

There are three ways an AI agent can answer "what are the best practices for
this AWS service":

1. **From memory** — free and instant, but the model's training data goes
   stale the moment AWS ships a new feature, renames a service, or updates its
   Well-Architected guidance. It will still answer confidently even when it's
   wrong or out of date.
2. **Live research** — the agent runs web searches or queries an AWS
   documentation MCP server on the spot, every time. This gets it right, but
   it's expensive: several search → fetch → read round-trips, burning tens of
   thousands of tokens, repeated for every question, even the same one asked
   twice.
3. **This skill** — the research is already done, once, per service, and
   stored as a small, source-linked file. The agent opens exactly
   `services/<category>/<service>.md`, reads a few hundred lines, and answers
   — no live search needed and no repeated token cost, while every practice is
   still traceable to an official `docs.aws.amazon.com` / `aws.amazon.com` /
   `wa.aws.amazon.com` page. And because content ages, a documented refresh
   loop (below) keeps it from silently drifting back into "stale training
   data" territory.

## What it contains / does NOT contain

| ✅ Contains | ❌ Does not contain |
|---|---|
| Best practices per service, by Well-Architected pillar | Service overviews / "what is X" |
| `[when-it-applies]` context tags per practice | Pricing, cost estimates, calculators |
| Cross-service general best practices | Tutorials / getting-started / how-to |
| Official AWS source link on every item | Extended code samples |

## Quick start

**1. Install the coding agent** (skip if you already have one):

```bash
# Claude Code
npm install -g @anthropic-ai/claude-code
claude --version   # verify

# OpenAI Codex CLI
npm install -g @openai/codex
codex --version    # verify
```

**2. Install this skill:**

```bash
# Claude Code
git clone https://github.com/ferdinandobons/AWSBestPracticesSkill ~/.claude/skills/aws-best-practices

# OpenAI Codex CLI
git clone https://github.com/ferdinandobons/AWSBestPracticesSkill ~/.codex/skills/aws-best-practices
```

Restart the tool if it's open, then just ask in natural language:

> *"best practices for securing my S3 bucket"* · *"how should I run DynamoDB for high traffic"* · *"AWS account security baseline"* · *"is my Lambda function set up correctly for production"*

The model reads [`SKILL.md`](SKILL.md), opens the matching
`services/<category>/<service>.md` (or `general/<topic>.md`), and answers with
sourced best practices — it won't need to open anything else in this repo.

Update anytime:
```bash
git -C ~/.claude/skills/aws-best-practices pull   # or ~/.codex/skills/aws-best-practices
```

## How navigation works

`SKILL.md` is a router. The model identifies the service + concern from your
use case, opens the matching file under `services/`, reads the **Common
scenarios** map, then the relevant pillar sections.

```
SKILL.md                          # router / index — what the model reads first
catalog.md                        # human-readable index (generated)
catalog.json                      # machine-readable source of truth
services/<category>/<service>.md  # per-service best practices
general/<topic>.md                # cross-service best practices
scripts/                          # maintainer utilities (check.py, cost.py)
GENERATE.md                       # fills in missing files (maintainers)
REFRESH.md                        # periodic refresh: new services + stale content (maintainers)
```

Browse the full index in [`catalog.md`](catalog.md).

## Coverage

- **208 services** across 23 AWS categories + **9 general** cross-service docs — 217 files, all complete.
- Best practices sourced from official AWS documentation and the Well-Architected Framework.
- Every source link verified live (HTTP 200, official AWS host) as of the last full check.

## How the catalog stays current

This isn't a one-time snapshot. Two portable, tool-agnostic prompts drive the
catalog's lifecycle — paste either into a Claude Code / Codex CLI chat in this
repo:

- **[`GENERATE.md`](GENERATE.md)** fills in any catalog entry that doesn't
  have a file yet, researching official AWS docs per service.
- **[`REFRESH.md`](REFRESH.md)** runs periodically to (1) diff `catalog.json`
  against AWS's current service list — picking up new services, catching
  renamed or recategorized ones, dropping fully-retired ones — and (2)
  re-review existing files whose content has gone stale, per
  `scripts/check.py --stale` (default: no review in the last 180 days).

Both are gated by [`scripts/check.py`](scripts/check.py), which validates
structure, coverage, freshness, and link health with zero external
dependencies (`--check-links` hits the network; everything else is a pure
stdlib parse), so a maintenance pass can't silently drift from the "only
best practices, always sourced" rule.

## Build cost

The entire best-practices corpus is generated by pasting [`GENERATE.md`](GENERATE.md)
into a coding agent's chat. Token usage is tracked from each generation run.

<!-- BUILD-COST -->
**Generation cost so far: ~30.51M tokens** (30,510,969) across 481 workflow agents · 217 files. See [`docs/build-cost.md`](docs/build-cost.md) for the per-phase breakdown.
<!-- /BUILD-COST -->

## Maintenance

This is a living collection. The update procedure — generating missing
entries with [`GENERATE.md`](GENERATE.md), keeping the catalog current with
[`REFRESH.md`](REFRESH.md), and the validation gate — is documented in
[`MAINTENANCE.md`](MAINTENANCE.md). Validate locally with:

```bash
python3 scripts/check.py                # coverage + conformance + freshness summary
python3 scripts/check.py --strict       # release gate: every catalog entry has a file
python3 scripts/check.py --check-links  # validate all source links (network)
python3 scripts/check.py --stale        # list entries due for a REFRESH.md pass
```

Contributions welcome — see [`MAINTENANCE.md`](MAINTENANCE.md) before opening a PR.

## License

MIT — see [`LICENSE`](LICENSE).
