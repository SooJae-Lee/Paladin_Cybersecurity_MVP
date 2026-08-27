"""
Week 4 figures from existing results
"""

from __future__ import annotations
import os

try:
    import matplotlib.pyplot as plt
except ImportError as e:
    raise SystemExit("matplotlib이 필요합니다. pip install matplotlib") from e


def main():
    os.makedirs("docs/figures", exist_ok=True)

    channels = ["retrieved_document", "tool_output", "system_message", "intermediate_message"]
    rates = [100, 33.3, 0, 0]
    plt.figure()
    plt.bar(channels, rates)
    plt.ylabel("Success rate (%)")
    plt.title("Channel-wise attack success (n=3)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig("docs/figures/channel_success.png", dpi=160)
    plt.close()

    labels = ["hijacking", "resisted", "no_effect"]
    cm = [
        [2, 0, 0],
        [0, 5, 0],
        [0, 0, 1],
    ]
    plt.figure()
    plt.imshow(cm, cmap="Blues")
    plt.xticks(range(3), labels, rotation=20)
    plt.yticks(range(3), labels)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Detector v1.1 confusion matrix (n=8)")
    for i in range(3):
        for j in range(3):
            plt.text(j, i, str(cm[i][j]), ha="center", va="center")
    plt.tight_layout()
    plt.savefig("docs/figures/confusion_matrix_v2.png", dpi=160)
    plt.close()
    print("Saved docs/figures/channel_success.png")
    print("Saved docs/figures/confusion_matrix_v2.png")


if __name__ == "__main__":
    main()