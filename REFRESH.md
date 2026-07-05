# Refresh the AWS best-practices catalog

Self-contained instructions: paste this whole file into a new chat with any
terminal coding agent (Claude Code, Codex CLI, etc.) whose working directory is
this repository, to run a periodic maintenance pass: pick up AWS services that
didn't exist when the catalog was last built, drop ones AWS has fully retired,
and re-review content that's gone stale. Run this every 3–6 months, whenever
AWS GA's a new service you notice is missing, or whenever `scripts/check.py`
reports stale entries.

This is the sibling of [`GENERATE.md`](GENERATE.md): that file fills in files
that don't exist yet; this one keeps files that already exist correct and
current, and grows the catalog itself when AWS grows. Read `MAINTENANCE.md`
first if you haven't; it explains the file layout and validation gate this
prompt assumes.

---

## Part 1. Catalog drift: new, renamed, and retired services

Goal: `catalog.json` matches AWS's current service lineup before you refresh
any content. Skipping this step means you might spend a whole pass polishing
descriptions of a service AWS deprecated last quarter, while a service AWS
shipped this quarter stays invisible.

1. Get an authoritative current service list. In order of preference:
   - An AWS documentation/pricing MCP tool, if available (e.g. a
     `get_pricing_service_codes`-style tool, or an AWS Knowledge
     `search_documentation` call for "AWS services list" / "AWS product and
     service portal").
   - Otherwise, web search for `"AWS products and services list"` and
     `"AWS What's New"` (filtered to the last 6–12 months) and read the
     official `aws.amazon.com/products/` category pages.
2. Diff that list against `catalog.json`'s `categories.*.services[]` (match on
   `name` / `aws_service_code`, not just `slug`: AWS renames products; see
   `CHANGELOG.md` for precedent like `Amazon GameLift` → `Amazon GameLift
   Servers`). For each mismatch, classify it as one of:
   - **New**: a GA, generally-available-to-new-customers service with no
     matching catalog entry. Confirm it's not a preview/beta and not already
     covered under a different name.
   - **Renamed**: same underlying service, new official product name. Update
     `name` (and `slug`/`path` only if the old ones would be actively
     misleading) in place; do not create a duplicate entry, and do not touch
     the existing `.md` file's content just for the rename (a follow-up
     refresh pass will pick up the file's `# <name>` line naturally).
   - **Retired**: fully shut down, no longer operable at all (compare against
     the precedent in `CHANGELOG.md`: AWS QLDB, OpsWorks, RoboMaker, IoT
     Analytics, IoT Events were removed this way). This is different from
     "closed to new customers": a service still usable by existing customers
     (e.g. AWS Elemental MediaStore's discontinuation, or a service closed to
     new sign-ups) keeps its catalog entry; write/keep migration- or
     lifecycle-planning-focused best practices for it instead of removing it.
   - **Recategorized**: AWS moved a service to a different product category in
     its own taxonomy. Move the entry between `categories` in `catalog.json`.
3. Apply the diff to `catalog.json` directly (add/rename/move/remove entries;
   add a brand-new `categories.<key>` block only if AWS introduced a genuinely
   new top-level category). Record what changed in a `CHANGELOG.md` entry.
4. For newly-added entries, generate their files exactly like `GENERATE.md`'s
   step 2 (`generate` → `verify`, Workflow fan-out if available). For removed
   entries, delete the `.md` file if one exists.

## Part 2. Refresh stale content

Goal: every existing file's `last_reviewed` date is recent, and its content
reflects AWS's current guidance, not what was true when it was last written.

1. List what's due: `python3 scripts/check.py --stale <scope-or-empty>` → a
   JSON array of entries `{ name, slug, path, abspath, type, category,
   last_reviewed, age_days }`, sorted oldest-first, for files whose trailing
   `<!-- meta: last_reviewed=... -->` is missing or older than the default
   180-day threshold (override with `--stale-days N`).
2. Refresh a batch (Workflow fan-out if available, one agent per entry,
   otherwise sequential, same pattern as `GENERATE.md`):
   - **re-research**: look up the same official AWS sources as a fresh
     generation would (AWS documentation MCP if available, otherwise web
     search for `"<name> best practices"`, `"<name> security best practices"`,
     `"<name> Well-Architected"`, etc.), specifically checking for: new
     best-practice pages or Well-Architected lens content that didn't exist
     before, practices that no longer apply (superseded features, deprecated
     APIs), and whether every existing `[doc]` link still resolves and still
     supports its bullet's claim.
   - **update**: edit the file in place: add genuinely new practices, remove
     ones AWS no longer recommends or that reference a retired feature, fix or
     replace any broken/mismatched link. Don't rewrite bullets that are still
     accurate just to reword them; a refresh is a content diff, not a rewrite.
     Keep following the same format rules as `GENERATE.md` (pillar sections
     only where real content exists, `[context]` + rationale + `[doc]` link on
     every bullet, no descriptions/pricing/tutorials/extended code).
   - **stamp**: update the trailing line to
     `<!-- meta: last_reviewed=<today>; sources=<n> -->` with the current date
     and the current distinct-source count, whether or not the content
     changed; a completed review is itself worth recording.
   - return `{ path, changed: true|false, notes: <one-line summary of what, if anything, changed> }`.
3. After the batch: run `python3 scripts/check.py` and fix anything it flags;
   record token usage with `python3 scripts/cost.py add --name "refresh:
   <category>" --tokens <tokens used> --agents <agent count> --files
   <refreshed>`; run `python3 scripts/check.py --write-index`; commit.

Repeat steps 1–3 until `python3 scripts/check.py --stale <scope-or-empty>`
returns an empty list for the given scope (or until you've covered the batch
size you intended for this pass; a partial refresh that's committed is
better than an uncommitted one, since `--stale` picks up exactly where you
left off next time).

---

Rules that always apply (same as `GENERATE.md`): only best practices, never
service descriptions, pricing, tutorials, or extended code. Every
non–`Common scenarios` bullet links to an official AWS URL
(`docs.aws.amazon.com`, `aws.amazon.com`, `wa.aws.amazon.com`). Never invent a
URL. Before adding a brand-new catalog entry, confirm the service is GA and
open to new customers. Before removing one, confirm it's fully retired, not
merely closed to new customers.
