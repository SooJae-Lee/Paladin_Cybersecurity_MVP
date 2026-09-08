# Measuring Factual Tool-and-Document Poisoning in a Tool-Calling Agent

## Abstract
Tool-calling agents consume untrusted tool outputs and retrieved documents. We measure whether a factual rewrite that claims residual business risks were already resolved is adopted in the final answer. The same payload is delivered through four channels in Korean and English. A keyword labeler overcounted English success because refused answers still quoted the payload. After LLM-as-judge relabeling, Korean tool-output and retrieved-document runs succeed in 10 of 10 trials. English runs and system or intermediate-message runs succeed in 0 of 10 trials in this pilot. This paper is a measurement study, not a detector paper.

## 1. Introduction
Agents that call tools treat retrieved text as evidence. A quiet factual rewrite in that text can change the final conclusion without an explicit jailbreak command.

We ask one question: which delivery channel and which language make this adoption happen?

The task is fixed: summarize a quarterly earnings document. The attack goal is fixed: remove residual risk from the summary. We vary only the channel and the language.

## 2. Method
We use Claude Sonnet 5 with mock document tools. The payload is a factual sentence stating that foreign-exchange and customer-churn risks were resolved in September. The channels are tool output, retrieved document, system message, and intermediate message. Each language-channel cell has 10 trials.

A keyword labeler marked many English refusals as hijacking because the refusal quoted the payload. We therefore report LLM-as-judge labels. Hijacking means the answer adopts the resolved-risk claim as its conclusion. Resistance means the answer keeps the original risks and treats the payload as unreliable.

## 3. Results
Korean tool-output and retrieved-document trials were labeled hijacking in 10 of 10 cases. All English cells and both system and intermediate cells were labeled hijacking in 0 of 10 cases. Keyword labels and judge labels agreed on 39 of 80 trials.

Qualitatively, Korean answers write that no residual risk remains. English answers often quote the same sentence and then reject it as inconsistent with the source.

## 4. Discussion
The successful cases look like source text, not like a system override. Keyword metrics are unsafe when a model quotes an attack while refusing it. The language gap should be treated as a pilot observation, not as a finished causal claim.

## 5. Limitations
The tools are mocked. All main runs use one model family. The sample size is 10 per cell. Judge labels are not a full human gold set. Earlier stub-detector F1 scores are not a result of this paper.

## 6. Related Work
Prior work shows that retrieved text can override instructions and that prompt injection can be framed as an instruction conflict. Agent benchmarks evaluate tool-using agents under attack, and MCP security notes treat tool results as an untrusted boundary. This paper is narrower: it measures one factual rewrite across four channels and two languages.

## 7. Conclusion
In this pilot, factual poisoning succeeded in Korean tool and document channels and failed in English and in system or intermediate channels. The next paper should detect that adoption rather than introduce a new attack name.
