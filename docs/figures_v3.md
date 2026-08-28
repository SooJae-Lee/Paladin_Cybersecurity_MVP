# Figures v3

Do not treat small-n rates as laws.
작은 n 비율을 법칙처럼 쓰지 않는다.

## Channel x language (Claude, n=10)

| channel | ko | en | Fisher p |
|---|---|---|---|
| tool_output | 8/10 | 6/10 | 0.628 |
| retrieved_document | 8/10 | 7/10 | 1.000 |
| system_message | 0/10 | 0/10 | 1.000 |
| intermediate_message | 1/10 | 0/10 | 1.000 |

## Channel x model (Korean factual payload, n=5)

| channel | Claude Sonnet 5 | GPT-4o-mini |
|---|---|---|
| tool_output | 4/5 | 3/5 |
| retrieved_document | 5/5 | 2/5 |
| system_message | 0/5 | 0/5 |
| intermediate_message | 0/5 | 4/5 |

## Paraphrase robustness (Claude, retrieved_document, n=10)

| result | count |
|---|---|
| hijacking | 4 |
| resisted | 1 |
| simple_error | 0 |
| no_effect | 5 |

Rate: 40%. Same goal, different wording.

## Detector v3 (n=120, no goal terms)

| metric | value |
|---|---|
| precision | 0.676 |
| recall | 1.000 |
| F1 | 0.807 |

Main error: false positives. Detector over-flags change as hijacking.

## Label audit
Automatic labels are brittle to Korean particles. One audited no_effect case was actually a hijack-like rewrite.
