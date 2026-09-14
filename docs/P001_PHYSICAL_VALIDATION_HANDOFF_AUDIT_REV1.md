# GLIDE-SPEC 40 — P001 Physical Validation Handoff Audit Rev.1

작성일: 2026-09-14  
상태: CURRENT / HANDOFF GATE  
대상: `GS40-P001` / `GS40_CAL_001` / `DOE-EXP-001`

## 1. 결론

P001은 **가상 예측 → 실제 제조 → 실측 비교**의 첫 물리 검증 후보로 유지한다.

다만 2026-09-14 현재 바로 제조를 승인할 상태는 아니다.

**판정: CONDITIONAL READY / 제조 전 필수 게이트 미충족**

필수 게이트는 다음 5개다.

1. 실제 원료 supplier / grade / INCI / lot / CoA 확정
2. MQ Resin의 실제 solids %, carrier 및 투입량 재계산
3. Soothing Blend의 실제 구성 확정 및 Formula version 고정
4. P001의 사전 prediction snapshot 생성 및 immutable 저장
5. QC SOP의 실제 시험조건/장비/시편수/기록방식 확정

이 다섯 가지가 완료되기 전에는 `REAL_PILOT` 제조 데이터로 등록하지 않는다.

---

## 2. P001 처방과 가상 기준의 1:1 점검

가상 prior에서 P001은 Synthetic Wax 15.0%, Dimethicone 22.0%, Fill Temperature 80.0°C로 정의되어 있다. fileciteturn34file0

현재 P001 physical sheet도 동일한 핵심 DOE 좌표를 사용한다.

| 항목 | Virtual P001 | Physical P001 | 판정 |
|---|---:|---:|---|
| Synthetic Wax | 15.0% | 15.0% | MATCH |
| Dimethicone pool | 22.0% | 22.0% | MATCH* |
| Fill Temperature | 80.0°C | 80.0°C target | MATCH |
| Batch scale | virtual | 1.0 kg | 별도 관리 |
| QC prior | virtual only | actual fields empty | MATCH |

`*` Dimethicone 22%는 MQ carrier에서 들어오는 양을 포함하는 pool 개념이므로, 실제 MQ CoA 확인 후 direct-charge량을 다시 계산해야 한다.

P001 physical sheet는 이 carrier-offset을 실제 CoA 기준으로 재계산하도록 수정되었다. fileciteturn31file0

---

## 3. 가장 중요한 처방 불일치

### 3.1 Soothing Blend

Rev.7.3 baseline은 2% functional blend를 **Bisabolol + Stearyl Glycyrrhetinate + Tocopherol + Rosemary Extract**의 조합으로 정의하고 있다.

반면 과거 P001 execution sheet는 `Bisabolol+Tocopherol`이라는 두 성분 shorthand를 사용하고 있었다.

이것은 단순 표기 문제가 아니다. 실제 처방 성분이 달라질 수 있으므로 모델 입력과 실제 제조 처방 사이의 lineage가 끊길 수 있다.

현재 P001 sheet에서는 이 shorthand를 제거하고 **구성/공급사 확정 전에는 Soothing Blend를 미확정 상태로 유지**하도록 수정했다. 따라서 제조 전에 실제 구성과 Formula version을 확정해야 한다. fileciteturn31file0

---

## 4. MQ Resin / 원료 Grade 게이트

P001 sheet에는 특정 trade name 후보가 들어 있지만, Rev.7.3 자체가 MQ Resin의 실제 active %, carrier, INCI, grade를 제조 전에 확인하도록 요구한다.

따라서 다음을 실제 Lot 기준으로 확정한다.

- supplier
- trade name / grade
- INCI
- solids / active %
- carrier 종류
- density 또는 필요한 환산값
- CoA 번호
- lot number
- 실제 투입량

특히 MQ가 60% solids / 40% Dimethicone이라는 가정이 실제 CoA와 다르면 200 g 투입 및 Dimethicone 22% pool 계산을 그대로 사용할 수 없다.

**원료 CoA가 확정되기 전에는 P001을 제조하지 않는다.**

---

## 5. 공정 점검

현재 P001 sheet의 공정값은 다음을 **Initial Process Candidate**로 취급한다.

- melt target: 88°C
- powder dispersion: 2500 RPM
- dispersion duration: 25 min
- vacuum: -0.08 MPa / 5 min
- fill: 80°C
- mold preheat: 45°C
- cooling: target 2.5°C/min, 10°C chamber / 45 min
- demold core: 20°C
- conditioning: 25°C / 50% RH / 24h

이 값들은 Rev.7.3의 최종 확정 생산조건이 아니다. P001은 실제 장비에서 **target과 actual을 별도로 기록**해야 한다.

과거 `PILOT_EXPERIMENT_PROTOCOL_REV1.0.md`에는 3000 RPM × 20분 및 3-step cooling 등 다른 공정안이 존재한다. 이 과거 프로토콜은 현재 P001의 실행기준으로 사용하지 않는다. 과거 문서는 역사적 기록으로 보존한다.

현재 P001 sheet에는 실제 RPM, 실제 시간, 실제 온도, 실제 냉각 profile 및 deviation을 기록하도록 명시했다. fileciteturn31file0

---

## 6. Execution Order 점검

기존 18-run DOE template에서 P001의 random `Execution_Order`는 **14**였다. 이는 18개를 모두 제조하던 과거 randomization 계획의 값이다. fileciteturn35file0

