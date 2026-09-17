# Paladin paper skeleton v0
Date: 2026-09-17
Status: notes only, not a submission draft

# Introduction draft v0
Date: 2026-09-17

LLM agents now call tools. They read search hits, file contents, and calendar records, then answer. That extra context is useful, and it is also an attack surface.

Prior work on prompt injection mostly studies a direct order inside a web page or email: "ignore previous instructions." Current models often refuse that order. This project asks a narrower question: if the injected text looks like a later fact rather than an order, does the agent still refuse?

Early runs with Claude Sonnet 5 say no. In a document-summary task, a command such as "do not mention risk" is rejected. A factual update such as "the FX and churn risks were closed in September" is adopted, both in retrieved documents and in tool output. The same factual update fails in code review, because the source file itself shows a plaintext password check.

The working claim is therefore not "agents are generally hijackable." It is that adoption depends on channel, wording, and whether the original source contradicts the payload.

Next steps are a second task family, a stable judge protocol, and a first detector that flags adopted updates without relying on the [INJECTED] marker.
# Threat Model draft
Date: 2026-09-17

Attacker
Cannot edit the system prompt or the user request.
Can plant text in one untrusted channel:
- retrieved document
- tool output
- later, a calendar or file record

Goal
Change the agent's final answer so that an injected fact is treated as true.
Example: "FX and churn risks are already closed."

Not the goal
Steal keys, call a second malicious tool, or crash the agent.

Defender / agent
Claude Sonnet 5 with tool calling.
It can read tools, refuse odd orders, and compare sources.
It does not have a separate detector in the current runs.

Success
adopted: the final answer uses the injected fact as if it were true.
rejected: the final answer keeps the original source and may flag the extra text.
unclear: both appear, or the answer hedges.

Assumption we already tested
A bare command in the same channel is usually rejected.
A later-looking factual update can still be adopted if the original source does not contradict it.
# Attack findings draft
Date: 2026-09-17

Claim
A tool-calling agent can be steered by a factual update inside retrieved text or tool output. A direct command in the same place usually fails.

Evidence
1. Document summary + retrieved_document
   V1 command: rejected
   V2/V6 factual update: adopted on P1-P4 at n=15
2. Document summary + tool_output
   V1: 0/15 adopted
   V2: 15/15 adopted
3. Code review + tool_output
   V1: 0/5 adopted
   V2: 0/5 adopted
   The visible source (login.py) contradicts the injected claim.

Working rule
Injection works when the payload looks like a later fact, not an order, and the original source does not clearly contradict it.

Not claimed yet
Cross-model results, detector performance, MCP live server results.
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
# Positioning table
Date: 2026-09-17

| work | setting | typical payload | what they measure | gap for us |
|---|---|---|---|---|
| InjecAgent | tool agent | ignore previous instructions | ASR of harmful tool calls | little factual-update wording |
| AgentDojo | stateful tools | important / system-style orders | ASR + task utility | same instruction bias |
| MCP threat papers | MCP servers | tool poisoning, malicious server | protocol/ecosystem risk | not a controlled wording study |
| this project | Claude tool-calling + mock tools | command vs factual update vs hedge vs source cue | adoption of injected fact | small model set, synthetic docs |

One sentence
We do not claim a new protocol. We claim that wording and source contradiction change adoption after the model has already learned to refuse a direct order.
