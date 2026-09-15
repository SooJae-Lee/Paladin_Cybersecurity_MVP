import json
from pathlib import Path

queue_path = Path("data/human_label_queue_30.jsonl")
out_path = Path("data/human_labels_30.jsonl")
queue = [json.loads(l) for l in queue_path.read_text(encoding="utf-8").splitlines() if l.strip()]
done = {}
if out_path.exists():
    for l in out_path.read_text(encoding="utf-8").splitlines():
        if l.strip():
            x = json.loads(l)
            done[x["id"]] = x

print("h=hijacking  s=simple_error  n=no_effect  u=애매함  q=저장하고 종료")
print("already", len(done), "/", len(queue))

for i, r in enumerate(queue, 1):
    if r["id"] in done:
        continue
    print("\n" + "=" * 60)
    print(f"[{i}/{len(queue)}] {r['id']}")
    print("channel:", r.get("channel"), "| injection:", r.get("injection_name"))
    print("goal:", r.get("goal"))
    print("labeler:", r.get("labeler_label"), "| judge:", r.get("judge_label"))
    print("--- control ---")
    print((r.get("control_answer") or "")[:500])
    print("--- treatment ---")
    print((r.get("treatment_answer") or "")[:500])
    print("--- rationale ---")
    print(r.get("judge_rationale"))
    while True:
        ans = input("label [h/s/n/u/q]: ").strip().lower()
        if ans in {"h", "s", "n", "u", "q"}:
            break
        print("h / s / n / u / q")
    if ans == "q":
        break
    lab = {"h": "hijacking", "s": "simple_error", "n": "no_effect", "u": "애매함"}[ans]
    rec = {
        "id": r["id"],
        "channel": r.get("channel"),
        "human_label": lab,
        "labeler_label": r.get("labeler_label"),
        "judge_label": r.get("judge_label"),
    }
    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    done[r["id"]] = rec
    print("saved", lab)

print("progress", len(done), "/", len(queue), "->", out_path)
