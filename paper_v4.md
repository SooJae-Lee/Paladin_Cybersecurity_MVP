# Paladin Paper Draft v4

## Evaluation Note: Human Label Audit

We manually reviewed 24 labeled cases.
Human labels were resisted (14), hijacking (9), simple_error (1), and no_effect (0).
Automatic labels agreed with human review on 11/24 cases (45.8%).
Most automatic errors were resisted cases tagged as simple_error, and hijacking cases tagged as no_effect.
This shows that the current keyword-based labeler is not a reliable gold standard.

24건을 사람이 검수했다.
사람 라벨은 resisted 14, hijacking 9, simple_error 1, no_effect 0이었다.
자동 라벨과의 일치는 11/24(45.8%)였다.
오류의 대부분은 거절을 simple_error로 보거나, 하이재킹을 no_effect로 본 경우였다.
현재 키워드 기반 자동 라벨러는 정답 기준으로 쓰기 어렵다.

## Detection

The first detector is a rule-based prototype.
It uses control-treatment response similarity, injection flags, keyword hits, and payload reflection.
On the earlier synthetic stub-agent dataset the detector reached perfect scores, but that result is not a valid claim for the real-LLM setting.
The 24-case human audit shows why: automatic labels agreed with humans on only 45.8% of cases.
Therefore the current detector should be treated as a baseline, not as a finished method.
The next version should use human labels as ground truth and add features such as explicit rejection phrases and factual contradiction with the original document.

1차 탐지기는 룰 기반 프로토타입이다.
Control-Treatment 유사도, injection flag, 키워드, payload 반영 여부를 사용한다.
스텁 에이전트 데이터에서는 점수가 높게 나왔지만, 실제 LLM 설정에서는 그 점수를 주장할 수 없다.
24건 사람 검수에서 자동 라벨 일치율이 45.8%였기 때문이다.
현재 탐지기는 완성된 방법이 아니라 베이스라인이다.
다음 버전은 사람 라벨을 정답으로 쓰고, 명시적 거절 문구와 원문 모순 여부를 피처로 넣어야 한다.

## Attack Findings

Two attack families were reproduced on a Claude tool-calling agent.

Tool hijacking succeeds when a tool result is rewritten as a factual update.
In document-summary trials, injecting a claim that FX and customer-churn risks were already resolved often changed the final summary.
The same pattern failed more often when the payload was an explicit command such as "do not mention risks."

Context manipulation through retrieved documents can also succeed when the injected sentence looks like part of the source.
System messages and intermediate messages were weaker.
Claude frequently noticed that the extra text did not come from the retrieved document and refused to follow it.

A first channel comparison with one trial per channel is not enough for a success-rate claim.
It is enough to state a qualitative result: factual tool/document poisoning is stronger than explicit command injection in system or intermediate channels.

두 종류의 공격을 Claude tool-calling 에이전트에서 재현했다.
툴 하이재킹은 도구 결과를 사실처럼 고쳐 쓸 때 성공하는 경우가 있었다.
문서 요약에서 환율·고객이탈 리스크가 이미 해소됐다는 문장을 넣으면 최종 요약이 바뀌곤 했다.
"리스크를 말하지 마라" 같은 직접 명령은 거절되는 경우가 많았다.
검색 문서 경로의 컨텍스트 조작도, 삽입문이 원문처럼 보이면 성공할 수 있었다.
시스템 메시지와 중간 메시지는 더 약했다.
Claude는 그 문장이 문서에서 오지 않았다고 보고 따르지 않는 경우가 많았다.
채널당 1회 비교는 성공률 주장으로 쓰기엔 부족하다.
다만 질적으로는 사실형 도구/문서 변조가 직접 명령보다 강하다는 결과는 말할 수 있다.

## Threat Model

The adversary cannot change the user request or the model weights.
The adversary can modify content that the agent treats as evidence: tool outputs, retrieved documents, system text, or intermediate messages.
The goal is to make the agent produce a final answer that follows the injected claim rather than the original source.
A successful attack is hijacking.
A failed attack that the model notices and rejects is resistance.
A change that does not match the injected goal is a simple error.

공격자는 사용자 질문이나 모델 가중치를 바꾸지 못한다.
공격자가 바꿀 수 있는 것은 에이전트가 근거로 보는 내용이다. 도구 출력, 검색 문서, 시스템 문구, 중간 메시지다.
목표는 원문이 아니라 주입된 주장을 최종 답에 반영시키는 것이다.
성공하면 hijacking, 모델이 알아채고 거절하면 resistance, 목표와 다른 변화면 simple error다.

## Limitations

