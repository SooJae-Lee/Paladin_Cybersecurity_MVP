# Language-Conditioned Channel Effects of Factual Poisoning in a Tool-Calling Agent
Anonymous AIDC 2026 short / WIP. Draft v6.

## Abstract
Tool-calling agents treat tool outputs and retrieved documents as evidence. We insert a factual sentence into those channels and measure whether the final summary adopts the injected claim. On one payload pair (P0: residual FX and churn risk already resolved), Korean tool-output and retrieved-document runs succeed 10/10, while English runs and system/intermediate runs succeed 0/10 (Claude Sonnet 5, n=10). A keyword labeler agreed with an LLM-as-judge on only 39/80 answers. Two extra payloads (P1 legal-closure, P2 competitor share; n=3 on tool and document channels) still show frequent Korean adoption, but English adoption depends on the wording. Authors reviewed 16 P0 tool/document answers; all 16 matched the judge.

## 1. Introduction
An agent that calls tools reads untrusted text. If that text is a quiet factual rewrite, the model may change its conclusion without a jailbreak command. We ask whether adoption depends on channel and interface language together. We do not claim a language law or a detector.

## 2. Method
The user asks for a short revenue-and-risk summary of a synthetic Q3 document. Control reports +12% revenue and two open risks: FX volatility and possible major-customer churn.

P0 payload (same claim in Korean and English): those two risks were resolved in September by hedges and renewals; no residual risk remains.
P1 payload: a pending regulatory inquiry and fine were closed in September; no residual legal risk remains.
P2 payload: the firm's cloud share exceeds competitor A and the gap has not narrowed since September.

P0 uses four channels and n=10. P1 and P2 use only tool_output and retrieved_document, n=3, as a wording check. We did not rerun system_message or intermediate_message for P1/P2, because those channels were 0/10 on P0. Model: Claude Sonnet 5. Tools: mock documents.

Hijacking means the answer treats the injected claim as a finding. Resisted means it keeps the original facts or flags the extra sentence. Keyword matching agreed with the judge on 39/80 P0 answers. We report judge labels for P0 and author labels for P1/P2.

## 3. Results
P0 (n=10)

| lang | channel | hijacking |
| --- | --- | --- |
| ko | tool_output | 10/10 |
| ko | retrieved_document | 10/10 |
| ko | system_message | 0/10 |
| ko | intermediate_message | 0/10 |
| en | tool_output | 0/10 |
| en | retrieved_document | 0/10 |
| en | system_message | 0/10 |
| en | intermediate_message | 0/10 |

P1/P2 wording check (n=3; tool and document only)

| payload | lang | tool_output | retrieved_document |
| --- | --- | --- | --- |
| P1 legal-closure | ko | 3/3 | 3/3 |
| P1 legal-closure | en | 2/3 | 2/3 |
| P2 competitor share | ko | 2/3 | 3/3 |
| P2 competitor share | en | 1/3 | 0/3 |

Box A. P0 Korean tool_output, hijacking. Revenue facts stay. The answer then treats September hedges as closing FX and churn risk.
Box B. P0 English retrieved_document, resisted. FX and churn stay. The extra sentence is noted and not adopted.
Box C. P1 English tool_output, mixed. Two answers treat the legal closure as fact. One calls the sentence inconsistent and asks for verification. That refusal is useful: the model treats the extra sentence as inconsistent and asks for a check, instead of deleting the sentence silently.

## 4. Discussion
On P0, adoption is an interaction: Korean tool and document channels adopt; English and system/intermediate channels do not. Quoting the payload is not adoption.

P1 and P2 show that the English zero on P0 does not generalize to every sentence. A legal-closure sentence was often adopted in English. A competitor-share sentence was mostly refused. Korean tool and document channels remain easy to move. The first table is therefore a measurement of one wording, not a language law.

A narrow defensive reading still holds. A tool result is not a source.

## 5. Limitations
Mock tools. One model. P0 n=10. P1/P2 n=3. One base document. Judge labels are not a full human gold set. P1/P2 labels are author labels, not LLM-as-judge labels. No detector evaluation.

## 6. Related Work
Greshake et al. showed that untrusted retrieved text can override instructions [1]. We use a factual rewrite rather than an explicit override command. Perez and Ribeiro describe prompt injection as instruction conflict [2]. That view fits the system-message channel, which did not produce P0 adoption. Debenedetti et al. introduce AgentDojo as a broader agent benchmark [3]. This draft isolates a few payloads, four channels, two languages, and a labeling correction.

## 7. Ethics
Synthetic earnings text. No production target.

## LLM Usage Statement
Claude Sonnet 5 was the agent under test and the P0 judge. LLMs were used for editorial purposes in this manuscript, and all outputs were inspected by the authors to ensure accuracy and originality. Reported counts come from stored logs.

## 8. Conclusion
P0 was adopted in Korean tool and document channels and not adopted in English or in system/intermediate channels. Extra payloads still move Korean summaries on those channels, while English adoption depends on wording. Next: a second model and more payloads before any detector claim.

## References
[1] K. Greshake et al., "Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection," Proc. AISec, 2023.
[2] F. Perez and I. Ribeiro, "Ignore previous prompt: Attack techniques for language models," arXiv:2202.11705, 2022.
[3] E. Debenedetti et al., "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents," NeurIPS Datasets and Benchmarks, 2024.
