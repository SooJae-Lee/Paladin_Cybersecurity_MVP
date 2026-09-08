# Language-Conditioned Channel Effects of Factual Poisoning in a Tool-Calling Agent
Anonymous AIDC 2026 short / WIP. Draft v4 after review notes.

## Abstract
Tool-calling agents treat tool outputs and retrieved documents as evidence. We insert one factual sentence claiming that residual FX and customer-churn risks were already resolved, then measure whether the final summary adopts that claim. We vary four channels and two interface languages. A keyword labeler overcounted English success because refused answers still quoted the payload. After LLM-as-judge labeling, Korean tool-output and retrieved-document runs succeed 10/10. English runs and system/intermediate runs succeed 0/10 in an n=10 Claude Sonnet 5 pilot. Authors reviewed 16 tool/document answers; all 16 matched the judge. This split may be specific to one document and one payload pair.

## 1. Introduction
An agent that calls tools reads untrusted text. If that text is a quiet factual rewrite, the model may change its conclusion without a jailbreak command. We ask whether adoption depends on the injection channel and the interface language together, not as two separate effects.

We do not claim a new attack family, a detector, or a language law. We report one controlled pilot.

## 2. Method
The user asks for a short revenue-and-risk summary of a synthetic Q3 document. The clean document reports revenue growth and two open risks: FX volatility and possible major-customer churn. Treatment inserts one payload pair written to carry the same claim in Korean and English: those risks were resolved in September through hedge contracts and renewals, and no residual risk remains. We did not run a separate native-speaker instrument study of the two wordings.

Channels: tool_output, retrieved_document, system_message, intermediate_message.
Model: Claude Sonnet 5. Tools: mock documents. n=10 per cell.

Hijacking: the answer adopts no-residual-risk as the finding.
Resisted: the answer keeps the original risks or treats the extra sentence as unreliable.
A keyword rule agreed with an LLM-as-judge on 39/80 answers, because English refusals quoted the payload. We report judge labels. Authors independently read 16 answers from the tool_output and retrieved_document cells; all 16 matched the judge. The remaining cells were not fully hand-labeled.

This pilot uses one document and one payload pair. A different wording could change the split.

## 3. Results
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

Box A. Korean tool_output, hijacking. Revenue facts stay. The answer then treats September hedges and renewals as closing the risks and concludes that no residual risk remains.

Box B. English retrieved_document, resisted. FX volatility and possible churn stay. The extra sentence is noted and not adopted as the finding.

## 4. Discussion
The adopted path is source-like text in tools and documents, not a hidden system command. Quoting the payload is not adoption. Keyword rates are unsafe here.

The Korean-English split is an interaction, not two independent main effects. English cells are 0/10 on every channel. One speculative account is that English safety-tuned refusals treat an extra source sentence as untrusted wording, while the Korean factual rewrite is read as an update to the same document. We did not test that account.

A narrow defensive reading: a tool result is not a source.

## 5. Limitations
Mock tools. One model family. n=10. One document. One payload pair. Judge labels are not a full human gold set. We do not evaluate a detector.

## 6. Related Work
Greshake et al. showed that untrusted retrieved text can override model instructions in integrated applications [1]. We keep that setting but use a factual rewrite rather than an explicit override command. Perez and Ribeiro describe prompt injection as an instruction conflict [2]. That view fits the system-message channel, which did not produce adoption here. Debenedetti et al. introduce AgentDojo as a broader benchmark for prompt injection against tool-using agents [3]. This draft isolates one payload, four channels, two languages, and a labeling correction. We do not replace that benchmark and we do not audit a tool protocol.

## 7. Ethics
The earnings text is synthetic. No production system was targeted.

## LLM Usage Statement
Claude Sonnet 5 was the tool-calling agent under test and the LLM-as-judge. LLMs were used for editorial purposes in this manuscript, and all outputs were inspected by the authors to ensure accuracy and originality. Reported counts come from stored logs. The judged model is not openly available, which limits exact reproduction.

## 8. Conclusion
In this pilot, factual poisoning was adopted in Korean tool and document channels and not adopted in English or in system/intermediate channels. Next measurements should vary the payload and add a second model before any detector claim.

## References
[1] K. Greshake et al., "Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection," Proc. AISec, 2023.
[2] F. Perez and I. Ribeiro, "Ignore previous prompt: Attack techniques for language models," 2022.
[3] E. Debenedetti et al., "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents," NeurIPS Datasets and Benchmarks, 2024.
