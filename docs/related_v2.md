# Related Work (v2)

| Work | What it measures | Difference from this paper |
|---|---|---|
| Greshake et al. / indirect PI | Instructions hidden in retrieved content | We fix one goal and vary channel |
| Zhan et al., InjecAgent (ACL Findings 2024) | 1,054 IPI cases, harm vs exfil on tool agents | Broader tools; we isolate channel/framing on one summary task |
| Debenedetti et al., AgentDojo (NeurIPS 2024) | Dynamic tool tasks + utility under attack | We do not score utility of a full office agent |
| BIPIA / ASB | Broader IPI and agent-security suites | Different threat taxonomy; not our contribution |
| OWASP LLM01 | Industry ranking of prompt injection | Not a measurement paper |
| MCP / GitHub-MCP case studies | Real protocol incidents | Out of scope for this mock-tool study |
| Framing-gap work on tool agents (2026) | Overt vs reframed exfil | Closest in spirit; we measure summary hijack by channel |

Position: a measurement note on channel and framing, not a new benchmark or a production detector.
