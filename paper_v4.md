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
