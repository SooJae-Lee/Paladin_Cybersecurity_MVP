# Related Work draft

Prompt injection is well studied for single-turn chat.
The usual attack is a hidden instruction in a webpage or email:
"ignore previous instructions and do X."
Recent models often refuse that form.

Agent settings are different.
The model does not only read the user.
It also reads tool outputs, search snippets, and retrieved files.
Those channels look like evidence, not like a command.
Prior work on indirect prompt injection shows that this channel exists,
but most papers still test command-style payloads.

This paper focuses on a narrower case:
a factual update inside a retrieved document.
The payload does not say "ignore the policy."
It says the listed risk is already resolved.
The question is whether the agent copies that update into the summary.

Closest lines of work:
- prompt injection and jailbreaks in chat models
- indirect prompt injection through retrieved web content
- tool-using agents and MCP-style tool interfaces
- defenses based on instruction hierarchy and untrusted-context tags

The gap we target is measurement, not a new defense architecture.
We need a fixed task, a fixed source document, repeated trials,
and labels for adopted / rejected / unclear.
Without that, it is hard to say which channel actually changes the answer.
