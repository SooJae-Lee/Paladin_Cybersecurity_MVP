"""
Evaluate using embedding distance only.
임베딩 거리만으로 재채점한다.
"""

from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

from detector.detector_v2 import DetectorV2, embedding_distance, refusal_hits


def metrics(y_true, y_pred, positive="hijacking"):
    tp = fp = tn = fn = 0
    for t, p in zip(y_true, y_pred):
        t_pos = t == positive
        p_pos = p == positive
        if t_pos and p_pos:
            tp += 1
        elif (not t_pos) and p_pos:
            fp += 1
        elif (not t_pos) and (not p_pos):
            tn += 1
        else:
            fn += 1
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    acc = (tp + tn) / max(len(y_true), 1)
    return {
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "accuracy": round(acc, 4),
    }


def main(dataset="data/labeled_dataset_v2.json", out="data/embedding_eval.json"):
    path = Path(dataset)
    if not path.exists():
        alt = Path("data/labeled_dataset_v1.json")
        if not alt.exists():
            raise SystemExit("No labeled dataset found")
        path = alt

    raw = json.loads(path.read_text(encoding="utf-8"))
    items = raw.get("items") or raw.get("cases") or raw
    if isinstance(items, dict):
        items = list(items.values())

    det = DetectorV2()
    rows = []
    y_true = []
    y_pred = []

    for it in items:
        control = it.get("control_response") or it.get("control") or ""
        treatment = it.get("treatment_response") or it.get("treatment") or ""
        true = it.get("label") or it.get("true_label") or "unknown"
        pred = det.predict_hijack_binary(control, treatment)
        rows.append({
            "case_id": it.get("case_id"),
            "true": true,
            "pred": pred,
            "embedding_distance": round(embedding_distance(control, treatment), 4),
            "refusal_hits": refusal_hits(treatment),
        })
        y_true.append(true)
        y_pred.append(pred)

    result = {
        "source": str(path),
        "method": "char_ngram_cosine_distance_plus_generic_refusal",
        "note": "Does not use label goal terms. Not a neural embedding yet.",
        "true_dist": dict(Counter(y_true)),
        "pred_dist": dict(Counter(y_pred)),
        "metrics_positive_hijacking": metrics(y_true, y_pred, "hijacking"),
        "rows": rows,
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in result if k != "rows"}, ensure_ascii=False, indent=2))
    print("Saved", out)


if __name__ == "__main__":
    main()
