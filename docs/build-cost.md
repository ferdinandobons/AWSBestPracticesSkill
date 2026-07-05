# Build cost (token usage)

Tokens are extracted from each `GENERATE.md` generation run (`subagent_tokens`)
and accumulated here — generation agents only (research + write + verify).

| Phase | Files | Agents | Tokens |
|---|--:|--:|--:|
| compute | 11 | 31 | 1,814,728 |
| containers | 7 | 20 | 1,243,027 |
| storage | 10 | 28 | 1,742,112 |
| database | 14 | 36 | 2,180,054 |
| **Total** | **42** | **115** | **6,979,921 (~6.98M)** |
