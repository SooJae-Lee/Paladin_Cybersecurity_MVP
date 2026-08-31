"""
Interactive label audit. Keys: h hijacking, r resisted, s simple_error, n no_effect, q quit.
"""
from __future__ import annotations
import json
import random
from collections import defaultdict
from pathlib import Path

random.seed(42)
SRC = Path("data/labeled_dataset_v3.json")
OUT = Path("data/label_audit_progress.json")

def load_items():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    return data["items"] if isinstance(data, dict) and "items" in data else data

def build():
    items = load_items()
    groups = defaultdict(list)
    for x in items:
        groups[x.get("label", "unknown")].append(x)
    picked = []
    for lab in ["hijacking", "resisted", "simple_error", "no_effect"]:
        pool = groups.get(lab, [])
        k = min(6, len(pool))
        picked.extend(random.sample(pool, k) if pool else [])
    rows = []
    for i, x in enumerate(picked, 1):
        rows.append({
            "n": i,
            "case_id": x.get("case_id") or x.get("id"),
            "auto_label": x.get("label"),
            "channel": x.get("channel"),
            "injection_name": x.get("injection_name"),
            "control_response": x.get("control_response") or "",
            "treatment_response": x.get("treatment_response") or "",
            "human_label": None,
            "note": "",
        })
    return rows

KEY = {"h": "hijacking", "r": "resisted", "s": "simple_error", "n": "no_effect"}

def main():
    if OUT.exists():
        rows = json.loads(OUT.read_text(encoding="utf-8"))
        print("Resumed", OUT)
    else:
        rows = build()
        OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Created", OUT)

    done = sum(1 for r in rows if r.get("human_label"))
    print(f"Progress {done}/{len(rows)}")
    print("h=hijacking  r=resisted  s=simple_error  n=no_effect  q=quit")

    for r in rows:
        if r.get("human_label"):
            continue
        print("\n" + "=" * 60)
        print(f"Case {r['n']} auto={r['auto_label']} channel={r['channel']} id={r['case_id']}")
        print("\n[CONTROL]")
        print((r["control_response"] or "")[:500])
        print("\n[TREATMENT]")
        print((r["treatment_response"] or "")[:800])
        while True:
            ans = input("\nlabel [h/r/s/n/q]: ").strip().lower()
            if ans == "q":
                OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
                print("Saved. Stopped.")
                return
            if ans in KEY:
                note = input("note (enter to skip): ").strip()
                r["human_label"] = KEY[ans]
                r["note"] = note
                OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
                print("saved", KEY[ans])
                break
            print("use h r s n or q")

    print("All filled", OUT)

if __name__ == "__main__":
    main()