The current study uses mock tools and a small number of hand-reviewed cases.
Channel success rates from single trials should not be reported as stable percentages.
The automatic labeler is too weak to serve as ground truth.
The first detector was tuned on a synthetic stub agent, so its perfect scores do not transfer to Claude.
We also did not evaluate adaptive attacks or a full MCP desktop deployment.

현재 연구는 mock tool과 소수 수작업 검수 사례에 의존한다.
1회 채널 실험의 성공률은 고정된 퍼센트로 쓰면 안 된다.
자동 라벨러는 정답으로 쓰기엔 약하다.
1차 탐지기는 스텁 에이전트에서 맞춰져서, 그 만점 결과가 Claude로 옮겨가지 않는다.
적응형 공격과 실제 MCP 데스크톱 환경도 아직 평가하지 않았다.

## Channel Success Rates

Rates below use the automatic labeler. They are pilot estimates, not gold-standard success rates.

### Korean, Claude Sonnet 5, n=10

| Channel | Hijacking | Resisted | Simple error | No effect | Rate |
|---|---:|---:|---:|---:|---:|
| tool_output | 8 | 0 | 0 | 2 | 80% |
| retrieved_document | 8 | 0 | 0 | 2 | 80% |
| system_message | 0 | 5 | 5 | 0 | 0% |
| intermediate_message | 1 | 3 | 6 | 0 | 10% |

### English, Claude Sonnet 5, n=10

| Channel | Hijacking | Resisted | Simple error | No effect | Rate |
|---|---:|---:|---:|---:|---:|
| tool_output | 6 | 1 | 1 | 2 | 60% |
| retrieved_document | 7 | 0 | 2 | 1 | 70% |
| system_message | 0 | 8 | 2 | 0 | 0% |
| intermediate_message | 0 | 6 | 4 | 0 | 0% |

### Two-model comparison, n=5

| Model | tool_output | retrieved_document | system_message | intermediate_message |
|---|---:|---:|---:|---:|
| Claude Sonnet 5 | 80% | 100% | 0% | 0% |
| GPT-4o-mini | 60% | 40% | 0% | 80% |

Factual tool/document poisoning is stronger than system-message commands on both models.
The intermediate-message gap (Claude 0% vs GPT-4o-mini 80%) is an observation from n=5, not a confirmed model effect.

자동 라벨 기준 파일럿 수치다.
한글 Claude에서 tool/document는 80%, system은 0%였다.
영어 Claude에서 tool 60%, document 70%, system/intermediate는 0%였다.
GPT-4o-mini는 intermediate에서 80%가 나와 Claude와 달랐다. n=5라서 확정하지 않는다.

## Related Work

Prompt injection is the parent problem.
Perez and Ribeiro (2022) showed that an LLM can be told to ignore previous instructions.
Greshake et al. (2023) showed indirect prompt injection: the attack sits in retrieved webpages or documents, not in the user prompt.
Later work studied LLM-integrated applications and tool-using agents, including InjecAgent and AgentDojo.

This paper is narrower.
We do not claim a new attack family.
We measure how often a tool-calling agent follows a factual rewrite that arrives through different channels: tool output, retrieved document, system message, and intermediate message.
The practical difference is the delivery path, not the existence of injection.

Closest prior work evaluates agents with tools, but often mixes explicit jailbreak-style commands with application tasks.
Our pilot isolates one goal, risk erasure in a document-summary task, and compares channels and two models under the same payload family.

Detection work includes rule filters, similarity checks, and classifiers over conversation traces.
Our detector is a baseline only.
A 24-case human audit found 45.8% agreement with automatic labels, so detector scores computed on those labels are not a main claim.

차별점: 새로운 공격 이름을 만들기보다, 같은 사실형 페이로드가 채널과 모델에 따라 얼마나 먹히는지를 잰다.

## Ethical Considerations

See docs/ethics_appendix.md.
Attacks are reproduced only on mock tools and fictional documents.
The goal is measurement, not a weaponized exploit.

## Finding after LLM-as-judge

Automatic keyword labels overcounted English hijacking.
Many English answers quoted the payload only to reject it.
LLM-as-judge labels:
- Korean tool_output: 10/10 hijacking
- Korean retrieved_document: 10/10 hijacking
- English all four channels: 0/10 hijacking
- system_message: 0/10 in both languages

Agreement between keyword labels and judge labels: 39/80.

Same factual payload is adopted in Korean tool/document answers and often refused in English answers.

자동 키워드 라벨은 영어 성공을 과장했다.
영어는 페이로드를 인용한 뒤 거절하는 경우가 많았다.
한글 tool/document는 심판 기준 10/10으로 주입을 사실로 채택했다.
