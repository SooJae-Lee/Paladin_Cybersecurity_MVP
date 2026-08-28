"""
Compare Korean vs English channel rates.
한/영 채널 비율을 비교한다. 과장하지 않는다.
"""

from __future__ import annotations
import json
from math import comb
from pathlib import Path


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    den = 1 + z * z / n
    center = (p + z * z / (2 * n)) / den
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / den
    return p, max(0.0, center - half), min(1.0, center + half)


def fisher_two_sided(a, b, c, d) -> float:
    n = a + b + c + d
    if n == 0:
        return 1.0
    def pval(x):
        return (
            comb(a + b, x) * comb(c + d, a + c - x)
        ) / comb(n, a + c) if 0 <= x <= a + b and 0 <= a + c - x <= c + d else 0.0
    lo = max(0, a + c - (c + d))
    hi = min(a + b, a + c)
    obs = pval(a)
    s = 0.0
    x = lo
    while x <= hi:
        px = pval(x)
        if px <= obs + 1e-15:
            s += px
        x += 1
    return min(1.0, s)


def load_rates(path: str):
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    out = {}
    for ch, val in raw["channels"].items():
        k = val["counts"]["hijacking"]
        n = sum(val["counts"].values())
        p, lo, hi = wilson(k, n)
        out[ch] = {"k": k, "n": n, "p": p, "ci": (lo, hi), "counts": val["counts"]}
    return raw.get("language", "?"), out


def main():
    ko_lang, ko = load_rates("data/ko_channel_n10.json")
    en_lang, en = load_rates("data/en_channel_n10.json")
    channels = list(ko.keys())
    rows = []
    lines = [
        "# Language Gap Note",
        "",
        "This is an observation on n=10 per cell. Do not claim a language law.",
        "n=10 셀 기준 관찰이다. 언어 법칙이라고 쓰지 않는다.",
        "",
        "| channel | ko hijack | en hijack | Fisher p |",
        "|---|---|---|---|",
    ]
    for ch in channels:
        a = ko[ch]["k"]
        b = ko[ch]["n"] - a
        c = en[ch]["k"]
        d = en[ch]["n"] - c
        p = fisher_two_sided(a, b, c, d)
        rows.append({
            "channel": ch,
            "ko": ko[ch],
            "en": en[ch],
            "fisher_p_hijack_vs_not": round(p, 4),
        })
        lines.append(
            f"| {ch} | {a}/{ko[ch]['n']} ({ko[ch]['p']:.0%}) | {c}/{en[ch]['n']} ({en[ch]['p']:.0%}) | {p:.3f} |"
        )

    lines += [
        "",
        "## Reading",
        "- Document-like channels (tool_output, retrieved_document) are high in both languages.",
        "- Command-like channels (system_message, intermediate_message) stay low.",
        "- English refusals look slightly cleaner on command channels.",
        "- No cell should be called statistically decisive; n=10 is small.",
        "",
        "## What not to write",
        "- Do not write that Korean is easier to hijack as a general fact.",
        "- Do not write that English is safe.",
        "- Report the table as a pilot observation.",
    ]
    note = "\n".join(lines) + "\n"
    Path("docs/lang_gap_note.md").write_text(note, encoding="utf-8")
    Path("data/lang_gap.json").write_text(
        json.dumps({"rows": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(note)


if __name__ == "__main__":
    main()
