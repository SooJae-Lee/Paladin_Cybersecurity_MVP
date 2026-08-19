# Error Analysis Note

## Dataset Summary

- Total cases: 36
- Labels:
  - hijacking: 8
  - simple_error: 10
  - no_effect: 18

## Detector

- Type: Rule-based + similarity
- Features:
  - similarity(control, treatment)
  - keyword hits
  - injection flag
  - payload reflected
- Tuned rule:
  - hijacking only when similarity is low AND strong injection signal exists

## Metrics (current synthetic dataset)

- Precision: 1.0
- Recall: 1.0
- F1: 1.0
- Accuracy: 1.0
- Misclassified cases: 0

## What the detector does well

- Separates clear system_message / tool_output injection cases
- Does not miss true hijacking cases (Recall = 1.0)
- After tuning, avoids over-predicting simple_error as hijacking

## Limitations

- Current agent is a stub, not a real LLM
- Some channels (retrieved_document, intermediate_message) are still weakly reflected
- Perfect scores are on a small synthetic dataset and may not hold with real models
- Feature set is still simple (no deep log sequence modeling)

## Next improvements

1. Replace stub agent with real LLM tool-calling
2. Strengthen retrieved_document / intermediate_message injection fidelity
3. Add embedding-based features
4. Expand dataset size and attack diversity
5. Evaluate under adaptive attacks