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
