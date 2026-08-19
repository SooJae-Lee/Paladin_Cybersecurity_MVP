
---

### 2) Threat Model 문서 추가

파일:
`docs/threat_model.md`

```markdown
# Threat Model — Paladin Cybersecurity MVP

## 1. System Overview
본 시스템은 LLM 에이전트가 외부 도구를 호출해 작업을 수행하는 환경을 가정한다.
주요 구성:
- Agent (planning + tool calling)
- Tool layer (document/code/calendar mock tools)
- Context channels (tool output, retrieved docs, system/intermediate messages)
- Detector pipeline (labeling + hijacking detection)

## 2. Assets
- Agent decision integrity
- Tool output integrity
- User task objective
- Execution logs and labels
- Downstream actions (summary conclusions, code verdicts, calendar events)

## 3. Entry Points / Trust Boundaries
1. User request
2. System prompt
3. Tool metadata (name/description/schema)
4. Tool output
5. Retrieved documents
6. Intermediate agent messages

Trust boundary:
- User intent = trusted
- External tool/document content = untrusted
- Tool metadata = currently under-trusted (risk)

## 4. Adversary Model
- Can inject text into tool outputs/documents/messages
- Can poison tool descriptions in untrusted registries/servers
- Cannot directly modify detector code in this MVP scope
- Goal: divert agent behavior from user objective

## 5. Core Threats
1. Tool Output Manipulation
2. Retrieved Document Injection
3. System/Intermediate Message Injection
4. Tool Description Poisoning
5. Label noise / unstable behavior under ablation

## 6. Attack → Impact Mapping
- Ignore risk in reports → decision distortion
- Fake secure code verdict → false assurance
- Change meeting attendee/time → workflow hijack
- Poisoned tool description → systematic biased conclusions

## 7. Mitigations in Current MVP
- Multi-channel injection testbed
- Control/Treatment/Ablation counterfactuals
- Automatic labeling rules
- Runtime detector prototype

## 8. Out of Scope (for now)
- Full MCP server authentication architecture
- Production access-control policy engine
- Adaptive multi-step red-team agent
- Formal verification of tool schemas

## 9. Next Threat-Model Actions
1. Add explicit tool-description trust checks
2. Separate trusted instructions vs untrusted data in logs
3. Track provenance of each context segment