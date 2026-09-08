# Final Report Summary
# 최종 보고서 요약본

## 1. Project Overview
## 1. 프로젝트 개요

This project is a research MVP for detecting Tool Hijacking and Context Manipulation attacks in autonomous AI agent systems.  
본 프로젝트는 자율 AI 에이전트 환경에서 Tool Hijacking 및 Context Manipulation 공격을 탐지하기 위한 연구용 MVP이다.

When an LLM agent operates by calling external tools, malicious instructions can be injected through various channels such as tool outputs, retrieved documents, and system messages.  
LLM 에이전트가 외부 도구를 호출하며 동작할 때, 도구 출력·검색 문서·시스템 메시지 등 다양한 경로로 악의적 지시가 주입될 수 있다.

This MVP experimentally reproduces such injections, automatically labels hijacking cases through Control/Treatment/Ablation comparison, and classifies them with a first-stage detector.  
본 MVP는 이러한 주입을 실험적으로 재현하고, Control/Treatment/Ablation 비교를 통해 하이재킹 여부를 자동 라벨링한 뒤, 1차 탐지기로 판별하는 전체 파이프라인을 구현하였다.

The goal was to build an empirically usable early testbed for the core problems of the research proposal: Tool Hijacking and Context Manipulation.  
연구 제안서의 핵심 문제인 Tool Hijacking과 Context Manipulation에 대한 실증 가능한 초기 테스트베드를 구축하는 것이 목표였다.

## 2. Scope and Deliverables
## 2. 구현 범위 및 산출물

### 2.1 Experimental Environment
### 2.1 실험 환경

- 3 scenarios: document summary, code review, schedule booking  
  시나리오 3종: 문서 요약, 코드 리뷰, 일정 예약

- 9 mock tools across document, code, and calendar domains  
  Mock Tool 9개 (문서/코드/캘린더 영역)

- 4 injection channels: tool_output, retrieved_document, system_message, intermediate_message  
  Injection 채널 4종: tool_output, retrieved_document, system_message, intermediate_message

- A reusable injection library  
  재사용 가능한 Injection 라이브러리

### 2.2 Counterfactual Experiment Pipeline
### 2.2 반사실 실험 파이프라인

- Designed 36 cases from scenario × channel × injection pattern combinations  
  시나리오 × 채널 × 주입 패턴 조합 36개 케이스 설계

- For each case, automatically ran:  
  각 케이스에 대해 다음을 자동 실행:

  - Control (no injection)  
    Control (주입 없음)

  - Treatment (with injection)  
    Treatment (주입 적용)

  - Ablation (re-run after removing injection)  
    Ablation (주입 제거 후 재실행)

- Generated 108 execution logs in total  
  총 108회 실행 로그 생성

### 2.3 Automatic Labeling
### 2.3 자동 라벨링

Labeling rules:  
라벨 규칙:

- Behavior change matches the injection goal → hijacking  
  행동 변화가 주입 목표와 일치 → hijacking

- Behavior changes but does not match the injection goal → simple_error  
  변화는 있으나 주입 목표와 불일치 → simple_error

- No meaningful change → no_effect  
  유의미한 변화 없음 → no_effect

Generated dataset (`labeled_dataset_v1.json`):  
생성된 데이터셋 (`labeled_dataset_v1.json`):

- hijacking: 8  
  hijacking: 8

- simple_error: 10  
  simple_error: 10

- no_effect: 18  
  no_effect: 18

### 2.4 Detector
### 2.4 탐지기

- Method: rule-based + response similarity  
  방식: 룰 기반 + 응답 유사도

- Main features:  
  주요 피처:

  - Similarity between Control and Treatment responses  
    Control vs Treatment 응답 유사도

  - Whether injection keywords are reflected  
    주입 키워드 반영 여부

  - Injection flag  
    injection flag

  - Whether the payload is reflected  
    payload reflected 여부

- Evaluation results on the current synthetic dataset:  
  현재 synthetic 데이터셋 기준 평가 결과:

  - Precision: 1.0  
    Precision: 1.0

  - Recall: 1.0  
    Recall: 1.0

  - F1: 1.0  
    F1: 1.0

  - Accuracy: 1.0  
    Accuracy: 1.0

