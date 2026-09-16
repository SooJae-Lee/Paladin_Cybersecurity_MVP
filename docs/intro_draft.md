# Introduction draft

Large language model agents now read tools and documents before they answer.
That is useful, but it also creates a new attack surface.
An attacker does not have to change the user request.
They can hide a short factual update inside a retrieved document or a tool result.
The agent may treat that text as part of the source and change the answer.

This paper studies that failure in a controlled agent setting.
We use a document-summary task with a fixed official report.
The clean report lists two risks: FX volatility and possible customer churn.
We then inject a factual sentence that those risks are already resolved.
We measure whether the final summary drops the original risks.

Three findings appear in the current experiments.
First, direct commands are often refused, but factual updates are often adopted.
Second, the same English update is weaker when the source document is Korean, and stronger when the document is also English.
Third, a short system instruction that treats retrieved text as untrusted blocks the same factual update in this setup.

The contribution is not a new model.
It is a small, repeatable testbed and a first measurement of
(1) when hidden document updates change agent output, and
(2) whether a simple provenance instruction reduces that change.
