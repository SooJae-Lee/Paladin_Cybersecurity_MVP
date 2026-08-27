# Measuring Channel-wise Tool Hijacking and Context Manipulation in Tool-Calling Agents

## Highlights
- Tool-calling agents can treat retrieved documents as evidence rather than as data.
- The same attack goal succeeds at different rates across four injection channels.
- Factual retrieved-document text is more effective than explicit commands.
- A refusal-aware runtime detector separates resisted and hijacking cases in a small sample.
- Stronger detection of quiet document-style poisoning is left to future work.

## Abstract
Autonomous agents retrieve documents and call tools, so untrusted content can enter the decision path. This paper measures that risk on a Claude tool-calling agent. We inject one attack goal through four channels: tool output, retrieved document content, system messages, and intermediate messages. Factual sentences placed in retrieved documents succeed more often than explicit commands or intermediate notes. A simple detector that uses refusal words and goal-change features separates resisted attacks from hijacking in an eight-case set. The result is a measurement study, not a complete defense.

## 1. Introduction
Tool-calling agents act on retrieved text. That creates a boundary problem. Content written as source material can change the final answer even when the user request is benign.

Prior work showed that injected text can steer language models. We ask a narrower question: if the goal is fixed, which channel changes a tool-calling agent?

This paper contributes a small testbed, a channel-wise comparison on Claude, and a first runtime detector. It does not claim a general defense. Better detection of document-style poisoning is future work.

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
The detector compares control and treatment answers using similarity, goal-word uptake, and refusal cues. Low similarity alone is insufficient because Claude outputs already vary.

If refusal cues appear, the label is resisted. If the goal is taken without refusal, the label is hijacking. Otherwise the label is no_effect. This rule fits the current sample and remains weak for quiet source-like poisoning.

## 6. Evaluation
Dataset v2 contains eight cases: two hijacking, five resisted, and one no_effect. Detector v1.1 agrees on all eight after a precision fix. These scores are preliminary and should not be generalized. They support only a local claim: channel matters in this setup, and refusal-aware features help separate resisted cases from hijacking.

## 7. Discussion
An agent can reject an explicit order and still accept a fake fact. That is the main practical observation.

The study is limited to one model, Korean-language tasks, mock tools, and a small sample. Language may affect refusal style. A second model and an English replica are required before a broader claim. Detection is intentionally first-stage.

## 8. Conclusion
Attack success depends on channel and framing. Factual retrieved content is the strongest path observed here. A simple detector can use refusal and goal-change signals. Future work should detect document-style poisoning and evaluate additional models.

## References
- Perez, F., and Ribeiro, I. 2022. Ignore previous prompt.
- Greshake, K., et al. 2023. Not what you've signed up for.
- Liu, Y., et al. 2024. Formalizing and benchmarking prompt injection.
- Zou, A., et al. 2023. Universal and transferable adversarial attacks.
- Zhang, N., et al. 2019. Dangerous skills.
- He, N., et al. 2026. ICL-Evader.
- Anthropic. 2024. Model Context Protocol specification.