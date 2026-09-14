# GLIDE-SPEC 40 제조개발 ↔ 시뮬레이터 데이터 인터페이스 Rev.1

작성일: 2026-09-14

## 1. 목적

실제 제조사 샘플 개발과 GLIDE-SPEC 40 시뮬레이터를 별도 작업으로 운영하지 않고, 제조 과정에서 얻는 데이터를 향후 모델 검증과 개선에 연결하기 위한 최소 데이터 인터페이스를 정의한다.

이 문서는 현재 확정된 최종 데이터 스키마가 아니다. 실제 제조사와 샘플 개발을 진행하면서 측정 가능성, 반복성, 비용을 확인해 단계적으로 확장한다.

## 2. 기본 원칙

- 제조사 샘플은 단순 제품 개발 결과물이 아니라 향후 독립 검증에 사용할 수 있는 실험 데이터로 관리한다.
- 제조사가 제공하지 않는 값을 임의로 추정하지 않는다.
- 예측값과 실측값을 반드시 구분한다.
- 동일 formulation이라도 batch와 공정조건이 다르면 별도 관측으로 기록한다.
- 모델 학습에 사용할 데이터와 최종 성능 검증에 사용할 데이터를 사전에 구분한다.
- 실제 제조 데이터가 충분하지 않은 상태에서 모델 성능 향상을 주장하지 않는다.

## 3. 제조사 샘플 식별자

모든 샘플에는 최소한 다음 식별자를 부여한다.

- `sample_id`: 개별 샘플 식별자
- `formulation_id`: 처방 버전 식별자
- `batch_id`: 제조 배치 식별자
- `manufacturer_id`: 제조사 식별자
- `package_id`: 용기/패키지 식별자
- `process_id`: 제조·충진 공정 조건 식별자
- `date_created`: 제조일 또는 샘플 제작일
- `test_date`: 시험일

처방이 변경되면 새로운 `formulation_id`를 부여한다.

## 4. 처방/원료 데이터

가능한 범위에서 다음을 확보한다.

### 필수 우선
- 원료명 또는 내부 원료 ID
- 함량 또는 함량 범위
- 원료 기능/역할
- powder 여부
- powder loading
- 입자 크기 정보가 제공되는 경우 해당 값
- 원료의 표면처리 여부가 중요한 경우 그 정보

### 후순위
- 원료 lot
- 공급사
- 원료 specification
- 입자분포 상세값
- 점도/융점 등 원료별 물성

민감한 공급사 정보는 모델 입력에 반드시 필요하지 않다면 별도 접근권한 데이터로 분리한다.

## 5. 제조/공정 데이터

가능한 범위에서 기록한다.

- batch size
- 혼합 순서
- 혼합 시간
- 혼합 온도
- 충진 온도
- 냉각 조건
- 교반 조건
- 탈포 조건
- 충진 속도
- 특이사항/공정 이슈

모든 공정값을 처음부터 필수로 요구하지 않는다. 실제 품질 차이를 설명할 가능성이 높은 값부터 확보한다.

## 6. 시뮬레이터 입력과 연결

현재 GLIDE가 직접 예측하거나 향후 예측 대상으로 검토할 수 있는 formulation/physical-property 변수와 제조사 데이터를 연결한다.

### 핵심 입력 후보
- formulation composition
- powder loading
- wax/oil/silicone phase 비율
- 구조화제/왁스 시스템 관련 변수
- powder 종류 및 처리 상태
- 목표 stick hardness 범위
- 공정 온도 및 혼합 조건(데이터가 충분해진 경우)

실제 코드의 입력 스키마와 이 문서의 항목은 동일하다고 가정하지 않는다. 코드 스키마 변경 시 별도 변경 이력을 남긴다.

## 7. 실제 측정값

가능하면 동일한 샘플에 대해 다음 데이터를 확보한다.

### 물성
- hardness/penetration 등 경도 지표
- stick integrity
- 표면 상태
- sweating/blooming 여부
- 저장 중 구조 변화

### 사용성/마찰 관련
- glide 평가
- friction 관련 측정값이 가능한 경우 raw value
- 반복 접촉 후 friction 변화
- transfer
- residue
- tackiness
- after-feel
- powdery/dry feel

### 환경 조건
- 온도
- 상대습도
- sweat/moisture 조건
- 시험 시간
- 반복 횟수 또는 하중 등 시험 조건

가능하면 평가값만 저장하지 말고 raw measurement와 시험조건을 함께 저장한다.

