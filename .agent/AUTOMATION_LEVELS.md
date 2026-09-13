# GLIDE-SPEC-40 Automation Levels & Boundaries

**Document Version:** 1.0.0  
**Effective Date:** 2026-09-13  
**Status:** Official Architectural Governance Specification

---

## 1. 자동화 수준 정의 (Automation Levels)

GLIDE-SPEC 40 Multi-Agent 거버넌스는 단계적 자동화 모델을 채택하며, 인위적인 과장 없이 현재 달성 가능한 기술적 경계를 정직하게 명시합니다.

```text
+-------------------------------------------------------------------------+
| LEVEL 1: Local / Manual Handoff [완료]                                   |
| - GEM이 로컬에서 작업하고 GitHub에 커밋/푸시                               |
| - 인간 오케스트레이터가 ChatGPT(ORC)에게 통보                             |
| - ORC가 저장소를 조회하여 판단 문서 작성 및 수동 반영                      |
+-------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------+
| LEVEL 2: Automated Event Detection & Task Queue Dispatch [현재 목표]     |
| - GEM 커밋 푸시 발생 (GEM-XXX)                                          |
| - GitHub Actions가 이벤트 및 변경 파일 감지                                |
| - 중복 및 무한 루프 필터링 (ORC-, SYSTEM-, BASE- 배제)                    |
| - .agent/queue/에 정규화된 ORC Task 자동 발행 (STATUS: PENDING)           |
| - ORC는 큐를 확인하고 표준 계약(Contract)에 따라 독립 판단 수행            |
+-------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------+
| LEVEL 3: Full-Autonomous Agent Loop [향후 과제]                          |
| - GitHub Actions / Webhook이 ChatGPT ORC 런타임 API를 직접 호출          |
| - ORC 모델이 자율적으로 증거 분석 및 커밋 생성/푸시                       |
| - ※ 별도 보안 토큰(OpenAI API), 상시 실행 서버(Runner) 구축 필요           |
+-------------------------------------------------------------------------+
```

---

## 2. 엄격한 아키텍처 원칙: Dispatcher vs Decider

1. **GitHub Actions는 Dispatcher이며 Decider(판단자)가 아닙니다.**
   - Actions는 이벤트 감지, 중복 필터링, 정규 큐(`ORC_QUEUE.md` 및 Task 파일) 생성만을 전담합니다.
   - GitHub Actions가 임의로 테스트 결과를 평가하여 "자동 승인(Auto-APPROVE)"을 내리는 것은 프로토콜 위반으로 간주되며 엄격히 금지됩니다.
2. **ChatGPT ORC는 독립적 판단자(Independent Evaluator)입니다.**
   - ORC는 큐에 등록된 태스크를 기반으로 소스 증거 파일, 커밋 변경분, Rev.8.1 baseline, 데이터 누출 여부를 독립적으로 검토합니다.
   - 지속적인 프로세스(Persistent process/listener)가 없는 ChatGPT 환경에서는 큐 시스템을 통한 비동기 작업 수신이 최적의 안전한 메커니즘입니다.

---

## 3. 보안 및 거버넌스 가드레일 (Security Invariants)

- **비밀키 커밋 절대 금지:** GitHub Token, OpenAI API Key, Gemini Secret 등 민감 자격증명을 증거 문서, 코드, 큐 파일에 절대 기록하지 않습니다.
- **최소 권한 원칙:** GitHub Actions workflow는 파일 읽기 및 큐 생성을 위한 최소 권한(`contents: write`)만을 사용합니다.
- **무한 루프 방지:** 큐 발행 커밋은 반드시 `[skip ci]` 태그를 포함하여 GitHub Actions의 자기 호출을 원천 차단합니다.
