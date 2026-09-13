# Public Web Evidence Saturation Matrix v0.1 — 2026-09-13

## Purpose

이 문서는 공개 웹 증거 수집을 무한 반복하지 않기 위한 **포화도(saturation) 관리판**이다.

목표는 각 failure cell에 대해 다음을 구분하는 것이다.

- **SEARCH**: 핵심 맥락이나 독립 사례가 부족하여 추가 탐색 필요
- **SATURATING**: 반복 신호가 형성되지만 반례/조건 차이가 더 필요
- **READY_FOR_TEST**: 공개 증거만으로 반복 가설이 충분히 형성되어 통제시험으로 이동 가능
- **SURVEY_GAP**: 공개 자료로 대표성·실제 행동·WTP 등을 답하기 어려워 1차조사가 필요
- **HOLD**: 현재 자료만으로 의사결정하기에는 정의 또는 인과관계가 불명확

이 상태값은 제품 성능의 우열이나 시장 규모를 의미하지 않는다.

---

## 1. Saturation rules

### 1.1 독립성

같은 원문을 재인용한 글, 동일 사건을 복제한 게시물, 동일 작성자의 반복 게시물은 독립 증거로 세지 않는다.

### 1.2 사례 수의 의미

소스 수는 **빈도/유병률/시장점유율의 추정치가 아니다.** 공개 웹 표본은 선택편향이 크므로, 사례 수는 오직 "이 failure context가 반복적으로 관찰되는가"를 판단하는 보조지표로 사용한다.

### 1.3 포화 판단

다음 5개 축에서 반복 신호가 확인되면 해당 cell은 READY_FOR_TEST 후보가 된다.

1. 서로 다른 출처/작성자의 반복 사례
2. 조건 차이에도 유지되는 핵심 failure mechanism 가설
3. 반례 또는 조건부 성공 사례의 존재 여부 파악
4. 제품 외 변수(garment/equipment/motion/environment) 분리 가능성
5. 측정 가능한 기술 질문으로 번역 가능

### 1.4 Survey Gap 판단

다음 질문은 공개 웹 자료를 더 모아도 대표적으로 답하기 어렵기 때문에 SURVEY_GAP로 분리한다.

- 실제 한국 러너에서의 발생률/비율
- 세그먼트별 반복 실패 비율
- 실제 구매 빈도와 연간 지출
- 가격 민감도/WTP
- 특정 해결책의 대표적 선호도
- switching threshold의 정량화

---

## 2. Failure-cell saturation matrix

