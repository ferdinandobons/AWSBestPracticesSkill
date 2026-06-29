# Build cost (token usage)

Tokens are extracted from each `/goal` **workflow run** (`subagent_tokens` in the
workflow usage report) and accumulated here. This counts the generation agents
(research + write + verify); main-loop orchestration tokens are not included.

| Phase | Files | Agents | Tokens |
|---|--:|--:|--:|
| Validation (s3, lambda, tagging-strategy) | 3 | 6 | 340,784 |
| **Total** | **3** | **6** | **340,784 (~341K)** |
