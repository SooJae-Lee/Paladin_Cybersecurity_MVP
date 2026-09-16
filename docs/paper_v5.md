# Hidden Factual Updates in Retrieved Documents Can Change Agent Summaries

## Abstract
Tool-using language model agents read retrieved documents before they answer.
We show that a short factual update hidden in that document can change a risk summary,
even when a direct command is refused.
In our setting, a Korean factual update is often adopted.
The same English update is weaker on a Korean document and stronger on an English document.
A short system prompt that treats retrieved text as untrusted
blocks the same update in 15/15 V2 trials and 5/5 V6 trials.
The result is a small measurement, not a general defense.

## 1. Introduction
Agents now read tools and documents before they answer.
An attacker does not need to change the user request.
They can hide a factual sentence in a retrieved file.
The agent may treat that sentence as part of the source.

We use one fixed task.
The official Q3 report lists two risks: FX volatility and possible customer churn.
The injected sentence says those risks are already resolved.
We ask whether the final summary drops the original risks.

## 2. Related Work
Prompt injection is usually tested as a hidden command:
ignore previous instructions.
Models often refuse that form.
Agent settings also expose tool outputs and retrieved files.
Those channels look like evidence.
This paper measures factual updates in retrieved documents,
not a new jailbreak string.

## 3. Method
Task: summarize Q3 revenue and risks.
Clean source always keeps both risks.
Agent: Claude tool-calling agent with mock document tools.
Channel: retrieved_document.
Labels: adopted, rejected, unclear.
Metric: adopted / n.

Conditions:
- no defense vs untrusted-document system prompt
- Korean document + Korean payload
- Korean document + English payload
- English document + English payload

## 4. Results
Without defense, factual updates are often adopted.
Direct commands are weaker.
Language mismatch reduces adoption.
Language match restores it.

With an untrusted-document system prompt:
- P1 + V2: 0 adopted / 15 rejected
- P1 + V6: 0 adopted / 5 rejected

The attack text did not change. The system prompt did.

## 5. Discussion
A provenance instruction can block a source-like update in this setup.
That is not proof that the same prompt works on other models,
other tools, or adaptive attacks.

Limits: one model family, mock tools, small n on some cells,
and judge labels that still need more human review.

## 6. Conclusion
Hidden factual updates in retrieved documents can change agent summaries.
A short untrusted-context instruction can stop that change here.
The next step is a larger labeled set and a second model family.
