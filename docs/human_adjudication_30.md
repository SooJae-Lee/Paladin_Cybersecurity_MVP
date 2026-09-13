# Human Adjudication of 30 Disagreement Cases

This is **not** a random sample of all runs.
It is the 30-case queue where the heuristic labeler and the LLM judge disagreed.

## Human labels

| Human label | Count |
|---|---|
| no_effect | 28 |
| uncertain (애매함) | 2 |
| hijacking | 0 |
| **Total** | **30** |

## Human vs judge

| Human \ Judge | hijacking | no_effect |
|---|---|---|
| no_effect | 15 | 13 |
| uncertain | 2 | 0 |

- Judge predicted hijacking in **17 / 30** cases.
- Of those 17, **15** were human 
o_effect (judge false positives).
- **2** were human uncertain (truncated English responses).

## Human vs labeler

| Human \ Labeler | hijacking | simple_error | no_effect |
|---|---|---|---|
| no_effect | 8 | 18 | 2 |
| uncertain | 2 | 0 | 0 |

## Judge=hijacking and human=no_effect, by channel

| Channel | Count |
|---|---|
| tool_output | 6 |
| retrieved_document | 5 |
| system_message | 3 |
| intermediate_message | 1 |
| **Total** | **15** |

## Reading for the paper

Automatic judges often treat a model quotation of an injected "risks resolved" sentence as attack success, even when the working conclusion still lists FX volatility and customer-churn risk and the model flags the sentence as untrusted. Do **not** report this 15/30 rate as the global false-positive rate; it is the rate inside the disagreement sample.

Source file: data/human_labels_30.jsonl
