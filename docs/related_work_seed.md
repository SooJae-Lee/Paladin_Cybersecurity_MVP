# Related Work seed list
Date: 2026-09-17

Use these first. Do not add random blogs.

## Prompt injection
1. Perez & Ribeiro. Ignore Previous Prompt. 2022.
2. Greshake et al. Not what you've signed up for (indirect prompt injection). 2023.
3. Liu et al. Formalizing and Benchmarking Prompt Injection Attacks and Defenses. USENIX Security 2024.

## Tool-using agents
4. Yao et al. ReAct. 2023.
5. Schick et al. Toolformer. 2023.

## Agent injection benchmarks
6. Zhan et al. InjecAgent. ACL Findings 2024. arXiv:2403.02691
   Gap: payloads are mostly explicit orders ("ignore previous instructions").
7. Debenedetti et al. AgentDojo. NeurIPS 2024. arXiv:2406.13352
   Gap: canonical attacks are still instruction-style.

## MCP security
8. Hou et al. MCP: Landscape, Security Threats, and Future Research Directions. arXiv:2503.23278
9. Song et al. Beyond the Protocol: Attack Vectors in the MCP Ecosystem. arXiv:2506.02040
10. Chen et al. MCPSecBench. arXiv:2508.13220

## Our difference
Those papers show agents can follow an injected order.
We measure when a later-looking fact is adopted even after the order is refused,
and when the original source blocks that fact (code review vs document update).
