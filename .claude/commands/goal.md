---
description: Generate AWS best-practice files via recursive, parallel workflows (one child workflow per category, one agent per service).
argument-hint: "[--all | --stale | <category>]"
---

# /goal — recursive parallel generation of best-practice files

You are the maintainer driver for **AWSBestPracticesSkill**. Generate the missing
(or stale) best-practice files by launching the recursive `goal` Workflow.

**Arguments:** `$ARGUMENTS`
- empty or `--all` → every catalog entry whose file is missing.
- `--stale` → missing files **and** files past the freshness threshold (180 days).
- `<category>` (e.g. `database`, `general`) → only that category's missing files.

## Procedure

1. **Build the work-list.** Run this helper (it reads `catalog.json`, checks which
   files exist / are stale, groups pending entries by category, and writes the
   Workflow args JSON). Pass the same `$ARGUMENTS` through:

   ```bash
   python3 scripts/goal_worklist.py $ARGUMENTS > "$CLAUDE_SCRATCH/goal_args.json" 2>/dev/null \
     || python3 scripts/goal_worklist.py $ARGUMENTS
   ```

   (The helper lives at `scripts/goal_worklist.py`. If `$CLAUDE_SCRATCH` is unset,
   just read the JSON it prints to stdout.) The JSON has the shape:
   `{ "childScriptPath": "<abs path to .claude/workflows/goal-category.js>",
      "categories": [ { "category", "title", "services": [ {name, slug, path, abspath, type, aws_service_code} ] } ] }`

2. **Stop early if empty.** If `categories` is empty, report "nothing to generate"
   and stop — do not launch a workflow.

3. **Launch the Workflow.** Call the `Workflow` tool with `name: "goal"` and
   `args` set to the JSON object from step 1 (pass it as a real JSON value, not a
   string). This runs one **child workflow per category in parallel**, each fanning
   out one **generate → verify** agent chain per service (bounded retry on
   verification failure).

4. **Apply results to the catalog.** When the workflow returns, for every result
   with `status: "written"`, update its `catalog.json` entry: set
   `last_reviewed` to today, `pillars` to the returned pillars, and `sources` to
   the returned count. Use:

   ```bash
   python3 scripts/goal_apply.py "$CLAUDE_SCRATCH/goal_results.json"
   ```

   after writing the workflow's `results` array to that path — or update
   `catalog.json` directly for the handful of written entries.

5. **Validate.** Run `python3 scripts/check.py` (and `--check-links` if generating
   broadly). Report: written / skipped / failed counts, and any validation errors.

6. **Re-run for the tail.** If any services `failed` or validation reports missing
   files, run `/goal` again — it only picks up what is still missing — until the
   work-list is dry.

## Notes
- Workflow scripts cannot read the filesystem, so the work-list is passed via
  `args`; the spawned agents (full subagents with file + MCP tools) do the writes.
- Workflow nesting is one level: parent (`goal`) → category children
  (`goal-category`); children use agents only, never another `workflow()` call.
- Keep the "only best practices" rule absolute: the verify stage rejects any file
  containing descriptions, pricing, tutorials, or extended code.
