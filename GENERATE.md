# Generate / update the AWS best-practices catalog

Self-contained instructions: paste this whole file into a new chat with any
terminal coding agent (Claude Code, Codex CLI, etc.) whose working directory is
this repository, to generate or refresh the best-practices files.

**Scope (optional):** to limit the work to one category, add a line above
these instructions, e.g. `Scope: database`. Without it, the scope is the
entire catalog.

---

Goal: every entry in `catalog.json` (within the scope above, or the whole file
if no scope was given) has a conformant best-practices file under `services/`
or `general/`, verified by `python3 scripts/check.py` reporting 0 errors. Keep
making progress until that holds for the given scope.

1. List what is missing: `python3 scripts/check.py --missing <scope-or-empty>`
   → a JSON array of entries `{ name, slug, path, abspath, type, category }`
   whose file does not exist yet.

2. Generate a batch (one category, or ~10 entries):
   - If a Workflow tool (or equivalent parallel-agent orchestration) is
     available, use it to generate in parallel: embed the entries directly in
     the workflow script (tool `args` are not always delivered reliably); run
     `pipeline(entries, generate, verify)`, one agent per entry.
   - If no such tool is available in this environment, process entries one at
     a time in sequence, still following the `generate` → `verify` steps below
     for each.
   - **generate** (one entry): look up the official AWS documentation for that
     service. If an AWS documentation MCP/tool is available, use it
     (`search_documentation` + `read_documentation`); otherwise use web search
     for `"<name> best practices"`, `"<name> security best practices"`,
     `"<name> Well-Architected"`, `"<name> reliability"`,
     `"<name> cost optimization"`, and read the most relevant official pages.
     Then write the file at `abspath`:
     - line 1: `# <name> — Best Practices`;
     - **service** entries → `## Common scenarios` (2–4 use-case → relevant-pillar
       lines, no links) then only the Well-Architected pillar sections that
       actually apply: `## 🔒 Security`, `## 🛡️ Reliability`,
       `## ⚡ Performance Efficiency`, `## 💰 Cost Optimization`,
       `## ⚙️ Operational Excellence`, `## 🌱 Sustainability`;
     - **general** entries → topic-based `##` sections instead of pillars;
     - each practice bullet: `- **[context]** imperative practice — short
       rationale. [doc](official AWS URL)`;
     - last line: `<!-- meta: last_reviewed=<today>; sources=<n> -->`;
     - return `{ path, status: "written" | "skipped" }`.
   - **verify** (one file): read it back and reject it (leave it for the next
     pass) if it contains any service description, pricing, tutorial, or
     extended code sample, or any practice bullet without an official AWS
     source link.

3. After the batch: run `python3 scripts/check.py` and fix anything it flags;
   record the run's token usage with `python3 scripts/cost.py add --name
   "<category>" --tokens <tokens used> --agents <agent count> --files <written>`;
   run `python3 scripts/check.py --write-index`; commit.

Repeat steps 1–3 until `python3 scripts/check.py --missing <scope-or-empty>`
returns an empty list for the given scope. If the scope was the whole catalog,
the project's overall finish line is `python3 scripts/check.py --strict`
reporting 0 errors (every catalog entry has a file); a scoped run's own
"done" is just that scope's missing list being empty, not the whole catalog.

Rules that always apply: only best practices, never service descriptions,
pricing, tutorials, or extended code (cost-optimization practices are fine;
prices are not). Every non–`Common scenarios` bullet links to an official AWS
URL (`docs.aws.amazon.com`, `aws.amazon.com`, `wa.aws.amazon.com`). Never
invent a URL. Skip an entry only if it genuinely has no published AWS best
practices. Before adding brand-new catalog entries, check whether the service
is still active and open to new customers; don't spend a generation pass on
a service AWS has already deprecated or closed to new customers.
