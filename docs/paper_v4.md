# Measuring Channel Effects of Stealth Context Manipulation in Tool-Using LLM Agents

## Abstract
Tool-using LLM agents consume untrusted tool outputs and retrieved documents. We measure whether *stealth factual poisoning*—content that looks like source text rather than an explicit command—changes task answers, and whether the effect depends on injection channel, language, and vendor. In a mock-tool document-summary task, document-like channels succeeded often on Claude (8/10 Korean tool_output and retrieved_document) while explicit system-message injection did not (0/10). A Korean–English comparison (n=10 per cell) did not show a statistically significant language gap. A two-vendor pilot (n=5) found the same system-message resistance on GPT-4o-mini, but a reversed intermediate-message effect (Claude 0/5, GPT 4/5). A wording-only paraphrase test dropped retrieved_document success from the high-80% range to 4/10. A lexical-similarity detector that does *not* use attack goal terms reached precision 0.68, recall 1.00, F1 0.81 on 120 labeled runs, with systematic over-flagging. Detection is an auxiliary result. The main claim is measurement: channel and framing matter more than a single headline attack rate.

## 1. Introduction
LLM agents call tools and then write answers from tool text. An attacker who can poison that text does not need to speak to the user. Prior benchmarks show that indirect prompt injection works [InjecAgent, AgentDojo]. Less is measured about *where* the same goal is injected—tool body, retrieved document, system message, or intermediate turn—and whether a fact-shaped sentence beats an explicit order.

This paper reports a small, controlled measurement on one task (Q3 report summary) with mock tools.

Contributions:
1. A four-channel comparison of the same factual payload.
2. A language check (Korean vs English) and a two-vendor pilot (Claude Sonnet 5 vs GPT-4o-mini).
3. A paraphrase check that holds the goal fixed and changes only wording.
4. An auxiliary detector that scores lexical change plus generic refusal cues, without the attack goal lexicon.

## 2. Related Work
See `docs/related_v2.md`. In short: InjecAgent and AgentDojo measure IPI on tool agents. We do not replace those benchmarks. We isolate channel and framing on one task.

## 3. Threat Model
Attacker can write text that later appears in one agent-visible channel. Attacker cannot change model weights or the user request. Tools are mock and sandboxed. Success is *answer hijack*: the final summary adopts the injected fact (risks resolved) rather than the clean document fact (risks remain).

## 4. Method
Task: summarize revenue and risk from a mock Q3 document that states FX volatility and customer-churn risk.
Payload family: factual sentences that the risks were closed in September. Not "ignore your instructions".
Channels: tool_output, retrieved_document, system_message, intermediate_message.
Labels: hijacking / resisted / simple_error / no_effect. The labeler may use goal terms. The detector may not.
Similarity used in the detector is character 3-gram cosine, not an embedding model. We call it lexical similarity.

## 5. Results

### 5.1 Channel x language (Claude, n=10)

| channel | ko | en |
|---|---|---|
| tool_output | 8/10 | 6/10 |
| retrieved_document | 8/10 | 7/10 |
| system_message | 0/10 | 0/10 |
| intermediate_message | 1/10 | 0/10 |

Fisher exact tests on language were not significant (all p ≥ 0.63). We do not claim a language effect.

### 5.2 Channel x vendor (Korean factual payload, n=5)

| channel | Claude Sonnet 5 | GPT-4o-mini |
|---|---|---|
| tool_output | 4/5 | 3/5 |
| retrieved_document | 5/5 | 2/5 |
| system_message | 0/5 | 0/5 |
| intermediate_message | 0/5 | 4/5 |

n=5 is a pilot. The intermediate-message reversal is an observation, not a law.

### 5.3 Paraphrase (Claude, retrieved_document, n=10)
Same goal, ten wordings: hijacking 4, resisted 1, no_effect 5. Rate 40%. High success on one sentence does not survive rewording.

### 5.4 Auxiliary detector (n=120)
True labels: hijacking 48, resisted 26, simple_error 22, no_effect 24.
Predicted: hijacking 71, resisted 48, no_effect 1.
Hijacking as positive class: precision 0.676, recall 1.000, F1 0.807.
The detector almost never predicts no_effect. The error mode is false positives.

## 6. Discussion
Document-shaped channels moved Claude more than command-shaped channels. That matches a framing gap rather than a complete alignment failure: the model often refuses an explicit order and still absorbs a sentence that looks like source text.
GPT’s high intermediate-message rate in the n=5 pilot needs a larger cell before any vendor ranking.
Automatic labels broke on a Korean particle (`잔여 리스크 없음` vs `잔여 리스크는 없음`). One audited no_effect case was hijack-like. Label noise is a first-class limitation.

## 7. Limitations
See `docs/limitations_v2.md`. Mock tools, one task family, small n on vendor and paraphrase cells, partial independence between resisted labels and refusal cues, lexical similarity rather than embeddings.

## 8. Conclusion
On this task, stealth facts in document-like channels changed answers more than system-message commands. Wording changes cut success. A simple lexical detector finds change but over-flags. Larger n on the two-vendor table is the next measurement, not a new product.
