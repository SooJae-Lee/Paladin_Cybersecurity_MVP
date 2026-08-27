# Introduction Draft

Autonomous AI agents no longer only generate text. They retrieve documents, inspect code, and call tools that can change the state of a system. This shift creates a practical security problem: content that looks like data can be interpreted as an instruction.

Prior work has shown that prompt injection and indirect prompt injection can manipulate language models. Those results mostly focus on the model itself. In deployed agents, however, the damage path is the tool-calling loop. A poisoned tool result or retrieved document can change the agent’s final answer or action even when the user prompt is benign.

This paper studies that systems-layer gap through a small but concrete testbed. We inject the same attack goal through four channels: tool output, retrieved document content, system messages, and intermediate messages. We then measure whether a tool-calling Claude agent changes its behavior.

The experiments show that attack success is highly channel-dependent. Direct commands and intermediate claims are often refused. Factual sentences placed inside retrieved document content are more likely to be accepted. We also adapt a simple runtime detector to real-model logs and show that refusal signals and response-change features can separate hijacking from resistance in a small labeled set.

This paper makes three contributions.

1. A reproducible tool-calling testbed for tool hijacking and context manipulation.
2. An empirical comparison of injection channels on a real LLM agent.
3. A first runtime detector and evaluation protocol for these attacks.

We do not claim a complete defense. The study is limited to one model, Korean-language tasks, mock tools, and a small sample. The goal is to measure the problem precisely enough to support later detection and containment research.