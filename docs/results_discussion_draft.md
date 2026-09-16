# Results and discussion draft

Without defense, a factual update inside a retrieved document often changes the summary.
Direct commands are weaker.
The same English update is weaker on a Korean document and stronger on an English document.

A short system prompt that treats retrieved text as untrusted
changes the same V2 attack from adopted to rejected in 15/15 trials.
The same prompt also blocks a V6 memo-style update in 5/5 trials.

This does not prove a general defense.
It shows that provenance instructions can matter
when the attack looks like a source update rather than a jailbreak.

Limits:
- one model family
- mock tools
- small n on some cells
- judge labels still need more human checks
