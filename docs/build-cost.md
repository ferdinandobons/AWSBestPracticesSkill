# Build cost (token usage)

This skill's best-practice content is generated autonomously by the `/goal`
command (research via the AWS Knowledge MCP + writing one file per service). This
note tracks the token cost of building it, for the README and social posts.

## How the number is measured

The agent cannot read its own live token meter from inside the session. The
authoritative figure comes from the host:

- **Claude Code:** run `/cost` (per-session) or check the usage shown at the end
  of the session / in the status line.
- **API usage dashboard:** the Anthropic console usage page for the build window.

The total is dominated by the mass `/goal` run (≈191 files, each doing several
MCP documentation reads + a generate + verify pass).

## Tally

| Phase | What | Tokens |
|---|---|---|
| Scaffolding | repo, `check.py`, catalog, docs, `/goal` command | _from `/cost`_ |
| Mass generation | `/goal` over all 191 entries | _from `/cost`_ |
| **Total** | | **_TBD — fill from `/cost` after the full run_** |

> Replace the `_TBD_` placeholder with the exact number from `/cost` once the full
> `/goal` generation has completed.
