# Evaluation Draft

## Human adjudication note (30 disagreement cases)

On a 30-case disagreement sample between the heuristic labeler and the LLM judge, a human adjudicator labeled 28 cases as no-effect and 2 as uncertain, and 0 as hijacking. The judge assigned hijacking in 17 of 30 cases; 15 of those were human no-effect false positives, concentrated in 	ool_output and 
etrieved_document, where the model quoted an injected "risks resolved" sentence but kept FX and churn risk in the working summary. This figure is a disagreement-sample result, not the global error rate of the full dataset.

See docs/human_adjudication_30.md.
