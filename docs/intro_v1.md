# Introduction v1

Tool-calling agents retrieve documents and invoke tools. That makes untrusted content part of the decision path. A sentence that looks like source material can change the final answer even when the user request is benign.

This paper measures that problem instead of proposing a full defense. We inject the same goal through four channels in a Claude tool-calling agent: tool output, retrieved document content, system messages, and intermediate messages.

Three contributions:

1. A small reproducible testbed for tool hijacking and context manipulation.
2. Evidence that success depends on channel and framing. Factual retrieved content is more effective than explicit commands.
3. A first runtime detector on real logs, with a clear limit: better detection of document-style poisoning is left to future work.

The study uses one model, Korean tasks, mock tools, and a small sample. The claim is measurement, not a complete security system.