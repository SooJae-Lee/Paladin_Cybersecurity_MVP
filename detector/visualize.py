"""
Confusion Matrix 시각화
"""

from __future__ import annotations
import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from detector.features import extract_feature_matrix
from detector.detector import RuleBasedDetector


def plot_confusion_matrix(
    y_true,
    y_pred,
    labels=("hijacking", "simple_error", "no_effect"),
    save_path="data/confusion_matrix.png",
):
    label_to_idx = {l: i for i, l in enumerate(labels)}
    n = len(labels)
    cm = np.zeros((n, n), dtype=int)

    for t, p in zip(y_true, y_pred):
        if t in label_to_idx and p in label_to_idx:
            cm[label_to_idx[t], label_to_idx[p]] += 1

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)

    ax.set(
        xticks=np.arange(n),
        yticks=np.arange(n),
        xticklabels=labels,
        yticklabels=labels,
        ylabel="True label",
        xlabel="Predicted label",
        title="Confusion Matrix",
    )
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # 숫자 표시
    thresh = cm.max() / 2 if cm.max() > 0 else 0.5
    for i in range(n):
        for j in range(n):
            ax.text(
                j, i, format(cm[i, j], "d"),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black",
            )

    fig.tight_layout()
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Saved confusion matrix to: {save_path}")
    return cm


def main():
    feats = extract_feature_matrix("data/labeled_dataset_v1.json")
    y_true = [f["label"] for f in feats]
    y_pred = RuleBasedDetector().predict(feats)

    print("True :", Counter(y_true))
    print("Pred :", Counter(y_pred))
    plot_confusion_matrix(y_true, y_pred)


if __name__ == "__main__":
    main()