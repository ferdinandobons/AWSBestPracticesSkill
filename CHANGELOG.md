# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.1.2] - 2026-07-06

### Added
- GitHub Pages landing page under `docs/` with SEO metadata, catalog coverage
  summary, extraction process, refresh process, install commands, `robots.txt`,
  `sitemap.xml`, and `llms.txt`.
- GitHub Actions workflow to deploy the `docs/` directory to GitHub Pages.

### Changed
- Clarify in the README, skill router, plugin manifests, Pages site, and LLM
  metadata that this is an independent, unofficial project and not affiliated
  with or endorsed by AWS.
- Remove the orange `AWS` badge from the GitHub Pages header.

## [0.1.1] - 2026-07-05

### Changed
- README quickstart: use the `claude plugin`/`codex plugin` CLI syntax
  consistently for both tools, and split usage into direct invocation
  (`/aws-best-practices` standalone, `/aws-best-practices:aws-best-practices`
  as a plugin, or referencing `aws-best-practices` in a Codex CLI prompt) and
  indirect invocation (asking a natural-language question, which triggers the
  skill automatically).

## [0.1.0] - 2026-07-05

### Added
- Repository skeleton: `SKILL.md` router, `MAINTENANCE.md`, CI.
- `catalog.json` source of truth: 208 services across 23 categories + 9 general docs.
- `scripts/check.py` validator + diff-checker (coverage, conformance, links,
  baseline diff, index generation).
- `GENERATE.md`: a portable, tool-agnostic prompt for the generation loop,
  copy-paste into any terminal coding agent's chat (Claude Code, Codex CLI,
  etc.), no dependency on Claude Code's slash-command mechanism.
- Full content generation: all 217 catalog entries (208 services + 9 general
  docs) researched against official AWS documentation, each practice bullet
  source-linked; verified with `scripts/check.py --strict` (0 errors) and a
  full network link check (0 broken links across ~3,200 URLs).
- `scripts/check.py --stale [category] [--stale-days N]`: freshness check that
  reads each file's trailing `last_reviewed` date and flags entries missing it
  or older than the threshold (default 180 days); surfaced as a non-blocking
  summary line in the default `check.py` run too.
- `REFRESH.md`: a portable prompt (sibling of `GENERATE.md`) for the periodic
  maintenance pass. Diffs `catalog.json` against AWS's current service list
  to catch new/renamed/retired services, then re-reviews entries flagged by
  `--stale` against current official docs.
- Catalog audit against the live AWS service list: added 20 services confirmed
  missing (e.g. ROSA, Amazon File Cache, Amazon VPC Lattice, AWS Verified Access,
  AWS Artifact, AWS Well-Architected Tool, Amazon Bedrock AgentCore).
- Plugin installability for both Claude Code (`.claude-plugin/plugin.json` +
  `.claude-plugin/marketplace.json`) and Codex CLI (`.codex-plugin/plugin.json`
  + `.agents/plugins/marketplace.json`), verified end to end with
  `claude plugin marketplace add`/`install` and `codex plugin marketplace
  add`/`add`. Manual `git clone` into a skills directory remains as a backup
  install method.

### Changed
- Renamed catalog entries to match current official AWS product names: Amazon
  GameLift → Amazon GameLift Servers; Amazon WorkSpaces Web → Amazon WorkSpaces
  Secure Browser; Amazon AppStream 2.0 → Amazon WorkSpaces Applications; Route 53
  Application Recovery Controller → Amazon Application Recovery Controller (ARC).
- Recategorized AWS AppFabric (→ Business Applications) and Amazon Application
  Recovery Controller (→ Networking & Content Delivery) to match AWS's current
  product taxonomy.

### Removed
- Dropped catalog entries for services confirmed fully retired by AWS: Amazon
  QLDB, AWS OpsWorks, AWS RoboMaker, AWS IoT Analytics, AWS IoT Events. The
  `robotics` category was removed as a result (RoboMaker was its only entry).
- Dropped `_TEMPLATE.md`: orphaned once `GENERATE.md` started embedding the
  file format spec directly (self-contained by design), and unreferenced by
  any other doc.
