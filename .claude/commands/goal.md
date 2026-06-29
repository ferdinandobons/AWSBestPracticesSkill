Goal: every entry in `catalog.json` has a conformant best-practices file under `services/` or `general/`, verified by `python3 scripts/check.py` reporting **0 errors**. Scope: `$ARGUMENTS` (default: all). Keep making progress until that holds.

1. Find what is still missing: run `python3 scripts/check.py` — it lists every `missing file`. Restrict to `$ARGUMENTS` if a category was given.

2. Generate the next batch (one category, or ~10 entries) with the **Workflow tool**: write a workflow script that lists those entries inline — `{ name, abspath, type }` for each — because the tool's `args` are not reliably delivered to the script. Run one agent per entry in parallel: `pipeline(entries, generate, verify)`.
   - `generate` (one entry): load the AWS Knowledge MCP with ToolSearch `select:mcp__plugin_deploy-on-aws_awsknowledge__aws___search_documentation,mcp__plugin_deploy-on-aws_awsknowledge__aws___read_documentation`; `search_documentation` for `"<name> best practices"`, `"<name> security best practices"`, `"<name> Well-Architected"`, `"<name> reliability"`, `"<name> cost optimization"`; `read_documentation` on the most relevant official pages; then Write the file at its absolute path:
     - first line `# <name> — Best Practices`;
     - **service** → `## Common scenarios` (2–4 use-case → pillar lines, no links) then only the applicable Well-Architected pillar sections: `## 🔒 Security`, `## 🛡️ Reliability`, `## ⚡ Performance Efficiency`, `## 💰 Cost Optimization`, `## ⚙️ Operational Excellence`, `## 🌱 Sustainability`;
     - **general** → topic-based `## ` sections instead of pillars;
     - every practice bullet: `- **[context]** imperative practice — short rationale. [doc](official AWS URL)`;
     - final line `<!-- meta: last_reviewed=<today>; sources=<n> -->`;
     - return `{ path, status: "written" | "skipped" }`.
   - `verify` (one file): read it and reject it for the next batch if it contains any service description, pricing, tutorial, or extended code, or any practice bullet without an official AWS source link.

3. Run `python3 scripts/check.py --write-index`, fix anything it flags, and commit the batch.

Done when `python3 scripts/check.py` reports 0 errors. Constraints: only best practices — never service descriptions, pricing, tutorials, or extended code (cost-optimization practices are fine; prices are not). Every non–`Common scenarios` bullet links to an official AWS URL (`docs.aws.amazon.com`, `aws.amazon.com`, `wa.aws.amazon.com`). Never invent a URL. Skip an entry only if it genuinely has no published AWS best practices.
