# Introduction draft v0
Date: 2026-09-17

LLM agents now call tools. They read search hits, file contents, and calendar records, then answer. That extra context is useful, and it is also an attack surface.

Prior work on prompt injection mostly studies a direct order inside a web page or email: "ignore previous instructions." Current models often refuse that order. This project asks a narrower question: if the injected text looks like a later fact rather than an order, does the agent still refuse?

Early runs with Claude Sonnet 5 say no. In a document-summary task, a command such as "do not mention risk" is rejected. A factual update such as "the FX and churn risks were closed in September" is adopted, both in retrieved documents and in tool output. The same factual update fails in code review, because the source file itself shows a plaintext password check.

The working claim is therefore not "agents are generally hijackable." It is that adoption depends on channel, wording, and whether the original source contradicts the payload.

Next steps are a second task family, a stable judge protocol, and a first detector that flags adopted updates without relying on the [INJECTED] marker.