| Failure cell | 반복 공개 신호 | 반례/불확실성 | 한국 자료 | 기술시험 후보 | 상태 | 다음 액션 |
|---|---|---|---|---|---|---|
| Inner thigh / groin | 강함 | 제품·속옷·inseam·시간 영향 혼재 | 있음 | sweat/water + garment motion + time-to-failure | READY_FOR_TEST | incumbent matched test |
| Sports bra / under-breast / band | 강함 | fit, bra geometry, tape가 개입 | 있음/부분적 | body-area + garment motion + reapplication | READY_FOR_TEST | 별도 anatomical cell 시험 |
| Waistband / hip | 중간~강함 | garment fit와 제품 효과 분리 필요 | 있음/부분적 | seam/garment migration | SATURATING | targeted web search + test design |
| Nipple / chest | 중간 | tape와 topical의 역할이 다름 | 부분적 | adhesive vs topical durability/compatibility | SATURATING | failure-context 보강 후 시험 |
| Intergluteal / perineal | 강함 | 해부학·의류·땀 조건 영향 | 있음/부분적 | sweat/water + motion + reachability | READY_FOR_TEST | incumbent matched test |
| Pack / hydration vest back | 강함 | equipment가 원인일 수 있음 | 있음 | equipment-induced garment motion | READY_FOR_TEST | equipment interaction test |
| Shoulder / strap interface | 중간 | vest/pack geometry 의존 | 부분적 | strap pressure/motion + textile friction | SATURATING | 독립 사례 추가 |
| Foot / blister-prone areas | 중간 | anti-chafe와 blister 관리가 다른 문제일 수 있음 | 부족 | textile/skin friction + moisture | HOLD | category boundary 먼저 정의 |
| Seam-created focal friction | 강함 | body area마다 결과 다름 | 있음 | seam/textile friction | READY_FOR_TEST | matched textile test |
| Garment migration / ride-up | 강함 | 제품 실패가 아닌 apparel failure일 수 있음 | 있음 | garment-motion test | READY_FOR_TEST | system-level test |
| Heavy sweat / wash-off | 강함 | 일부 사용자는 장시간 성공 | 있음 | sweat/water persistence | READY_FOR_TEST | matched persistence test |
| Heat / humidity | 강함 | 표준 임계값 없음 | 부분적 | temperature/humidity matrix | READY_FOR_TEST | controlled environment test |
| Reapplication burden | 강함 | 실제 빈도는 정량화 불가 | 부분적 | application/reapplication UX | READY_FOR_TEST | prototype UX protocol |
| Reachability | 중간~강함 | anatomy/mobility 차이 | 부분적 | self-application reachability | READY_FOR_TEST | format prototype test |
| Greasy / wet feel | 강함 | 주관성·개인차 큼 | 부분적 | standardized sensory panel | SATURATING | sensory instrument 설계 |
| Odor | 중간 | 제품·땀 상호작용 추정 수준 | 부족 | odor/sensory panel | HOLD | 더 강한 evidence가 있을 때 재평가 |
| Textile transfer / staining | 강함 | 실제 material test 부재 | 있음/부분적 | transfer/staining bench test | READY_FOR_TEST | incumbent textile test |
| Carryability | 중간~강함 | event logistics에 좌우 | 부분적 | carry/reapplication UX | SATURATING | 대표 format 비교 |
| Product ranking / incumbent preference | 강함 | 상반된 사용자 경험 다수 | 부분적 | blind/matched incumbent comparison | READY_FOR_TEST | petroleum jelly + leading formats |

---

## 3. Cross-variable saturation

| Variable | 상태 | 판단 |
|---|---|---|
| Time / duration | READY_FOR_TEST | 장시간 실패와 장시간 성공이 모두 관찰되어 controlled comparison 가치가 높음 |
| Sweat / water | READY_FOR_TEST | wash-off 관련 반복 신호와 반례가 충분히 존재 |
| Heat / humidity | READY_FOR_TEST | 위험 맥락은 반복되지만 임계값은 미확정 |
| Garment fit / migration | READY_FOR_TEST | 제품 외 원인 가능성이 반복적으로 확인됨 |
| Seams | READY_FOR_TEST | focal friction 가설이 반복되고 측정 가능 |
| Reapplication | READY_FOR_TEST | 장거리 운영 변수로 반복 관찰됨 |
| Reachability | READY_FOR_TEST | format 선택에 영향을 주는 사례가 반복됨 |
| Sensory / cleanup | SATURATING | switching 변수로는 충분하지만 표준화된 측정 구조가 필요 |
| Transfer / staining | READY_FOR_TEST | 반복되는 불만이 있고 객관적 bench test로 번역 가능 |
| Carryability | SATURATING | 반복 신호는 있으나 event format별 차이 큼 |
| Skin compatibility | SURVEY_GAP + TECHNICAL_OPEN | 공개 웹만으로 안전성/적합성을 판단할 수 없음; 별도 compatibility screening 필요 |
| Recovery | SURVEY_GAP + TECHNICAL_OPEN | prevention과 recovery가 별도 JTBD임은 확인되지만 제품 설계 근거는 부족 |
| Price / WTP | SURVEY_GAP | 공개 웹만으로 대표적인 가격 민감도 산출 불가 |

---

## 4. What is now saturated enough to stop broad web searching