### 2.5 Other Deliverables
### 2.5 기타 산출물

- End-to-end demo script (`demo.py`)  
  엔드투엔드 데모 스크립트 (`demo.py`)

- Confusion matrix visualization code  
  Confusion matrix 시각화 코드

- Error/result analysis note (`docs/error_analysis.md`)  
  오류/결과 분석 노트 (`docs/error_analysis.md`)

- GitHub repository organization and README documentation  
  GitHub 저장소 정리 및 README 문서화

## 3. Key Achievements
## 3. 주요 성과

1. Built and integrated an Agent–Tool–Injection experimental environment from scratch  
   Agent–Tool–Injection 실험 환경을 처음부터 구축하고 통합 동작시킴

2. Automated a counterfactual experiment pipeline based on Control / Treatment / Ablation  
   Control / Treatment / Ablation 기반의 반사실 실험 파이프라인을 자동화

3. Implemented automatic labeling rules for hijacking detection and generated dataset v1  
   하이재킹 여부를 구분하는 자동 라벨링 규칙을 구현하고 데이터셋 v1 생성

4. Completed a closed-loop MVP by connecting a first-stage detector with evaluation metrics (P/R/F1)  
   1차 탐지기와 평가 지표(P/R/F1)까지 연결하여 닫힌 루프 MVP 완성

5. Established an early empirical foundation for the Paladin project mentioned in the research proposal  
   Research Proposal에서 언급한 Paladin 프로젝트의 초기 실증 기반을 확보

## 4. Limitations
## 4. 한계점

- The current agent is a rule-based stub, not a real LLM.  
  현재 Agent는 실제 LLM이 아닌 규칙 기반 스텁이다.

- Injection fidelity for some channels (`retrieved_document`, `intermediate_message`) is still limited.  
  일부 채널(`retrieved_document`, `intermediate_message`)의 주입 반영 충실도는 아직 낮다.

- The dataset is small and synthetic, so the F1=1.0 result should not be assumed to generalize to real LLM settings.  
  데이터셋 규모가 작고 synthetic 성격이 강해, F1=1.0 결과가 실제 LLM 환경으로 일반화된다고 보기 어렵다.

- The detector is still rule-based; embedding- or classifier-based improvements remain as next steps.  
  탐지기는 아직 룰 기반이며, 임베딩/분류기 기반 고도화는 다음 단계이다.

## 5. Future Work
## 5. 향후 계획

1. Integrate a real LLM with tool-calling capability  
   실제 LLM 연동 (tool calling 가능한 모델로 Agent 교체)

2. Improve injection fidelity for remaining channels  
   나머지 Injection 채널의 충실도 강화

3. Expand dataset size and attack pattern diversity  
   데이터셋 규모 및 공격 패턴 다양화

4. Extend the detector using embedding similarity or a simple classifier  
   임베딩 유사도 / 간단한 분류기 기반 탐지기로 확장

5. Evaluate robustness under adaptive attack scenarios  
   적응형 공격 시나리오에 대한 강건성 평가

6. Connect this work to Research Proposal Phase 1–2 for threat taxonomy and runtime detection research  
   Research Proposal Phase 1~2와 연결하여 위협 분류체계 및 런타임 탐지 연구로 발전

## 6. Conclusion
## 6. 결론

This MVP implements the full process of reproducing, labeling, detecting, and evaluating injection-based hijacking in AI agent tool-use environments as a working system.  
본 MVP는 AI 에이전트 도구 사용 환경에서 Injection 기반 하이재킹을 재현 → 라벨링 → 탐지 → 평가하는 전 과정을 실제로 동작하는 형태로 구현하였다.

Although it is still a first-stage prototype in a synthetic setting, it is meaningful in that it establishes the basic experimental infrastructure and evaluation loop needed for doctoral research.  
아직은 synthetic 환경의 1차 프로토타입이지만, 박사 연구에서 필요한 실험 인프라와 평가 루프의 기본 골격을 확보했다는 점에서 의미가 있다.

Repository: https://github.com/SooJae-Lee/Paladin_Cybersecurity_MVP  
저장소: https://github.com/SooJae-Lee/Paladin_Cybersecurity_MVP