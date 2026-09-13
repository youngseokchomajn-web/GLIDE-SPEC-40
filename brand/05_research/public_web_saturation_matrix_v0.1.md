# Public Web Evidence Saturation Matrix v0.1 — 2026-09-13

## Purpose

이 문서는 공개 웹 증거 수집을 무한 반복하지 않기 위한 **포화도(saturation) 관리판**이다.

핵심 원칙은 **Global-first, Korea-localization**이다.

- 공개 웹 데이터는 국가로 제한하지 않는다.
- 글로벌 자료는 failure mode와 조건의 폭을 발견하고 반복 가설을 만드는 주 데이터층이다.
- 한국 자료는 글로벌 가설을 한국 러너/기후/사용행동/가격/유통/규제 맥락에서 검증하는 별도 localization layer다.
- 한국 자료가 부족하다고 글로벌 failure mode를 버리지 않는다.
- 반대로 글로벌 사례를 한국 시장의 prevalence나 선호도로 일반화하지 않는다.

최근 endurance-athlete 피부 문헌도 러너, 울트라러너, 트라이애슬론, 사이클리스트를 포괄하며 반복적 기계 부하, 땀, 의복/장비의 occlusion, 열·수분 노출 등을 공통 exposure 축으로 다룬다. 이는 국가보다 **운동 환경과 failure mechanism**을 우선 축으로 삼는 현재 연구 구조와 부합한다. citeturn0search0turn0search3

목표는 각 failure cell에 대해 다음을 구분하는 것이다.

- **SEARCH**: 핵심 맥락이나 독립 사례가 부족하여 추가 탐색 필요
- **SATURATING**: 반복 신호가 형성되지만 반례/조건 차이가 더 필요
- **READY_FOR_TEST**: 공개 증거만으로 반복 가설이 충분히 형성되어 통제시험으로 이동 가능
- **SURVEY_GAP**: 공개 자료로 대표성·실제 행동·WTP 등을 답하기 어려워 1차조사가 필요
- **HOLD**: 현재 자료만으로 의사결정하기에는 정의 또는 인과관계가 불명확

이 상태값은 제품 성능의 우열이나 시장 규모를 의미하지 않는다.

---

## 1. Evidence architecture

### Layer G — Global discovery

국가 제한 없이 다음을 수집한다.

- 러닝/울트라/트라이애슬론/사이클링 커뮤니티
- 스포츠의학/피부과 문헌
- 제품 리뷰 및 사용 경험
- 공개 포럼/인터뷰/장거리 운동 사례
- 다양한 기후·거리·운동 장비 맥락

목적:

1. failure mode 발견
2. 조건 변수 발견
3. 반례/상반된 경험 보존
4. 기술시험 가설 생성

### Layer K — Korea localization

한국 자료는 별도 태그로 유지한다.

- 한국 러너의 실제 사용 맥락
- 한국의 계절/고온다습/저온건조 등 환경
- 국내 제품/유통/가격
- 한국 러너의 구매·재구매·switching 행동
- 한국 규제 및 claim 환경

목적은 **글로벌 failure mode를 한국에서 다시 발견하는 것 자체가 아니라, 한국에서의 relevance와 market/product context를 검증하는 것**이다.

### Layer T — Technical validation

글로벌/한국 어느 쪽에서 발견되었는지와 관계없이 반복 가설을 controlled test로 이동시킨다.

---

## 2. Saturation rules

### 2.1 독립성

같은 원문을 재인용한 글, 동일 사건을 복제한 게시물, 동일 작성자의 반복 게시물은 독립 증거로 세지 않는다.

### 2.2 국가 수와 사례 수의 의미

국가 수나 소스 수는 **빈도/유병률/시장점유율의 추정치가 아니다.** 공개 웹 표본은 선택편향이 크므로, 사례 수와 국가 다양성은 오직 "이 failure context가 서로 다른 환경에서도 반복적으로 관찰되는가"를 판단하는 보조지표로 사용한다.

### 2.3 포화 판단

다음 5개 축에서 반복 신호가 확인되면 해당 cell은 READY_FOR_TEST 후보가 된다.

1. 서로 다른 출처/작성자의 반복 사례
2. 서로 다른 지역/환경에서도 유지되는 핵심 failure mechanism 가설
3. 반례 또는 조건부 성공 사례의 존재 여부 파악
4. 제품 외 변수(garment/equipment/motion/environment) 분리 가능성
5. 측정 가능한 기술 질문으로 번역 가능

### 2.4 Survey Gap 판단

다음 질문은 공개 웹 자료를 더 모아도 대표적으로 답하기 어렵기 때문에 SURVEY_GAP로 분리한다.

- 실제 한국 러너에서의 발생률/비율
- 세그먼트별 반복 실패 비율
- 실제 구매 빈도와 연간 지출
- 가격 민감도/WTP
- 특정 해결책의 대표적 선호도
- switching threshold의 정량화

---

## 3. Failure-cell saturation matrix

