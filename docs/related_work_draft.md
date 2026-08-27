# Related Work Draft

Prompt injection research showed that language models can be steered by untrusted text. Direct injection targets the prompt. Indirect injection hides instructions in retrieved documents, web pages, or emails. These papers established the problem, but many evaluate a single-turn model response rather than a tool-calling agent.

Agent security work extends this setting. Once a model can search documents, read files, or call APIs, poisoned content can influence not only wording but also the agent’s tool use and final decision. Protocols such as MCP matter because they connect models to third-party tools, yet the underlying issue is broader than one protocol: untrusted tool I/O enters the model context.

Attacks on in-context learning are also relevant. Models treat nearby text as evidence. That helps explain a result in this paper: a factual sentence inside retrieved content can succeed where an explicit “ignore the risk” command fails.

Detection work includes keyword filters, alignment, and LLM-as-judge methods. Judges are convenient but can themselves be manipulated. This paper therefore starts with inspectable runtime features: response change, goal-word uptake, and explicit refusal.

Positioning. We do not propose a complete containment architecture. We contribute a small systems-level measurement: the same attack goal across four channels in a real tool-calling agent, plus a first detector on the resulting logs.