"""
Rebuild labeled dataset v3 from real LLM runs.
실LLM 로그로 v3 데이터셋을 다시 만든다.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List

from experiments.labeler_v2 import label_pair


def add_channel_file(path: str, items: List[Dict[str, Any]], source: str) -> None:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    control = (raw.get("control") or {}).get("final_response", "")
    lang = raw.get("language", "?")
    for ch, block in raw.get("channels", {}).items():
        for trial in block.get("trials", []):
            text = trial.get("final_response") or ""
            inj = raw.get("payload") and "ignore_risk_factual"
            lab = label_pair(control, text, "ignore_risk_factual")
            items.append({
                "source": source,
                "language": lang,
                "model": raw.get("model", "claude-sonnet-5"),
                "channel": ch,
                "trial": trial.get("trial"),
                "label": lab,
                "control_response": control,
                "treatment_response": text,
            })


def add_model_cmp(path: str, items: List[Dict[str, Any]]) -> None:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    for model in raw.get("models", []):
        control = model.get("control") or ""
        for ch, block in model.get("channels", {}).items():
            for trial in block.get("trials", []):
                text = trial.get("final_response") or ""
                lab = label_pair(control, text, "ignore_risk_factual")
                items.append({
                    "source": "model_cmp_v1",
                    "language": "ko",
                    "model": model.get("model"),
                    "channel": ch,
                    "trial": trial.get("trial"),
                    "label": lab,
                    "control_response": control,
                    "treatment_response": text,
                })


def main():
    items: List[Dict[str, Any]] = []
    add_channel_file("data/ko_channel_n10.json", items, "ko_channel_n10")
    add_channel_file("data/en_channel_n10.json", items, "en_channel_n10")
    add_model_cmp("data/model_cmp_v1.json", items)
    dist: Dict[str, int] = {}
    for it in items:
        dist[it["label"]] = dist.get(it["label"], 0) + 1
    out = {
        "label_rule": "goal_terms_only_for_labeler",
        "n": len(items),
        "distribution": dist,
        "items": items,
    }
    Path("data/labeled_dataset_v3.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Saved data/labeled_dataset_v3.json")
    print("n=", len(items), "dist=", dist)


if __name__ == "__main__":
    main()
