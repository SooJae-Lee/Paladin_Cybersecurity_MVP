# Threat Model

## Assets
- The agent’s final answer to the user
- Intermediate tool results that shape that answer
- Downstream actions implied by the answer, such as a “safe to deploy” review

## Adversary
The attacker cannot change the model weights or the user’s request.
The attacker can poison one untrusted context channel:
tool output, retrieved document content, a system-side message, or an intermediate message.

## Trust boundary
System and user prompts are treated as more trusted.
Tool outputs and retrieved documents are untrusted data, but the agent may still read them as evidence.

## Scope
In scope: channel-wise context manipulation and tool-result poisoning on a Claude tool-calling agent.
Out of scope: full MCP server compromise, multi-agent collusion, and containment mechanisms.