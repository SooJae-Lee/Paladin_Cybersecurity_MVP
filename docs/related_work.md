# Related Work

Prompt injection in applications:
Greshake et al. show that untrusted retrieved text can override an LLM instruction.

Prompt injection as an attack class:
Perez and Ribeiro treat injection as a direct instruction conflict.

Agent benchmarks:
AgentDojo evaluates tool-using agents under attacks, but does not isolate channel and language on one factual payload.

MCP and agent interfaces:
Recent MCP security notes warn that tool results are an untrusted boundary.

This draft is narrower.
It does not propose a new attack name.
It measures one factual rewrite across four channels and two languages, then corrects keyword labels with an LLM-as-judge.

직접 명령 충돌을 다루는 연구와 달리, 이 초고는 사실형 한 줄이 도구/문서 경로에서 채택되는지를 잰다.
