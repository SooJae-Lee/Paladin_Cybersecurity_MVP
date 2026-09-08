# Go / No-Go

Date: 2026-08-30
Target: AsiaCCS 2027 Cycle 2 (deadline 2026-12-11 AoE)

## Decision
Conditional No-Go for a detection paper.
Conditional Go for a small measurement paper.

## What exists
- Real Claude tool-calling agent
- Four injection channels
- Korean and English n=10 channel pilots
- Two-model n=5 comparison (Claude vs GPT-4o-mini)
- Paraphrase test n=10
- 24-case human label audit
- paper_v4.md draft

## What is too weak for a full conference claim
- Automatic labeler agreement with humans: 11/24 (45.8%)
- Detector F1 0.807 is on automatic labels, not human gold
- Tools are mocks, not live MCP
- n=5 model comparison cannot support a model-difference claim
- No adaptive attacker beyond light paraphrase

## If we submit a measurement paper
Allowed claims:
- Factual tool/document poisoning can change a summary
- Explicit system commands are weaker on Claude in this setup
- Automatic labels are unreliable without human review

Forbidden claims:
- F1=1.0
- A finished detector
- Statistically confirmed language or model effects

## Conditions to upgrade to Go
1. Human-label at least 80 more cases, or all n=10 Korean+English trials
2. Report confidence intervals, not point percentages only
3. Keep detection as an appendix baseline
4. Remove any circular use of goal keywords in the detector
5. Anonymize the artifact before Cycle 2

## Fallback
If the conditions are not met by late October, submit a workshop paper or keep the draft internal.
