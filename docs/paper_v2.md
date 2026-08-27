# Measuring Channel-wise Tool Hijacking and Context Manipulation in Tool-Calling Agents

## Abstract
Tool-calling agents can treat retrieved documents and tool outputs as evidence. We measure this risk on a Claude tool-calling agent by injecting the same goal through four channels. Factual text placed in retrieved document content succeeds more often than explicit commands or intermediate notes. A small refusal-aware detector separates resisted attacks from hijacking in an eight-case set. The study is a measurement paper. Stronger detection of quiet document-style poisoning is future work.

## 1. Introduction
Agents no longer only generate text. They fetch documents and call tools. That creates a trust problem: untrusted content can look like source material and change the answer even when the user prompt is clean.

Previous papers showed that injected text can steer models. This paper asks a narrower systems question. If the attack goal is fixed, which channel actually changes a tool-calling agent?

Contributions.
1. A small reproducible testbed for tool hijacking and context manipulation.
2. Channel-wise measurement on Claude: retrieved factual content is more effective than explicit commands.
3. A first runtime detector on real logs, with a clear limit on document-style cases.

This paper does not claim a general defense.

## 2. Related Work
Prompt injection and indirect prompt injection established that untrusted text can steer models [Perez and Ribeiro 2022; Greshake et al. 2023; Liu et al. 2024]. Alignment attacks made the same point at the model layer [Zou et al. 2023]. Most of that work evaluates a model response, not a tool loop.

Agent and ecosystem papers are closer. Third-party skills already broke a trust boundary in voice assistants [Zhang et al. 2019]. In-context learning can treat nearby assertions as evidence [He et al. 2026]. MCP matters as one way to connect tools [Anthropic 2024], but the issue is broader than one protocol.

This paper’s difference is measurement: one goal, four channels, a real tool-calling agent.

## 3. Threat Model
Assets: the final answer, the tool results that shape it, and implied decisions such as “safe to deploy.”
Adversary: cannot change weights or the user request; can poison one untrusted channel.
Channels: tool output, retrieved document, system message, intermediate message.
Out of scope: MCP server takeover, multi-agent collusion, containment.

## 4. Attack
We use two tasks, document summary and code review, and two payload styles, direct command and factual rewrite. Success means the treatment answer moves toward the payload without explicit refusal.

Results for the factual risk-resolved payload, n=3:
retrieved_document 3/3; tool_output 1/3; system_message 0/3; intermediate_message 0/3.

A competitor-lag sentence in retrieved content was accepted. A “no vulnerability” sentence in code review was refused. Figure 1 shows the channel rates.

The attack finding is simple. The same claim is weak as a command and stronger as source-like document text.

## 5. Detection
The detector compares control and treatment answers. Features are similarity, goal-word uptake, and refusal words. Low similarity alone is not enough because Claude answers already vary.

Rule.
- refusal present → resisted
- goal taken and no refusal → hijacking
- otherwise → no_effect

The rule fits the current sample. It is weaker when poisoned text looks like ordinary source material.

## 6. Evaluation
Dataset v2 contains 8 cases: 2 hijacking, 5 resisted, 1 no_effect. Detector v1.1 matches 8/8 after a precision fix. Figure 2 is the confusion matrix.

These scores are preliminary. They support only a local claim: channel matters on this Claude setup, and refusal-aware rules can separate resisted cases from hijacking in this sample.

## 7. Discussion
The practical meaning is that agents may reject an order and still accept a fake fact. That is why retrieved document content is the main risk path here.

The result should not be over-read. We used one model, Korean tasks, mock tools, and small n. Language may change refusal style. An English replica and a second model are needed before generalization.

Detection is intentionally limited. This paper measures the gap. Better detection of document-style poisoning is the next study.

## 8. Conclusion
Attack success in this tool-calling setup depends on channel and framing. Factual retrieved content is the strongest path we observed. A simple detector can use refusal and goal-change signals. Future work should detect quiet document-style poisoning and test more models.

## References
- Perez, F., and Ribeiro, I. 2022. Ignore previous prompt.
- Greshake, K., et al. 2023. Not what you've signed up for.
- Liu, Y., et al. 2024. Formalizing and benchmarking prompt injection.
- Zou, A., et al. 2023. Universal and transferable adversarial attacks.
- Zhang, N., et al. 2019. Dangerous skills.
- He, N., et al. 2026. ICL-Evader.
- Anthropic. 2024. Model Context Protocol specification.