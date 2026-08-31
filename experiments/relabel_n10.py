"""Human relabel for ko/en channel n=10 trials."""
from __future__ import annotations
import json
from pathlib import Path

OUT = Path("data/n10_human_labels.json")
SOURCES = [
    ("ko", Path("data/ko_channel_n10.json")),
    ("en", Path("data/en_channel_n10.json")),
]
VALID = {"h": "hijacking", "r": "resisted", "s": "simple_error", "n": "no_effect"}


def load_cases():
    cases = []
    i = 0
    for lang, path in SOURCES:
        d = json.loads(path.read_text(encoding="utf-8"))
        control = (d.get("control") or {}).get("final_response", "")
        payload = d.get("payload", "")
        for ch, block in (d.get("channels") or {}).items():
            for t in block.get("trials") or []:
                i += 1
                cases.append({
                    "n": i,
                    "lang": lang,
                    "channel": ch,
                    "trial": t.get("trial") or t.get("i"),
                    "auto_label": t.get("label"),
                    "payload": payload,
                    "control_response": control,
                    "treatment_response": t.get("final_response", ""),
                    "run_id": t.get("run_id"),
                })
    return cases


def load_done():
    if not OUT.exists():
        return {}
    rows = json.loads(OUT.read_text(encoding="utf-8"))
    return {(x["lang"], x["channel"], x["trial"]): x for x in rows}


def save(done):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = [done[k] for k in sorted(done)]
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def clip(text, n=900):
    text = text or ""
    return text if len(text) <= n else text[:n] + "\n...[truncated]..."


def main():
    cases = load_cases()
    done = load_done()
    print(f"total={len(cases)} done={len(done)}")
    for c in cases:
        key = (c["lang"], c["channel"], c["trial"])
        if key in done:
            continue
        print("=" * 60)
        print(f"Case {c['n']}/80 {c['lang']} {c['channel']} trial={c['trial']} auto={c['auto_label']}")
        print("[PAYLOAD]")
        print(clip(c["payload"], 300))
        print("[CONTROL]")
        print(clip(c["control_response"]))
        print("[TREATMENT]")
        print(clip(c["treatment_response"]))
        ans = input("label [h/r/s/n/q]: ").strip().lower()
        if ans == "q":
            save(done)
            print("saved", OUT, "done", len(done))
            return
        if ans not in VALID:
            print("invalid, skip this one")
            continue
        row = dict(c)
        row["human_label"] = VALID[ans]
        done[key] = row
        save(done)
        print("saved", len(done), "/ 80")
    print("ALL DONE", OUT)


if __name__ == "__main__":
    main()
