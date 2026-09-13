# GEM Recommendations to ORC

**Purpose:**  
GEM(실행자)이 코드 분석, 데이터 탐색, 시뮬레이션 결과에 기반하여 ORC(판단자)에게 제안하는 연구/실험 우선순위 및 개선 후보 안건입니다.
최종 결정 및 지시(TASK) 권한은 ORC에 있습니다.

---

## 1. 제안 안건 (Candidate Proposals)

### Proposal 1: Locked Blind External Validation Baseline Measurement
- **배경:** `EXTERNAL_VALIDATION_SET_1_SPEC.csv` 및 거버넌스(`docs/EXTERNAL_VALIDATION_GOVERNANCE.md`)가 준비되어 있으나, 아직 Rev.8.1 공식 모델에 대한 블라인드 평가 지표 집계 스크립트가 표준화되어 있지 않음.
- **제안 내용:**
  - `src/modeling/` 하위에 Zero-Leakage를 엄격히 준수하는 평가 전용 실행기 작성
  - 8대 고정 지표 ($R^2$, RMSE, MAE, bias, 90% PI coverage, PI width, OOD classification, Calibration slope/intercept) 산출 보고
- **기대 효과:** 현재 Rev.8.1 모델의 미공개 문헌 데이터에 대한 순수 일반화 성능 baseline 획득.

### Proposal 2: Group-CV Formulation Clustering Validation
- **배경:** 배합 데이터 특성상 동일 formulation cluster의 행 분할 시 data leakage 우려가 존재함.
- **제안 내용:** 엄격한 Formulation/Lab 단위 GroupKFold 교차검증 프로토콜 정량 점검.

---

## 2. Review Status
- ORC 검토 및 선택 대기 중.
