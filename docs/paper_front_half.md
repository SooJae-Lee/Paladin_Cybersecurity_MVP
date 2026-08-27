# Measuring Channel-wise Tool Hijacking and Context Manipulation in Tool-Calling Agents

## 1. Introduction

Tool-calling agents retrieve documents and invoke tools. Untrusted content therefore becomes part of the decision path. A sentence that looks like source material can change the final answer even when the user request is benign.

Prior work showed that models can be steered by injected text. This paper measures the same problem in a tool-calling loop. We inject one attack goal through four channels on Claude: tool output, retrieved document content, system messages, and intermediate messages.

Contributions.

1. A small reproducible testbed for tool hijacking and context manipulation.
2. Evidence that success depends on channel and framing. Factual retrieved content is more effective than explicit commands.
3. A first runtime detector on real logs. Stronger detection of document-style poisoning is left to future work.

Limitations: one model, Korean-language tasks, mock tools, and a small sample. This is a measurement paper, not a complete defense.

## 2. Related Work

Prompt injection and indirect prompt injection showed that untrusted text can override or steer model behavior [Perez and Ribeiro 2022; Greshake et al. 2023; Liu et al. 2024]. Adversarial attacks on aligned models made the same point at the model layer [Zou et al. 2023]. These papers established the threat, but many evaluations use a single-turn response rather than a tool-calling agent.

Agent and ecosystem work is closer to this paper. Third-party skills already created a trust-boundary problem in voice assistants [Zhang et al. 2019]. In-context learning can also be evaded by fake assertions and diluted context [He et al. 2026]. Tool connectors such as MCP matter because they move third-party content into the model context [Anthropic 2024], but the issue is not limited to one protocol.

| Work | Focus | Gap vs this paper |
|---|---|---|
| Prompt injection papers | Model prompt / retrieved web text | Little channel-wise measurement in a tool loop |
| ICL evasion | In-context evidence manipulation | Not framed as agent tool I/O channels |
| Voice-skill security | Third-party skill trust boundary | Different interface, same structural issue |
| This paper | Four channels, one goal, tool-calling agent | Small n, one model, measurement only |

## 3. Threat Model

Assets. The final user-facing answer, the tool results that shape it, and implied decisions such as “safe to deploy.”

Adversary. The attacker cannot change model weights or the user request. The attacker can poison one untrusted channel: tool output, retrieved document content, a system-side message, or an intermediate message.

Trust boundary. System and user prompts are treated as more trusted. Tool outputs and retrieved documents are untrusted data, but the agent may still treat them as evidence.

Out of scope. Full MCP compromise, multi-agent collusion, and containment.

## 4. Attack

### 4.1 Setup
Tasks: Q3 report summary and login.py review.
Payload styles: direct command and factual rewrite.
Success: the treatment answer moves toward the payload and is not explicitly refused.

### 4.2 Channels
- tool_output: extra text in a tool result.
- retrieved_document: extra text in fetched document content.
- system_message: extra text in the system prompt.
- intermediate_message: an extra note after tool results.

The same claim changes meaning by location. A command looks like an instruction. A factual sentence in retrieved content looks like source material.

### 4.3 Results
Table 1. Factual risk-resolved payload, Claude Sonnet 5, n=3.

| Channel | Success |
|---|---|
| retrieved_document | 3/3 |
| tool_output | 1/3 |
| system_message | 0/3 |
| intermediate_message | 0/3 |

Figure 1. Channel-wise success rates (`docs/figures/channel_success.png`).

Additional cases. A competitor-lag sentence in retrieved content was accepted. A “no vulnerability / safe to deploy” sentence in code review was refused.

### 4.4 Finding
Not every injection works. Trusted-looking source text is more effective than an explicit command. Better detection of that document-style case is future work.

## References
- Perez, F., and Ribeiro, I. 2022. Ignore previous prompt.
- Greshake, K., et al. 2023. Not what you've signed up for.
- Liu, Y., et al. 2024. Formalizing and benchmarking prompt injection.
- Zou, A., et al. 2023. Universal and transferable adversarial attacks.
- Zhang, N., et al. 2019. Dangerous skills.
- He, N., et al. 2026. ICL-Evader.
- Anthropic. 2024. Model Context Protocol specification.