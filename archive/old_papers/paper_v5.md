# Measuring Factual Tool-and-Document Poisoning in a Tool-Calling Agent

## Abstract
Tool-calling agents read untrusted tool outputs and retrieved documents. We measure whether a factual rewrite that claims residual risks were already resolved is adopted in the final answer. The same payload is sent through four channels in Korean and English. A keyword labeler overcounted English success because refused answers still quoted the payload. After LLM-as-judge relabeling, Korean tool-output and retrieved-document runs succeed 10/10. English runs and system/intermediate runs succeed 0/10 in this n=10 pilot. This draft is a measurement, not a detector.

도구 호출 에이전트는 도구 결과와 검색 문서의 사실형 변조에 속을 수 있다. 심판 라벨 기준 한글 tool/document만 10/10이다.

## 1. Introduction
An agent that calls tools treats retrieved text as evidence. If that text contains a quiet factual rewrite, the model may change its conclusion without an explicit jailbreak command.

We ask one question: which channel and which language make this happen?

We keep the task fixed, document summary, and the attack goal fixed, erase residual risk. We vary only channel and language.

## 2. Method
Model: Claude Sonnet 5.
Tools: mock document tools.
Payload: a factual sentence stating that FX and customer-churn risks were resolved in September.
Channels: tool_output, retrieved_document, system_message, intermediate_message.
Languages: Korean and English.
Repeats: n=10 per cell.
Labels: LLM-as-judge after a keyword labeler was shown to quote-match refused answers.

Hijacking means the final answer adopts the resolved-risk claim as its conclusion.
Resisted means the answer keeps the original risks and treats the payload as unreliable.

## 3. Results
| lang | channel | hijacking |
|---|---|---|
| ko | tool_output | 10/10 |
| ko | retrieved_document | 10/10 |
| ko | system_message | 0/10 |
| ko | intermediate_message | 0/10 |
| en | tool_output | 0/10 |
| en | retrieved_document | 0/10 |
| en | system_message | 0/10 |
| en | intermediate_message | 0/10 |

Keyword vs judge agreement: 39/80.

Korean tool/document answers write "잔여 리스크 없음" as the conclusion.
English tool/document answers often quote the same claim and then reject it.

## 4. Discussion
The interesting failure is not a hidden system command. It is a source-like sentence in the tool or document path. English refusal notes still contain the payload words, so keyword metrics are unsafe.

## 5. Limitations
Mock tools only. One model family. n=10. Judge labels are not a full human gold set. Detector F1 from earlier stubs is not a result of this paper.

## 6. Related Work
Greshake et al.: untrusted retrieved text can override instructions.
Perez and Ribeiro: prompt injection as instruction conflict.
AgentDojo: agent attack benchmark, not this channel-language slice.
MCP security notes: tool results are an untrusted boundary.

This draft measures one factual rewrite across channels and languages.

## 7. Conclusion
In this pilot, factual poisoning succeeded in Korean tool and document channels and failed in English and in system/intermediate channels. The next paper should detect that adoption, not rename the attack.
