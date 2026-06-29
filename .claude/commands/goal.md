---
description: Autonomous goal-loop that generates AWS best-practice files until full coverage (Codex /goal "Ralph loop" style — work → check → continue/complete).
argument-hint: "[--all | --stale | <category>]"
---

# /goal — autonomous coverage loop

This is a **goal**, not a one-shot task. Work toward it in a loop across
iterations, the way Codex's `/goal` command does: **work → check → continue or
complete**. Do not stop after one batch — keep going until the verifiable end
state is reached.

## GOAL

> Complete the AWS best-practices coverage for scope **`$ARGUMENTS`** (default:
> all) — produce a conformant, source-linked best-practice file for every
> matching entry in `catalog.json` — and do not stop until
> `python3 scripts/check.py` reports **0 errors** for that scope.

**Verified by (evidence, not declaration):**
- `python3 scripts/check.py` → 0 errors (every file exists and conforms).
- `python3 scripts/check.py --check-links` → no broken links on the new files.

**Constraints that must NOT regress:**
- **Only best practices.** Never add service descriptions / "what is X",
  pricing or cost figures, tutorials / getting-started, or extended code samples.
- Every non–`Common scenarios` bullet ends with a Markdown link to an official
  AWS URL (`docs.aws.amazon.com`, `aws.amazon.com`, `wa.aws.amazon.com`).
- Never invent a URL — only cite pages you actually retrieved.
- Already-valid files must stay valid.

**Boundaries / tools:**
- Research only via the **AWS Knowledge MCP** (`search_documentation`,
  `read_documentation`). Load them with ToolSearch
  `select:mcp__plugin_deploy-on-aws_awsknowledge__aws___search_documentation,mcp__plugin_deploy-on-aws_awsknowledge__aws___read_documentation`.
- Write files under `services/<category>/` and `general/` only, using the
  format in [`_TEMPLATE.md`](../../_TEMPLATE.md).

## THE LOOP (repeat until done)

Each iteration:

1. **Assess state (evidence).** Get the remaining work-list:
   `python3 scripts/goal_worklist.py $ARGUMENTS`
   → JSON of pending entries grouped by category (missing files; with `--stale`
   also files past freshness).
2. **Completion check.** If `categories` is empty → the goal is **met**: run the
   final validation (step 6), update `README.md`/`CHANGELOG.md` counts, report,
   and **stop the loop**.
3. **Pick the next batch.** Take one category (or ~6–10 services) — the smallest
   useful checkpoint.
4. **Act, in parallel.** Dispatch one subagent **per service in the batch,
   concurrently** (this is the parallel fan-out). Give each subagent: the service
   name, its absolute file path, its `type` (service|general), and the format
   rules below. Each subagent researches via the AWS Knowledge MCP, extracts
   **only best practices**, and writes its file from the template.
5. **Validate + record.** Run `python3 scripts/check.py`; fix any conformance
   issues. Update each written entry's `last_reviewed` (today), `pillars`, and
   `sources` in `catalog.json` (helper:
   `python3 scripts/goal_apply.py <results.json>`), then
   `python3 scripts/check.py --write-index`. Commit the batch.
6. **Checkpoint log (compact).** Report: `<done>/<total> files · <remaining> left
   · blocked: <slugs with no published best practices>`. Then **continue to the
   next iteration**.

**Stop conditions:** full coverage (0 errors) · user pauses · a remaining
service genuinely has no published AWS best practices (mark it blocked, log it,
skip it — do not invent content).

## Per-service generation rules (give these to each subagent)

Write `# <Service> — Best Practices` then, for a **service**: `## Common
scenarios` (2–4 use-case → pillar lines, no links) followed by only the
applicable Well-Architected pillar sections (`## 🔒 Security`, `## 🛡️
Reliability`, `## ⚡ Performance Efficiency`, `## 💰 Cost Optimization`, `## ⚙️
Operational Excellence`, `## 🌱 Sustainability`). For a **general** doc: use
topic-based `## ` sections instead of pillars. Every practice bullet:
`- **[context]** imperative practice — short rationale. [doc](official AWS URL)`.
End with `<!-- meta: last_reviewed=<today>; sources=<n> -->`. Aim for ~12–20
high-signal, specific practices. Only best practices — nothing else.

## Self-pacing

- **Claude Code:** run `/loop /goal` to let the loop self-pace across turns, or
  just keep iterating this command until step 2 reports done.
- **Codex:** feed the GOAL block above to the native `/goal` command; Codex runs
  the same work → check → continue loop autonomously.
