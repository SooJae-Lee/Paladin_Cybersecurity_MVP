# AsiaCCS delta vs frozen AIDC WIP

AIDC files stay in paper/aidc/.
Do not change those counts.
This paper adds A/B/C on top.

## Already measured (AIDC, frozen)
- Claude Sonnet 5, P0, n=10: KO tool+doc 20/20, EN tool+doc 0/20
- No-injection baseline: 0/5 KO, 0/5 EN
- GPT-4o, same four P0 cells: 5/5 KO, 5/5 EN
- Extra Claude payloads: n=3 only
- Claim limit: not "Korean is weaker"; adoption is model x language x channel x payload

## Added experiments

### A - scale and scoring
- A-1: P1-P5 with n=15-20
- A-2: GPT-4o second-pass judge on stored answers
- A-3: larger no-injection baseline

### B - wording vs language
- B-1: six surface forms V1-V6 of the same fact
- Pilot n=10, then main n=20 on variants that move the number
- Question: is the KO/EN gap the language, or that one Korean string?

### C - small defenses (not the old detector)
- C-1: warning text before the tool result
- C-2: same warning in KO vs EN
- C-3: structured output constraint
- C is optional. The archived detector_mvp is not this paper method.

## Framing after 10/16
- Accept: extension of AIDC 2026 WIP
- Reject: fold reviewer points into Method/Limitations; do not name the reject in the PDF
