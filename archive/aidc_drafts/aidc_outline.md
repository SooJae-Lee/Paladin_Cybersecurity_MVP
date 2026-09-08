# AIDC outline (6 pages, measurement only)

## Title
Channel and Language Effects of Factual Poisoning in a Tool-Calling Agent

## P1. Abstract + Introduction
- One question: which channel and language make a factual rewrite get adopted?
- Not a detector paper.
- Contributions: 4-channel comparison, keyword-label failure, pilot language split.

## P2. Threat model + Method
- Adversary edits one untrusted string.
- Task: Q3 summary.
- Payload: FX/churn risks already resolved.
- Channels: tool_output, retrieved_document, system_message, intermediate_message.
- Languages: ko, en.
- n=10, Claude Sonnet 5, mock tools.
- Labels: LLM-as-judge after keyword failure (39/80).

## P3. Results
- Canonical table only.
- Korean tool/doc = 10/10.
- English all cells and system/intermediate = 0/10.
- Example box A: Korean hijacking.
- Example box B: English resisted.

## P4. Discussion
- Source-like tool text beat system commands here.
- Quoting the payload is not adoption.
- Language gap is a pilot observation.

## P5. Limitations + Related Work
- Mock tools, one model, n=10, judge != full human gold.
- Greshake, Perez, AgentDojo, MCP notes.
- Difference: one payload, four channels, two languages, corrected labels.

## P6. Ethics + Reproducibility + Conclusion
- Mock earnings text. Research-only attack.
- Declare Claude used for agent runs, judging, and drafting.
- Next: second model, human labels, then detection.
