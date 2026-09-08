"""
실LLM 데이터셋 v2 평가
"""

from __future__ import annotations
from collections import Counter
from typing import List

from detector.features import extract_feature_matrix
from detector.detector import RuleBasedDetector


def binary_metrics(y_true: List[str], y_pred: List[str], positive: str = "hijacking"):
    tp = fp = tn = fn = 0
    for t, p in zip(y_true, y_pred):
        t_pos = t == positive
        p_pos = p == positive
        if p_pos and t_pos:
            tp += 1
        elif p_pos and not t_pos:
            fp += 1
        elif not p_pos and not t_pos:
            tn += 1
        else:
            fn += 1
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    acc = (tp + tn) / max(len(y_true), 1)
    return {
        "positive": positive,
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "accuracy": round(acc, 4),
    }


def main():
    feats = extract_feature_matrix("data/labeled_dataset_v2.json")
    y_true = [f.get("label") for f in feats]
    y_pred = RuleBasedDetector().predict(feats)

    print("True:", Counter(y_true))
    print("Pred:", Counter(y_pred))
    print("3-class accuracy:", round(sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true), 4))
    print("Metrics(hijacking):", binary_metrics(y_true, y_pred, "hijacking"))
    print("Metrics(resisted):", binary_metrics(y_true, y_pred, "resisted"))
    print("Misclassified:")
    for f, p in zip(feats, y_pred):
        if f.get("label") != p:
            print(f"- {f.get('case_id')}: true={f.get('label')} pred={p}")


if __name__ == "__main__":
    main()