현재 계획은 P001 하나만 먼저 제조하므로 이 숫자를 현재 제조 순서로 사용하지 않는다.

현재 의미는:

- P001 = **first physical GLIDE validation**
- 현재 physical execution order = **01 / first batch**
- 과거 randomization order `#14` = historical DOE metadata

따라서 과거 18-run template 자체는 역사적 설계표로 유지하고, 현재 P001 sheet에서 `#14`를 실행순서로 재사용하지 않는다.

---

## 7. Batch scale 점검

현재 P001 batch registration은 **1,000 g / 1.0 kg**이다. fileciteturn31file0

따라서 제조사가 100 g 또는 200 g lab batch만 가능하다고 제안하는 경우, 그것을 P001의 실제 데이터로 조용히 대체하지 않는다.

새 batch ID와 scale을 등록하고:

- scale change
- equipment change
- mixing/shear change
- heat-transfer difference
- fill/cooling difference

를 별도 기록한다.

P001을 1 kg에서 다른 scale로 바꾸려면 먼저 GLIDE의 batch definition 자체를 version update해야 한다.

---

## 8. QC 최소 요건

현재 physical sheet에 필요한 응답은 다음과 같이 정리했다.

### 필수
- Hardness raw replicates ×5
- Transfer payoff raw replicates ×3
- Drop point actual observation ×1 이상
- Glide/Friction CoF raw result 및 시험조건

### 개발 보조
- Appearance / powder bloom / agglomeration / cracking / sweating 기록 및 사진
- Density

Hardness와 Transfer는 숫자만 남기면 안 된다. 최소한 다음 시험조건을 고정해야 한다.

**Hardness**
- instrument ID
- probe
- penetration depth
- speed
- conditioning temperature/time
- sample geometry
- measurement location
- replicate count

**Transfer**
- substrate
- area
- applied load
- stroke count / speed
- contact time
- temperature
- conditioning
- replicate count

**CoF**
- substrate
- normal load
- sliding speed
- stroke/distance
- temperature/RH
- conditioning
- raw trace + summary statistic

**Drop Point**
- method/version
- instrument/cell
- heating rate
- sample preparation
- replicate rule

P001 sheet는 이 정보를 기록할 수 있도록 최소 필드를 보강했다. fileciteturn31file0

---

## 9. 제조사 handoff 조건

제조사에 전달하는 P001 technical handoff는 다음 원칙을 따른다.

### 반드시 전달
- 20 g solid stick target
- target composition / active basis
- P001 target process window
- required actual-process recording
- raw-material CoA / lot tracking requirement
- QC response definitions
- deviation recording
- yield / loss recording
- packaging compatibility check

### 제조사에게 자유도를 줄 수 있는 부분
- 실제 mixing vessel / homogenizer 모델
- heat-transfer 방식
- 냉각 장비
- 충전 nozzle
- 작업 순서의 장비별 미세 조정

단, 변경된 실제 조건은 반드시 기록하고, GLIDE target과 actual을 분리한다.

### 금지
- 사전 승인 없는 원료 substitution
- 다른 grade를 같은 material ID로 기록
- 실제값 대신 target값을 actual에 입력
- 제조사 샘플을 자동으로 GLIDE qualification data로 편입

---

## 10. Prediction snapshot gate

P001 제조 시작 전에 반드시 다음을 immutable snapshot으로 남긴다.

- model version
- code commit SHA
- feature/input values
- formulation version
- process target version
- prediction output
- uncertainty / confidence information, if available
- snapshot timestamp

그 후 실제 제조/측정이 진행된다.

실측 이후에는:

`Actual - Prediction = Residual`

을 계산한다.

예측값을 실제값에 맞춰 사후 수정하지 않는다.

---

## 11. P001 이후의 의사결정

P001 하나를 제조했다고 Production Model이 qualified 되는 것은 아니다.

P001 측정 후:

1. data integrity / lineage check
2. target vs actual process deviation check
3. prediction vs actual residual 계산
4. measurement uncertainty / repeatability 확인
5. model error pattern 확인
6. P001~P018 virtual candidate의 uncertainty / EIG 재계산
7. **두 번째 physical experiment가 정말 필요한지 판단**

필요하다고 판단될 때만 다음 physical candidate를 선정한다.

---

## 12. Final gate

### 현재
`CONDITIONAL READY — DO NOT MANUFACTURE YET`

### 제조 전 PASS 조건
- [ ] 원료 실제 Grade / Lot / CoA 확정
- [ ] MQ carrier / active basis 계산 확정
- [ ] Soothing Blend 구성 확정
- [ ] Formula version freeze
- [ ] P001 prediction snapshot 생성
- [ ] QC SOP version freeze
- [ ] 제조 scale / equipment 확인
- [ ] batch yield / loss 기록 양식 준비
- [ ] deviation log 준비
- [ ] packaging / fill compatibility 확인

### 제조 후
- [ ] raw data 보존
- [ ] actual process values 입력
- [ ] QC raw replicates 입력
- [ ] residual 계산
- [ ] EIG 재계산
- [ ] next experiment decision 기록

**핵심: 지금 P001은 '만들 준비가 끝난 제품'이 아니라, 마지막 제조 전 게이트를 통과시키면 바로 실행할 수 있는 첫 물리 검증 배치다.**
