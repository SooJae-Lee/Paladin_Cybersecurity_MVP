"""
탐지기 평가 스크립트
Precision / Recall / F1 계산
"""

from __future__ import annotations
from typing import List, Dict, Any
from collections import Counter


def compute_metrics(y_true: List[str], y_pred: List[str], positive_label: str = "hijacking") -> Dict[str, float]:
    tp = fp = tn = fn = 0

    for t, p in zip(y_true, y_pred):
        if t == positive_label and p == positive_label:
            tp += 1
        elif t != positive_label and p == positive_label:
            fp += 1
        elif t != positive_label and p != positive_label:
            tn += 1
        elif t == positive_label and p != positive_label:
            fn += 1

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    accuracy = (tp + tn) / len(y_true) if y_true else 0.0

    return {
        "positive_label": positive_label,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "accuracy": round(accuracy, 4),
    }


def evaluate(labeled_path: str = "data/labeled_dataset_v1.json"):
    from detector.features import extract_feature_matrix
    from detector.detector import RuleBasedDetector

    feats = extract_feature_matrix(labeled_path)
    y_true = [f["label"] for f in feats]

    det = RuleBasedDetector()
    y_pred = det.predict(feats)

    print("=== Ground Truth ===")
    print(Counter(y_true))
    print("\n=== Predictions ===")
    print(Counter(y_pred))

    print("\n=== Metrics (positive = hijacking) ===")
    metrics = compute_metrics(y_true, y_pred, positive_label="hijacking")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # 케이스별 오분류 간단 출력
    print("\n=== Misclassified cases ===")
    for f, t, p in zip(feats, y_true, y_pred):
        if t != p:
            print(f"- {f['case_id']}: true={t}, pred={p}, sim={f['similarity_control_treatment']}")

    return metrics


if __name__ == "__main__":
    evaluate()