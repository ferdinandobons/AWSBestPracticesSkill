# AWS Best Practices Skill

A skill for **Claude** and **Codex** that collects the **best practices of every
AWS service** — and nothing else. Find recommendations by **use case**:
security, reliability, performance, cost, operations, sustainability.

> **Scope:** this skill contains **only best practices**. No service
> descriptions, no pricing, no tutorials, no code walkthroughs. Just what AWS
> recommends you do, organized so you can act on it, each item linked to its
> official AWS source.

## What it contains / does NOT contain

| ✅ Contains | ❌ Does not contain |
|---|---|
| Best practices per service, by Well-Architected pillar | Service overviews / "what is X" |
| `[when-it-applies]` context tags per practice | Pricing, cost estimates, calculators |
| Cross-service general best practices | Tutorials / getting-started / how-to |
| Official AWS source link on every item | Extended code samples |

## Installation

**Claude Code** — install as a skill (one of):
- Clone into your skills directory: `git clone https://github.com/ferdinandobons/AWSBestPracticesSkill ~/.claude/skills/aws-best-practices`
- Or add it as a plugin/marketplace skill and let Claude load `SKILL.md`.

**Codex** — skills load natively; place the repo where Codex discovers skills and
it will pick up `SKILL.md`.

Once installed, ask things like *"best practices for securing my S3 bucket"* or
*"how should I run DynamoDB for a high-traffic app"* and the model opens the
matching `services/<category>/<service>.md`.

## How navigation works

`SKILL.md` is a router. The model identifies the service + concern from your use
case, opens the matching file under `services/`, reads the **Common scenarios**
map, then the relevant pillar sections.

```
SKILL.md                          # router / index
catalog.md                        # human-readable index (generated)
catalog.json                      # machine-readable source of truth
services/<category>/<service>.md  # per-service best practices
general/<topic>.md                # cross-service best practices
scripts/check.py                  # validator + diff-checker (maintainers)
```

Browse the full index in [`catalog.md`](catalog.md).

## Coverage

- **182 services** across 24 AWS categories + **9 general** cross-service docs.
- Best practices sourced from official AWS documentation and the
  Well-Architected Framework.

## Build cost

The entire best-practices corpus was generated autonomously by the `/goal`
command. Total build cost: **~_TBD_ tokens** (see [`docs/build-cost.md`](docs/build-cost.md)).

## Maintenance

This is a living collection. The update procedure, the `/goal` generation
command, and the validation gate are documented in
[`MAINTENANCE.md`](MAINTENANCE.md). Validate locally with:

```bash
python scripts/check.py
```

## License

MIT — see [`LICENSE`](LICENSE).