| Failure cell | Global signal | Geographic diversity | Contradiction / uncertainty | Korea evidence | Technical test candidate | Status | Next action |
|---|---|---|---|---|---|---|---|
| Inner thigh / groin | Strong | Multi-region | Product·underwear·inseam·time effects mixed | 있음 | sweat/water + garment motion + time-to-failure | READY_FOR_TEST | incumbent matched test |
| Sports bra / under-breast / band | Strong | Multi-region | fit, bra geometry, tape involved | 있음/부분적 | body-area + garment motion + reapplication | READY_FOR_TEST | separate anatomical-cell test |
| Waistband / hip | Moderate–strong | Multi-region | garment fit and product effect need separation | 있음/부분적 | seam/garment migration | SATURATING | targeted global search + test design |
| Nipple / chest | Moderate | Multi-region | tape and topical have different roles | 부분적 | adhesive vs topical durability/compatibility | SATURATING | strengthen failure-context evidence |
| Intergluteal / perineal | Strong | Multi-region | anatomy·garment·sweat interaction | 있음/부분적 | sweat/water + motion + reachability | READY_FOR_TEST | incumbent matched test |
| Pack / hydration vest back | Strong | Multi-region | equipment may be causal | 있음 | equipment-induced garment motion | READY_FOR_TEST | equipment interaction test |
| Shoulder / strap interface | Moderate | Multi-region | vest/pack geometry dependent | 부분적 | strap pressure/motion + textile friction | SATURATING | add independent cases |
| Foot / blister-prone areas | Moderate | Multi-region | blister management may be a different category | 부족 | textile/skin friction + moisture | HOLD | define category boundary first |
| Seam-created focal friction | Strong | Multi-region | body-area dependent | 있음 | seam/textile friction | READY_FOR_TEST | matched textile test |
| Garment migration / ride-up | Strong | Multi-region | may be apparel failure, not product failure | 있음 | garment-motion test | READY_FOR_TEST | system-level test |
| Heavy sweat / wash-off | Strong | Multi-region | some users report long-duration success | 있음 | sweat/water persistence | READY_FOR_TEST | matched persistence test |
| Heat / humidity | Strong | Multi-region | no standardized threshold | 부분적 | temperature/humidity matrix | READY_FOR_TEST | controlled environment test |
| Reapplication burden | Strong | Multi-region | actual frequency not quantifiable from anecdotes | 부분적 | application/reapplication UX | READY_FOR_TEST | prototype UX protocol |
| Reachability | Moderate–strong | Multi-region | anatomy/mobility differences | 부분적 | self-application reachability | READY_FOR_TEST | format prototype test |
| Greasy / wet feel | Strong | Multi-region | subjective and individual | 부분적 | standardized sensory panel | SATURATING | sensory instrument design |
| Odor | Moderate | Limited/mixed | product·sweat interaction mostly inferred | 부족 | odor/sensory panel | HOLD | re-evaluate if stronger evidence appears |
| Textile transfer / staining | Strong | Multi-region | material-test evidence limited | 있음/부분적 | transfer/staining bench test | READY_FOR_TEST | incumbent textile test |
| Carryability | Moderate–strong | Multi-region | event logistics vary | 부분적 | carry/reapplication UX | SATURATING | representative format comparison |
| Product ranking / incumbent preference | Strong | Multi-region | strong contradictory user experiences | 부분적 | blind/matched incumbent comparison | READY_FOR_TEST | petroleum jelly + leading formats |

**주의:** `Multi-region`은 prevalence나 시장 크기를 의미하지 않는다. 단지 동일한 failure context가 서로 다른 지역의 공개 사례에서 관찰되었다는 뜻이다.

---

## 4. Cross-variable saturation

| Variable | Status | Judgment |
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

## 5. What is now saturated enough to stop broad web searching

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

## 6. Where targeted web searching is still justified

### A. Anatomical gaps

- nipple/chest
- shoulder/strap
- waistband/hip
- Korean female runner-specific contexts
- sensitive-skin reactions

### B. Category-boundary gaps

- foot/blister 영역이 anti-chafe product와 동일한 제품 문제인지 여부
- recovery use-case와 prevention use-case의 실제 행동 차이

### C. Geographic gaps

지역은 기본적으로 제한하지 않는다. 다만 특정 지역이 실제 제품/기후/규제 결정에 중요할 경우 별도 localization cell로 수집한다.

우선순위는 필요에 따라:

1. Korea
2. Japan
3. North America
4. Europe
5. Australia/New Zealand
6. 기타 endurance-running 시장

순으로 둘 수 있으나, **이 순서는 데이터 품질이나 중요도의 서열이 아니라 localization 작업의 운영 순서일 뿐이다.**

---

## 7. Survey should not duplicate the global web dataset

1차조사는 다음처럼 **공개 웹 자료로 대표적으로 답할 수 없는 질문**에 집중한다.

- 한국 러너 중 각 failure cell을 실제로 경험하는 비율
- distance/time/sex/anatomy/weather segment별 차이
- 현재 사용 제품과 실제 재구매/교체 행동
- 연간 지출
- 가격 민감도와 WTP
- 제품 성능이 같을 때 switching을 일으키는 UX 조건
- topical / tape / apparel / equipment solution의 실제 선택 비율

글로벌 웹에서 이미 반복적으로 확인된 "어떤 상황에서 어떤 문제가 생길 수 있는가"를 설문에서 다시 장황하게 묻는 것은 피한다.

---

## 8. Technical test handoff

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

## 9. Evidence boundary

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

## 10. Next gate

현재 연구 단계의 핵심 질문은 **"더 많은 사례가 필요한가?"가 아니라 "어떤 cell은 시험으로 넘길 만큼 포화되었고, 어떤 cell만 추가 조사해야 하는가?"**이다.

따라서 다음 작업 순서는:

1. READY_FOR_TEST cell의 incumbent test protocol 작성
2. SATURATING cell에만 제한적 추가 web search
3. SURVEY_GAP를 field instrument에 연결
4. HOLD cell은 정의가 명확해질 때까지 제품 요구사항에서 제외
5. 각 technical result를 다시 evidence registry/decision log에 연결