현재 다음 영역은 동일한 일반론을 반복 수집하는 것보다 **통제시험 설계/실험 준비가 더 가치가 높다.**

1. 장시간 persistence / time-to-failure
2. heavy sweat / water persistence
3. heat/humidity interaction
4. garment migration / seam friction
5. sports-bra anatomical cell
6. pack/hydration-vest interaction
7. reapplication/application burden
8. reachability
9. textile transfer/staining
10. incumbent preference contradiction

이는 해당 제품이 우수하다는 뜻이 아니라, **반복 가설이 시험 가능한 수준까지 구체화되었다**는 뜻이다.

---

## 5. Where targeted web searching is still justified

### A. Anatomical gaps

- nipple/chest
- shoulder/strap
- waistband/hip
- Korean female runner-specific contexts
- sensitive-skin reactions

### B. Category-boundary gaps

- foot/blister 영역이 anti-chafe product와 동일한 제품 문제인지 여부
- recovery use-case와 prevention use-case의 실제 행동 차이

### C. Korean/local gaps

한국 러너의 실제 사용 맥락을 더 찾는 것은 의미가 있지만, 이를 공개 웹 사례 수로 대표성 있는 비율로 변환해서는 안 된다.

---

## 6. Survey should not duplicate the web dataset

1차조사는 다음처럼 **웹 자료로 답할 수 없는 질문**에 집중한다.

- 한국 러너 중 각 failure cell을 실제로 경험하는 비율
- distance/time/sex/anatomy/weather segment별 차이
- 현재 사용 제품과 실제 재구매/교체 행동
- 연간 지출
- 가격 민감도와 WTP
- 제품 성능이 같을 때 switching을 일으키는 UX 조건
- topical / tape / apparel / equipment solution의 실제 선택 비율

웹에서 이미 반복적으로 확인된 "어떤 상황에서 어떤 문제가 생길 수 있는가"를 설문에서 다시 장황하게 묻는 것은 피한다.

---

## 7. Technical test handoff

READY_FOR_TEST cell은 `technical_validation_matrix_v0.1.md`와 연결한다.

권장 우선순위:

### T1 — Matched incumbent persistence
- petroleum jelly
- leading stick/balm incumbent
- 필요 시 additional specialized format
- sweat/water + time 조건

### T2 — Garment/system interaction
- seam
- migration
- compression/long inseam
- sports bra
- hydration vest/pack

### T3 — Environment
- temperature
- humidity
- sweat/water load

### T4 — UX
- application time
- reachability
- reapplication
- carryability
- sensory/cleanup

### T5 — Transfer
- representative textile/materials
- visible residue/staining scoring

수치 기준은 기존 원칙대로 baseline과 method variance를 먼저 확보한 뒤 설정한다.

---

## 8. Evidence boundary

이 문서는 공개 웹 사례의 **반복성·조건성·시험 가능성**을 관리하는 문서이지 다음을 주장하는 문서가 아니다.

- 객관적 friction reduction
- 정확한 지속시간
- 특정 제품의 우월성
- 임상적 예방/치료 효과
- 한국 시장 prevalence
- 대표적 WTP
- 규제상 효능/의약적 claim 적격성

모든 제품 요구사항은 최종적으로 evidence ID 또는 controlled test ID와 연결해야 한다.

---

## 9. Next gate

현재 연구 단계의 핵심 질문은 **"더 많은 사례가 필요한가?"가 아니라 "어떤 cell은 시험으로 넘길 만큼 포화되었고, 어떤 cell만 추가 조사해야 하는가?"**이다.

따라서 다음 작업 순서는:

1. READY_FOR_TEST cell의 incumbent test protocol 작성
2. SATURATING cell에만 제한적 추가 web search
3. SURVEY_GAP를 field instrument에 연결
4. HOLD cell은 정의가 명확해질 때까지 제품 요구사항에서 제외
5. 각 technical result를 다시 evidence registry/decision log에 연결
