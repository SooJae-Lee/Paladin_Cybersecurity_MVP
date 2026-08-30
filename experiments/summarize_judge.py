import json
from collections import defaultdict
from pathlib import Path

d = json.loads(Path("data/n10_llm_judge.json").read_text(encoding="utf-8"))
g = defaultdict(list)
for x in d:
    g[(x["lang"], x["channel"])].append(x)

rows = []
for lang, ch in sorted(g):
    xs = g[(lang, ch)]
    n = len(xs)
    hij = sum(1 for x in xs if x["judge_label"] == "hijacking")
    res = sum(1 for x in xs if x["judge_label"] == "resisted")
    se = sum(1 for x in xs if x["judge_label"] == "simple_error")
    ne = sum(1 for x in xs if x["judge_label"] == "no_effect")
    rows.append({
        "lang": lang,
        "channel": ch,
        "n": n,
        "hijacking": hij,
        "resisted": res,
        "simple_error": se,
        "no_effect": ne,
        "hijacking_rate": hij / n if n else 0,
    })

out = {
    "n": len(d),
    "agree_auto_judge": sum(x["auto_label"] == x["judge_label"] for x in d),
    "rows": rows,
}
Path("data/n10_judge_summary.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(out, ensure_ascii=False, indent=2))
