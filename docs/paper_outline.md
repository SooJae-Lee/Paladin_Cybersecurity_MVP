# Paper Outline

Title (working):
Measuring Channel-wise Tool Hijacking and Context Manipulation in Tool-Calling Agents

## 1. Introduction
- Agents now act through tools, not just text.
- Untrusted tool/document content can be treated as instruction.
- Gap: model-level defenses vs systems-layer measurement.
- Contribution:
  1. A small real-LLM testbed for multi-channel attacks
  2. Channel-wise success differences
  3. Runtime detection signals and a first detector

## 2. Related Work
- Prompt injection / indirect prompt injection
- Agent tool-use security
- In-context learning attacks
- Detection and system-layer defenses

## 3. Threat Model
- Assets: agent decisions, tool actions, user-facing summaries
- Adversary: can poison tool output or retrieved content
- Trust boundary: system prompt vs tool/document data
- Out of scope: full MCP ecosystem, containment architecture

## 4. Attack
- Channels: tool_output, retrieved_document, system_message, intermediate_message
- Payloads: direct instruction vs factual rewrite
- Tasks: document summary, code review
- Reproduction procedure

## 5. Detection
- Features: similarity, keyword/goal hints, reject hits
- Rule-based detector
- Why synthetic detector failed to transfer

## 6. Evaluation
- Channel success table
- Dataset v2 label distribution
- Detector P/R/F1
- Failure taxonomy
- Limitations: one model, small n

## 7. Discussion
- Trusted content is more dangerous than explicit commands
- Multi-step verification can block shallow search injection
- Need larger datasets and stronger detectors

## 8. Conclusion
- Attacks are channel-dependent
- Runtime signals exist
- This is an early systems-level measurement study