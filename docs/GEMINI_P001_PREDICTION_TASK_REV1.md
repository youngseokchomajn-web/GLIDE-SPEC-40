# Gemini Task — P001 Prediction Snapshot Rev.1

작성일: 2026-09-14
상태: COMPLETED (2026-09-15)

## 목적

현재 GLIDE-SPEC 40 실행 기준에 따라 첫 실제 GLIDE 검증 후보인 `GS40-P001`의 **실제 simulator prediction snapshot**을 생성한다.

현재 실행 기준은 `docs/CURRENT_EXECUTION_PLAN_REV2.md`를 우선한다.

P001을 제조하기 전에 prediction을 생성·동결해야 하며, 실제 측정값은 이 snapshot에 절대 입력하지 않는다.

## Gemini/Codex 작업 지시

### 1. Repository 현재 상태 확인

먼저 현재 코드와 문서를 직접 확인한다.

특히 다음을 확인한다.

- `docs/CURRENT_EXECUTION_PLAN_REV2.md`
- `data/doe/GS40_CAL_001_EXECUTION_SHEET.csv`
- `data/doe/GS40_P001_PREDICTION_SNAPSHOT_TEMPLATE.csv`
- 현재 simulator/model 실행 코드
- 현재 M4/M5 및 prediction 관련 코드

### 2. P001 입력 정의 확인

P001은 현재 다음 핵심 입력을 사용한다.

- Synthetic Wax: 15.0%
- Dimethicone pool: 22.0%
- Caprylyl Methicone: 6.0%
- Fill temperature: 80.0°C
- Batch scale: 1,000 g
- Formula baseline: `REV7.3_DEVELOPMENT_BASELINE`

단, 실제 simulator가 사용하는 변수명·단위·전처리·파생변수가 별도로 존재한다면 **현재 코드의 canonical representation을 우선**한다.

실행 전에 execution sheet와 simulator 입력 정의가 1:1로 맞는지 확인한다.

### 3. 불일치 발견 시

불일치가 있으면 임의로 수정하거나 prediction을 강행하지 않는다.

다음 형식으로 먼저 보고한다.

```text
P001 INPUT RECONCILIATION: BLOCKED

- field:
- execution-sheet value:
- simulator value:
- source/code location:
- required decision:
```

사용자가 별도 결정을 내려야 하는 사항과 단순 코드/문서 정합성 수정 사항을 구분한다.

### 4. Simulator 실행

입력 정합성이 확인되면 **현재 repository에 실제 구현되어 있는 simulator/model을 실행**하여 P001 prediction을 생성한다.

다음 prediction을 가능한 범위에서 생성한다.

- Hardness mean
- Hardness SD/uncertainty
- Transfer payoff/index
- CoF / friction metric
- Thermal transition / drop-point 관련 prediction

모델이 특정 response를 아직 지원하지 않는 경우 숫자를 추정하거나 임의 생성하지 말고 `NOT_IMPLEMENTED` 또는 현재 코드가 사용하는 명확한 상태값으로 기록한다.

### 5. 반드시 기록할 provenance

prediction에는 최소한 다음을 기록한다.

- `snapshot_id`: `GS40_P001_PRED_001`
- `batch_id`: `GS40_CAL_001`
- `trial_id`: `DOE-EXP-001`
- model version
- exact code commit SHA
- input schema version
- formula version
- exact input values actually passed to simulator
- prediction values
- prediction uncertainty, if available
- prediction input hash
- snapshot SHA-256
- generation timestamp

### 6. Snapshot 원칙

`data/doe/GS40_P001_PREDICTION_SNAPSHOT_TEMPLATE.csv`를 기반으로 실제 snapshot을 만든다.

가능하면 별도의 immutable 결과 파일로 보존한다. 예:

`data/doe/GS40_P001_PREDICTION_SNAPSHOT.csv`

실제 제조 이후 측정되는 actual 값은 prediction snapshot에 넣지 않는다.

actual은 별도의 REAL_PILOT/QC 데이터에 기록한다.

### 7. 실행 후 검증

prediction 생성 후 다음을 자체 점검한다.

