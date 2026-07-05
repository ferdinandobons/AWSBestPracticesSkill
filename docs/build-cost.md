# Build cost (token usage)

Tokens are extracted from each `GENERATE.md` generation run (`subagent_tokens`)
and accumulated here — generation agents only (research + write + verify).

| Phase | Files | Agents | Tokens |
|---|--:|--:|--:|
| compute | 11 | 31 | 1,814,728 |
| containers | 7 | 20 | 1,243,027 |
| storage | 10 | 28 | 1,742,112 |
| database | 14 | 36 | 2,180,054 |
| networking-content-delivery | 16 | 32 | 2,100,215 |
| security-identity-compliance | 23 | 46 | 2,892,048 |
| management-governance | 20 | 40 | 2,633,854 |
| **Total** | **101** | **233** | **14,606,038 (~14.61M)** |
