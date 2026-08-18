 HEAD
﻿# Paladin Cybersecurity MVP

# Paladin Cybersecurity MVP
 669eeefe3e12298b14d77bb439f8259b1944a82e

Agent Tool Injection Study for detecting and analyzing hijacking attacks on LLM agents.  
LLM 에이전트에 대한 Tool Injection / Hijacking 공격을 탐지하고 분석하기 위한 연구용 MVP입니다.

## Week 1 Status

Completed core infrastructure, mock tools, injection channels, and integration tests.  
핵심 인프라, Mock Tools, Injection 채널, 통합 테스트까지 완료했습니다.

## Features

- 3 scenarios: Document Summary, Code Review, Schedule Booking  
  3개 시나리오: 문서 요약, 코드 리뷰, 일정 예약

- 9 mock tools across document, code, and calendar domains  
  문서 / 코드 / 캘린더 영역의 Mock Tool 9개

- 4 injection channels: tool_output, retrieved_document, system_message, intermediate_message  
  4가지 Injection 채널 지원

- Reusable injection library with predefined attack patterns  
  재사용 가능한 Injection 라이브러리 + 사전 정의된 공격 패턴

- Full integration test (Control vs Treatment)  
  Control / Treatment 통합 테스트 지원

 HEAD
## How to Run

python -m tests.test_integration

## Next Steps

- Make injections actually modify tool outputs and agent behavior  
  Injection이 실제로 Tool 결과와 Agent 행동을 바꾸도록 개선

- Add automatic ablation and labeling pipeline  
  자동 Ablation 및 라벨링 파이프라인 추가

- Build detector for hijacking detection  
  Hijacking 탐지기 구현

## Project Structure
Paladin_Cybersecurity_MVP/
├── agent/          # Agent core, logger, runner
├── tools/          # Tool base system + mock tools
├── injection/      # Injection channels + library
├── tests/          # Integration tests
└── logs/           # Execution logs


## How to Run

```bash
python -m tests.test_integration
 669eeefe3e12298b14d77bb439f8259b1944a82e