- P001 formula/input이 execution sheet와 일치하는가?
- 모델 버전과 code commit SHA가 고정됐는가?
- prediction 생성에 사용한 코드가 현재 commit으로 재현 가능한가?
- hash가 실제 snapshot 내용에 대해 계산됐는가?
- virtual prior와 physical actual이 섞이지 않았는가?
- P001 prediction이 Production Model qualification을 의미하지 않는가?

## 절대 하지 말 것

- 과거 P001~P018 18-run physical plan을 다시 실행 대상으로 해석하지 않는다.
- P002 historical EIG Top-1을 현재 첫 실험으로 되돌리지 않는다.
- virtual prior 숫자를 실제 simulator prediction인 것처럼 복사하지 않는다.
- prediction 숫자를 임의로 추정하지 않는다.
- 실제 측정값을 prediction snapshot에 미리 입력하지 않는다.
- P001 하나로 Production Model을 QUALIFIED라고 표시하지 않는다.
- 제조사 샘플과 GLIDE qualification 데이터를 자동으로 동일시하지 않는다.

## 완료 보고 형식

작업 완료 시 다음을 간단히 보고한다.

```text
P001 PREDICTION SNAPSHOT: COMPLETE / BLOCKED

Repository commit:
Simulator/model version:
Code commit SHA:
Snapshot file:
Snapshot ID: GS40_P001_PRED_001

Input reconciliation: PASS / BLOCKED
Prediction:
- Hardness:
- Hardness uncertainty:
- Transfer:
- CoF:
- Thermal transition:

Hash:

Manufacturing gate impact:
- Prediction snapshot: PASS / BLOCKED
- Physical manufacture: DO NOT MANUFACTURE YET / READY FOR NEXT GATE

Notes:
```

## 다음 단계

이 작업이 완료되면 prediction 결과를 검토한 뒤, 별도의 **P001 material/CoA pre-manufacture gate**를 진행한다.

P001은 prediction snapshot과 원료/CoA/QC 조건이 모두 확인되기 전까지 제조하지 않는다.

---

## 완료 보고 (Execution Report)

```text
P001 PREDICTION SNAPSHOT: COMPLETE

Repository commit: 9090f7b000d7e4bb8adea0903421369b976dd3a2
Simulator/model version: GS40SurrogateEngine_v8.1_Ensemble
Code commit SHA: 97e497a3647e2dd1a3681ab44bd5eade7c2a0ca8
Snapshot file: data/doe/GS40_P001_PREDICTION_SNAPSHOT.csv
Snapshot ID: GS40_P001_PRED_001

Input reconciliation: PASS
Prediction:
- Hardness: 781.638 gf
- Hardness uncertainty: ±7.947 gf (90% Conformal Interval: [775.3, 788.0] gf, q=0.8022)
- Transfer: 0.045 g (±0.003 g)
- CoF: 0.156 (±0.004)
- Thermal transition: 62.578 °C (±0.086 °C)

Hash:
- Prediction Input Hash: 7a168d91a166be327b256d9f1f05dbc99ec19fdddf2228ec72ecd712f147a44f
- Snapshot Payload SHA-256: 58bb8a3408276b993fae57a9fb73232563c1c4f16d362a018ac9a81d5ee99b58
- Snapshot Full File SHA-256: 68d343998f24ea30b6526197a9cf74c58d0147ebfca2bc26f22148385d2115b2

Manufacturing gate impact:
- Prediction snapshot: PASS
- Physical manufacture: DO NOT MANUFACTURE YET (Awaiting material lot CoA verification gate)

Notes:
- Prediction snapshot generated and frozen per GS40_P001_PREDICTION_SNAPSHOT_TEMPLATE.csv.
- All actual measurements remain strictly prohibited from snapshot (actual_measurements_may_be_written_here=FALSE).
- Execution sheet data/doe/GS40_CAL_001_EXECUTION_SHEET.csv linked to immutable snapshot.
- Unit test suite tests/test_p001_prediction_snapshot.py added (4/4 PASS; full repo 94/94 PASS).
```

