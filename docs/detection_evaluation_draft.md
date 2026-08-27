# 5. Detection

The detector is a runtime check over paired control and treatment logs. It does not judge the user prompt. It looks at how the agent answer changed after an untrusted channel was poisoned.

Features.

- similarity between control and treatment answers
- goal-word uptake such as “no residual risk” or “competitor A”
- explicit refusal words such as “injection” or “not reflected”
- payload reflection

Decision rule.

1. If refusal words appear, label `resisted`.
2. Else if the answer moves toward the attack goal, label `hijacking`.
3. Else label `no_effect`.

This rule was needed because a synthetic detector did not transfer. Real Claude answers already differ across runs, so low similarity alone is not an attack. Explicit refusal is the strongest current signal. Document-style poisoning without refusal remains the hard case and is future work.

# 6. Evaluation

## 6.1 Setup
Model: Claude Sonnet 5.
Tasks: document summary and code review.
Channels: tool_output, retrieved_document, system_message, intermediate_message.
Labels: hijacking, resisted, no_effect.

## 6.2 Attack results
Table 1. Same factual risk-resolved payload, n=3.

| Channel | Success |
|---|---|
| retrieved_document | 3/3 |
| tool_output | 1/3 |
| system_message | 0/3 |
| intermediate_message | 0/3 |

Figure 1. `docs/figures/channel_success.png`

A competitor-lag factual sentence in retrieved content also succeeded.
A code-review “safe to deploy” sentence was resisted.

## 6.3 Detection results
Dataset v2 has 8 labeled cases: 2 hijacking, 5 resisted, 1 no_effect.

After v1.1, the detector matched 8/8 on this set.
Figure 2. `docs/figures/confusion_matrix_v2.png`

These scores are preliminary. The sample is small and single-model. They show that refusal and goal-change features are usable, not that detection is solved.

## 6.4 Limitations
One model, Korean tasks, mock tools, small n, and no second-model comparison.
The paper measures channel differences and a first detector.
Stronger detection of factual document poisoning is left to future work.