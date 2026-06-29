# Build cost (token usage)

Tokens are extracted from each `/goal` **workflow run** (`subagent_tokens` in the
workflow usage report) and accumulated here. This counts the generation agents
(research + write + verify); main-loop orchestration tokens are not included.

| Phase | Files | Agents | Tokens |
|---|--:|--:|--:|
| Validation (s3, lambda, tagging-strategy) | 3 | 6 | 340,784 |
| Compute | 9 | 18 | 1,025,058 |
| **Total** | **12** | **24** | **1,365,842 (~1.37M)** |
