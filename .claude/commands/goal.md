Goal: every entry in `catalog.json` has a conformant best-practices file under `services/` or `general/`, verified by `python3 scripts/check.py` reporting **0 errors**. Scope: `$ARGUMENTS` (a category, or empty for all). Keep making progress until that holds.

1. List what is missing: `python3 scripts/check.py --missing $ARGUMENTS` → a JSON array of entries `{ name, slug, path, abspath, type, category }` whose file does not exist yet.

2. Generate a batch (one category, or ~10 entries) with the **Workflow tool**. Embed those entries inline in the workflow script (the tool's `args` are not reliably delivered). Run `pipeline(entries, generate, verify)` — one agent per entry, in parallel.
   - `generate` (one entry): load the AWS Knowledge MCP — ToolSearch `select:mcp__plugin_deploy-on-aws_awsknowledge__aws___search_documentation,mcp__plugin_deploy-on-aws_awsknowledge__aws___read_documentation`; `search_documentation` for `"<name> best practices"`, `"<name> security best practices"`, `"<name> Well-Architected"`, `"<name> reliability"`, `"<name> cost optimization"`; `read_documentation` on the most relevant official pages; then Write the file at `abspath`:
     - line 1 `# <name> — Best Practices`;
     - **service** → `## Common scenarios` (2–4 use-case → pillar lines, no links) then only the applicable Well-Architected pillar sections: `## 🔒 Security`, `## 🛡️ Reliability`, `## ⚡ Performance Efficiency`, `## 💰 Cost Optimization`, `## ⚙️ Operational Excellence`, `## 🌱 Sustainability`;
     - **general** → topic-based `## ` sections instead of pillars;
     - each practice bullet: `- **[context]** imperative practice — short rationale. [doc](official AWS URL)`;
     - last line `<!-- meta: last_reviewed=<today>; sources=<n> -->`;
     - return `{ path, status: "written" | "skipped" }`.
   - `verify` (one file): read it and reject it (leave for the next pass) if it contains any service description, pricing, tutorial, or extended code, or any practice bullet without an official AWS source link.

3. After the batch: run `python3 scripts/check.py` and fix anything it flags; record the workflow run's token usage with `python3 scripts/cost.py add --name "<category>" --tokens <subagent_tokens> --agents <agent_count> --files <written>` (values from the workflow usage report); run `python3 scripts/check.py --write-index`; commit.

Done when `python3 scripts/check.py` reports 0 errors. Only best practices — never service descriptions, pricing, tutorials, or extended code (cost-optimization practices are fine; prices are not). Every non–`Common scenarios` bullet links to an official AWS URL (`docs.aws.amazon.com`, `aws.amazon.com`, `wa.aws.amazon.com`). Never invent a URL. Skip an entry only if it genuinely has no published AWS best practices.
