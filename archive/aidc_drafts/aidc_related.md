# AIDC Related Work draft

Indirect prompt injection showed that untrusted retrieved text can override a model's instructions. Greshake et al. demonstrated this in retrieval settings, where the attack sits inside documents rather than in the user prompt. Our study keeps that threat but measures a quieter payload: a factual rewrite, not an explicit ignore-previous-instructions command.

Perez and Ribeiro framed prompt injection as an instruction conflict. That view still matters for system-message attacks. In our pilot, the system-message channel did not produce adoption. The successful path was source-like text in tool outputs and retrieved documents.

Agent benchmarks such as AgentDojo evaluate tool-using agents under a broad attack suite. They are larger and more general than this draft. We do not replace that benchmark. We isolate one payload, four channels, and two languages, then correct a labeling error that keyword matching introduces.

MCP and related agent-tool notes treat tool results as an untrusted boundary. That is the practical setting of this measurement. We do not audit the MCP specification. We only show that, in a mock tool-calling loop, a factual sentence in tool or document text can be adopted in Korean and rejected in English on Claude Sonnet 5.

This draft is therefore a slice, not a survey and not a new attack family.
