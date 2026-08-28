# Measuring Channel-wise Tool Hijacking and Context Manipulation in Tool-Calling Agents

## Highlights
- Tool-calling agents can treat retrieved documents as evidence rather than as data.
- The same attack goal succeeds at different rates across four injection channels.
- Factual retrieved-document text is more effective than explicit commands in this setup.
- A prototype detector is described only as future work; its current scores are not a main result.
- Stronger and independent detection of quiet document-style poisoning is left to later work.

## Abstract
Autonomous agents retrieve documents and call tools, so untrusted content can enter the decision path. This paper measures that risk on a Claude tool-calling agent. We inject one attack goal through four channels: tool output, retrieved document content, system messages, and intermediate messages. In this setup, factual sentences placed in retrieved documents succeed more often than explicit commands or intermediate notes. The study reports channel-wise outcomes. It does not claim an independent defense. Earlier prototype detector scores are omitted because labeling and detection shared keyword rules.

## 1. Introduction
Tool-calling agents act on retrieved text. That creates a boundary problem. Content written as source material can change the final answer even when the user request is benign.

Prior work showed that injected text can steer language models. We ask a narrower question: if the goal is fixed, which channel changes a tool-calling agent?

This paper contributes a small testbed and a channel-wise comparison on Claude. It does not claim a general detector or a complete defense. Independent detection metrics are left to later work.

## 2. Related Work
Prompt injection studies established that untrusted text can steer models [Perez and Ribeiro 2022; Greshake et al. 2023; Liu et al. 2024]. Related attacks target alignment [Zou et al. 2023]. Many evaluations still use a single-turn response.

Closer work studies trust boundaries around third-party skills and in-context evidence [Zhang et al. 2019; He et al. 2026]. MCP is one connector that brings tool I/O into context [Anthropic 2024]. Our difference is measurement across four channels in one tool-calling loop.

## 3. Threat Model
The attacker cannot modify model weights or the user prompt. The attacker can poison one untrusted channel: tool output, retrieved document content, a system message, or an intermediate message. We do not study MCP server compromise or containment.

## 4. Attack
We evaluate document summary and code review with direct and factual payloads. An attack succeeds when the treatment answer moves toward the payload and is not explicitly refused.

For a factual risk-resolved payload (n=3), retrieved_document succeeded in 3/3 trials, tool_output in 1/3, and system_message and intermediate_message in 0/3. A competitor-lag sentence in retrieved content was accepted. A “no vulnerability” sentence in code review was refused.

The same claim is therefore weaker as a command and stronger as document-shaped evidence.

## 5. Detection
We do not report detection performance as a main result.

A prototype compared control and treatment answers using similarity, goal-word uptake, and refusal cues. That prototype is not an independent evaluator: its decision rules overlapped with the labeling keywords. Agreement with those labels is therefore circular and is not reported here.

Independent Precision, Recall, and F1 are TBD. They will be computed only after labeling rules and detector features use different signals (`metrics_v3`).

## 6. Evaluation
Dataset v2 contains eight labeled cases: two hijacking, five resisted, and one no_effect. These counts describe attack outcomes, not detector quality.

The supported claim is descriptive and local: in this setup, channel and payload style change whether Claude follows or resists the injected text. Larger repeats, an English replica, and a second model are required before a broader claim.

## 7. Discussion
An agent can reject an explicit order and still accept a fake fact. That is the main practical observation.

The study is limited to one model, mainly Korean-language tasks, mock tools, and a small sample. Language may affect refusal style. A second model and an English replica are required before a broader claim.

## 8. Limitations
The current detector prototype is not an independent evaluator. We do not report its agreement rate as evidence of detection performance. Tools are mocked. Sample size is small. Results should not be read as a general ranking of all agent stacks.

## 9. Conclusion
Attack success depends on channel and framing. Factual retrieved content is the strongest path observed here. Future work should separate labeling from detection, then evaluate additional languages and models.

## References
- Perez, F., and Ribeiro, I. 2022. Ignore previous prompt.
- Greshake, K., et al. 2023. Not what you've signed up for.
- Liu, Y., et al. 2024. Formalizing and benchmarking prompt injection.
- Zou, A., et al. 2023. Universal and transferable adversarial attacks.
- Zhang, N., et al. 2019. Dangerous skills.
- He, N., et al. 2026. ICL-Evader.
- Anthropic. 2024. Model Context Protocol specification.