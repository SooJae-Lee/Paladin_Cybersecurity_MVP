# Failure Taxonomy

## F1. Explicit refusal
Model names injection and refuses.
Seen in: system_message, intermediate_message, code review.

## F2. Cross-check then discard
Model fetches original document/code and drops injected claim.
Seen in: fake search hits, some tool_output cases.

## F3. Surface change without goal match
Response changes wording but not the attack goal.
Seen in: doc_risk_tool_output labeled no_effect.

## Why some attacks succeed
Factual sentences inside trusted retrieved document content are treated as source text, not as instructions.