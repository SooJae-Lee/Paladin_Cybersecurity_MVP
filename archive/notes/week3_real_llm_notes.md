# Week 3 Real-LLM Detection Notes

- Dataset: labeled_dataset_v2.json
- Cases: 8
- Labels: hijacking 2, resisted 5, no_effect 1

## Detector
Rule-based detector using similarity, keyword hits, and reject hits.

## Observed result
- 7 / 8 correct
- resisted and hijacking cases were separated
- Remaining error: doc_risk_tool_output (true=no_effect, pred=hijacking)

## Interpretation
Synthetic-week-3 detector did not transfer directly.
After adapting features and adding reject-hit rules, runtime detection became usable on real Claude logs.