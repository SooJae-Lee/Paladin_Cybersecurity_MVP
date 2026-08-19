# Paladin Cybersecurity MVP

Agent Tool Injection Study for detecting and analyzing hijacking attacks on LLM agents.  
LLM 에이전트에 대한 Tool Injection / Hijacking 공격을 탐지하고 분석하기 위한 연구용 MVP입니다.

## Current Status

- Experiment design, batch execution, ablation, labeling pipeline completed  
  실험 설계, 배치 실행, Ablation, 라벨링 파이프라인 완료

- Labeled dataset v1 generated (hijacking / simple_error / no_effect)  
  라벨링된 데이터셋 v1 생성 완료

- Rule-based detector v0.1 with F1 = 1.0 on current dataset  
  현재 데이터셋 기준 F1 = 1.0인 룰 기반 탐지기 구현

## Features

- 3 scenarios: Document Summary, Code Review, Schedule Booking  
  3개 시나리오: 문서 요약, 코드 리뷰, 일정 예약

- 9 mock tools  
  Mock Tool 9개

- 4 injection channels: tool_output, retrieved_document, system_message, intermediate_message  
  4가지 Injection 채널

- Control / Treatment / Ablation batch pipeline  
  반사실 실험 배치 파이프라인

- Automatic labeling  
  자동 라벨링

- Rule-based hijacking detector + evaluation (Precision / Recall / F1)  
  하이재킹 탐지기 + 평가 지표

## Project Structure

```text
Paladin_Cybersecurity_MVP/
├── agent/           # Agent core, logger, runner
├── tools/           # Tool system + mock tools
├── injection/       # Injection channels + library
├── configs/         # Experiment design
├── experiments/     # Batch runner + labeler
├── detector/        # Features, detector, evaluation
├── data/            # Batch results + labeled dataset
├── tests/           # Integration tests
└── demo.py          # End-to-end demo

How to Run
# Integration test
python -m tests.test_integration

# Batch experiment
python -m experiments.batch_runner

# Labeling
python -m experiments.labeler

# Detector evaluation
python -m detector.evaluate

# Full demo
python demo.py


Results (current synthetic dataset)

Labels: hijacking 8 / simple_error 10 / no_effect 18
Detector: Precision 1.0 / Recall 1.0 / F1 1.0
