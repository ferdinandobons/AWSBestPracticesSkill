# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Repository skeleton: `SKILL.md` router, `_TEMPLATE.md`, `MAINTENANCE.md`, CI.
- `catalog.json` source of truth: 208 services across 23 categories + 9 general docs.
- `scripts/check.py` validator + diff-checker (coverage, conformance, freshness,
  links, AWS-catalog comparison, baseline diff, index generation).
- `GENERATE.md`: a portable, tool-agnostic prompt for the generation/update
  loop — copy-paste into any terminal coding agent's chat (Claude Code, Codex
  CLI, etc.), no dependency on Claude Code's slash-command mechanism.
- Per-service and general best-practice content.
- Catalog audit against the live AWS service list: added 20 services confirmed
  missing (e.g. ROSA, Amazon File Cache, Amazon VPC Lattice, AWS Verified Access,
  AWS Artifact, AWS Well-Architected Tool, Amazon Bedrock AgentCore).

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
