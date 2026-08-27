# Measuring Channel-wise Tool Hijacking and Context Manipulation in Tool-Calling Agents

## Abstract
Tool-calling agents can treat untrusted tool outputs and retrieved documents as evidence. We measure this risk on a Claude agent across four injection channels. Factual text in retrieved documents is more effective than explicit commands. A small refusal-aware detector separates resisted and hijacking cases in an 8-sample set. Stronger detection of document-style poisoning is future work.

## 1. Introduction
Tool-calling agents retrieve documents and invoke tools. Untrusted content therefore becomes part of the decision path. This paper measures that problem instead of proposing a full defense.

Contributions.
1. A small reproducible testbed.
2. Channel-wise evidence that factual retrieved content works better than explicit commands.
3. A first runtime detector on real logs, with document-style detection left to future work.

## 2. Related Work
Prompt injection and indirect injection showed that untrusted text can steer models [Perez and Ribeiro 2022; Greshake et al. 2023; Liu et al. 2024]. Agent and ICL work shows the same trust-boundary issue when third-party content enters context [Zhang et al. 2019; He et al. 2026]. MCP is one connector, not the whole problem [Anthropic 2024]. This paper measures one attack goal across four channels in a tool-calling loop.

## 3. Threat Model
The attacker cannot change weights or the user request. The attacker can poison one untrusted channel: tool output, retrieved document, system message, or intermediate message. Out of scope: full MCP compromise and containment.

## 4. Attack
Tasks: document summary and code review.
Payloads: direct command vs factual rewrite.
Result: retrieved_document 3/3, tool_output 1/3, system_message 0/3, intermediate_message 0/3.
Finding: trusted-looking source text is more effective than an explicit command.

## 5. Detection
Compare control vs treatment.
Features: similarity, goal words, refusal words.
Rule: refused → resisted; goal taken and not refused → hijacking; else no_effect.
Limit: source-like poisoning without refusal is still hard.

## 6. Evaluation
Table 1 and Figures 1-2 as previously recorded.
Detector v1.1: 8/8 on dataset v2 after tuning.
These numbers are preliminary.

## 7. Discussion
The main meaning is practical. An agent can reject a command and still accept a fake fact if that fact sits in a document-shaped place.

This does not generalize yet. The study uses one model, Korean tasks, mock tools, and small n. Language may affect refusal style. A second model and an English replica are needed before a broader claim.

The detector is a first filter, not a product. It catches explicit refusal well. It is not a solution to quiet document-style poisoning. That is the next paper, not this one.

## 8. Conclusion
We measured tool hijacking and context manipulation in a tool-calling agent. Attack success depends on channel and framing. Retrieved factual content is the most effective path in this setup. A simple runtime detector can separate refused attacks from successful ones in a small sample. Future work should detect document-style poisoning more strongly and test more models.

## Issues
- Related Work citations are short-form, not full venue format.
- No English replica experiment.
- No second model.
- Sample size is small.
- Front-half and evaluation drafts were merged here; wording can still be tightened.

## References
- Perez, F., and Ribeiro, I. 2022. Ignore previous prompt.
- Greshake, K., et al. 2023. Not what you've signed up for.
- Liu, Y., et al. 2024. Formalizing and benchmarking prompt injection.
- Zou, A., et al. 2023. Universal and transferable adversarial attacks.
- Zhang, N., et al. 2019. Dangerous skills.
- He, N., et al. 2026. ICL-Evader.
- Anthropic. 2024. Model Context Protocol specification.