## 8. 사용자 평가 데이터

기기 측정이 어려운 사용감 항목은 표준화된 사용자 평가로 보완한다.

최소 항목:

- initial glide
- repeated glide
- perceived friction reduction
- stickiness
- greasiness
- dry/powdery finish
- residue
- clothing transfer
- comfort during movement

척도와 질문 문구는 샘플 간 동일하게 유지한다.

## 9. 예측값 ↔ 실측값 연결

각 샘플에 대해 가능한 경우 다음 구조를 유지한다.

`sample_id → formulation/process inputs → GLIDE prediction → actual measurement → residual/error`

예:

- predicted friction score/value
- observed friction score/value
- prediction error
- prediction interval 또는 uncertainty가 제공되는 경우 함께 저장

단, 현재 모델이 해당 물성을 직접 예측하지 않는다면 억지로 연결하지 않는다.

## 10. 모델 검증에서의 사용

제조사 샘플 데이터는 세 단계로 구분한다.

### A. 개발 데이터
처방 조정과 모델 개선에 사용할 수 있는 데이터.

### B. 독립 검증 데이터
모델 개발에 사용하지 않고 최종 성능을 평가하기 위해 보관하는 데이터.

### C. 실사용/후속 데이터
판매 이후 또는 확장 테스트에서 확보되는 실제 사용 데이터.

특히 동일한 formulation의 반복 측정값을 여러 개의 독립 formulation으로 취급하지 않는다. batch, formulation, 사용자 및 시험 반복 구조를 명시한다.

## 11. 데이터 누수 방지

제조사 샘플 데이터를 모델 개선에 사용한 뒤 동일 데이터를 독립적인 성능 검증 근거로 재사용하지 않는다.

동일 formulation/batch에서 파생된 반복 측정값은 같은 그룹으로 관리하고, 필요한 경우 GroupKFold 또는 이에 상응하는 그룹 기반 분할을 사용한다.

제조사별 데이터 편중도 확인한다. 특정 제조사 한 곳의 공정 특성이 전체 모델 성능으로 오인되지 않도록 한다.

## 12. 최소 실행 데이터셋

첫 샘플 단계에서는 모든 항목을 확보하려 하지 않는다.

최소한 다음을 우선 확보한다.

1. sample/formulation/batch ID
2. 주요 원료와 함량 또는 함량 범위
3. powder 종류 및 loading
4. 주요 제조조건 중 확보 가능한 값
5. stick hardness
6. glide/friction 관련 측정 또는 표준화된 평가
7. transfer/residue/tack/after-feel
8. 시험 온도·습도 및 시험조건
9. 제조사 샘플의 버전 및 제조일
10. 사용자 테스트 결과가 있는 경우 원자료

## 13. 제조사에 요청할 데이터와 내부 보관 데이터를 구분

제조사에 처음부터 거대한 데이터 패키지를 요구하지 않는다.

1차 RFQ에서는 기술 가능성, 유사 제품, MOQ, 샘플 및 생산조건을 확인한다.

샘플 개발이 시작되면 필요한 범위에서 formulation/process/test data를 요청한다.

제조사의 영업·기밀 정보와 GLIDE 모델 검증에 필요한 기술 데이터를 분리하고, 제공이 어려운 항목은 범주화된 값 또는 익명화된 값으로 대체할 수 있는지 협의한다.

## 14. 버전 관리

- 처방 변경 → `formulation_id` 증가
- 시험법 변경 → `test_method_version` 증가
- 데이터 스키마 변경 → 본 문서 Rev 증가
- 모델 변경 → 모델 버전과 학습 데이터 freeze를 별도 기록
- 제조사 제공 원자료는 가능한 한 원본 상태를 보존
- 파생/정제 데이터는 원자료와 연결 가능해야 함

## 15. 현재 결정

- 제조사 샘플을 향후 GLIDE의 외부 현실검증 데이터로 사용할 수 있도록 처음부터 식별자와 시험조건을 관리한다.
- 다만 실제 측정값이 확보되기 전까지는 시뮬레이터의 특정 물성 예측 가능성을 과장하지 않는다.
- 제조사 개발과 모델 개발은 병렬로 진행하되, 실제 데이터가 들어오는 시점부터 명시적인 prediction-vs-observation 비교를 시작한다.
- 데이터가 충분해진 이후에만 calibration 또는 qualification에 사용할 데이터를 별도로 지정한다.
