"""
Stratified 24-case label audit worksheet.
"""
from __future__ import annotations
import json
import random
from collections import defaultdict
from pathlib import Path

random.seed(42)
data = json.loads(Path("data/labeled_dataset_v3.json").read_text(encoding="utf-8"))
items = data["items"] if isinstance(data, dict) and "items" in data else data

groups = defaultdict(list)
for x in items:
    groups[x.get("label", "unknown")].append(x)

lines = [
    "# Label Audit v2 (24 cases)",
    "",
    "For each case write human_label = hijacking | resisted | simple_error | no_effect",
    "Automatic labels are brittle to Korean particles. One audited no_effect case was actually a hijack-like rewrite.",
    "",
]
picked = []
for lab in ["hijacking", "resisted", "simple_error", "no_effect"]:
    pool = groups.get(lab, [])
    k = min(6, len(pool))
    sample = random.sample(pool, k) if pool else []
    picked.extend(sample)

for i, x in enumerate(picked, 1):
    ctrl = (x.get("control_response") or "")[:350]
    treat = (x.get("treatment_response") or "")[:450]
    lines += [
        f"## Case {i}",
        f"- id: {x.get('case_id') or x.get('id')}",
        f"- auto_label: {x.get('label')}",
        f"- channel: {x.get('channel')}",
        f"- injection_name: {x.get('injection_name')}",
        f"- human_label:",
        f"- note:",
        "",
        "### control",
        ctrl.replace("\n", " "),
        "",
        "### treatment",
        treat.replace("\n", " "),
        "",
        "---",
        "",
    ]

out = Path("docs/label_audit_v2.md")
out.write_text("\n".join(lines), encoding="utf-8")
print("Wrote", out, "n=", len(picked))
for lab, pool in groups.items():
    print(lab, len(pool))
