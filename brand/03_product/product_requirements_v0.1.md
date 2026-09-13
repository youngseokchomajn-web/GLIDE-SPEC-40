# Product Requirements — v0.1

## Purpose

이 문서는 선택된 첫 제품 beachhead인 **S1 — long-duration inner-thigh/groin skin–garment interface protection**을 실제 제품 개발 언어로 번역하기 위한 formulation-neutral 요구사항이다.

제품의 formula, ingredient, format을 결정하는 문서가 아니다. 먼저 **누구의 어떤 상황에서 무엇이 실패하는가**를 고정하고, 이후 후보 제형과 제조 파트너가 이 요구사항을 얼마나 잘 충족할 수 있는지 비교하기 위한 기준선이다.

## 1. Target use scenario

### Primary user

- marathon / ultra / long-duration runner
- 반복적인 달리기에서 피부–의류 접촉 문제가 재현되는 사용자
- 단거리의 일회성 불편보다 장시간 활동에서 보호 유지가 중요한 사용자

### Primary scenario

장시간 러닝 중 inner-thigh/groin 주변에서 반복 움직임, 땀/습기, 의류 접촉이 동시에 발생하여 기존 피부 보호 루틴이 충분하지 않거나 유지·재도포가 번거로워지는 상황.

### Important boundary

특정 해부학 부위를 영구적인 SKU 범위로 확정하지 않는다. S1은 현재 beachhead scenario이며, 이후 실제 사용성과 시장성을 검증하면서 인접 interface로 확장 가능하다.

## 2. Problem definition

제품이 해결해야 할 핵심 문제는 단순한 'chafing 제거'가 아니다.

**장시간 움직이는 피부–의류 interface에서 보호 상태가 유지되지 않거나, 기존 보호 방법을 계속 사용하는 것이 불편해지는 문제.**

따라서 제품 요구사항은 다음 failure modes를 중심으로 정의한다.

1. protective film / friction protection의 시간 경과에 따른 변화
2. sweat / moisture 환경에서의 보호 상태 변화
3. 반복 움직임에 따른 interface 변화
4. garment contact, migration, seam interaction
5. application / reapplication의 번거로움
6. greasy/wet feel 등 sensory trade-off
7. transfer / staining / cleanup 부담
8. carryability 및 실제 운동 중 접근성

## 3. Must-address requirements

후보 제품은 최소한 다음 질문에 답할 수 있어야 한다.

| Requirement | 개발 질문 | 현재 확정 수준 |
|---|---|---|
| Friction protection | 반복 움직임 중 피부 보호 기능을 어떻게 유지하는가? | 요구사항 |
| Persistence | 장시간 사용에서 보호 상태가 어떻게 변화하는가? | 요구사항, exact duration 미정 |
| Sweat/moisture tolerance | 땀/습기 조건에서 제품 거동은 어떤가? | 요구사항 |
| Garment compatibility | 의류와 접촉했을 때 migration/transfer 문제는 어떤가? | 요구사항 |
| Reapplication practicality | 재도포가 필요하다면 얼마나 현실적인가? | 요구사항 |
| Sensory | 사용자가 실제 운동 전에/중에 받아들일 수 있는 감촉인가? | 요구사항 |
| Cleanup | 운동 후 제거·세척 부담은 어느 정도인가? | 요구사항 |
| Portability | 휴대·보관·운동 중 사용이 가능한가? | 요구사항 |
| Skin compatibility | 반복 사용을 전제로 한 피부 적합성은 어떤가? | 요구사항 |

## 4. Nice-to-have requirements

다음은 경쟁력 후보이지만 현재 핵심 요구사항보다 우선순위가 낮다.

- 빠른 application
- 적은 양으로 넓은 interface coverage
- 운동 중에도 손쉽게 재도포 가능한 UX
- 의류 오염 최소화
- 다양한 body-area로의 확장성
- 여행/레이스 키트와 결합하기 쉬운 portability

## 5. Requirements that must NOT be assumed

현재 evidence만으로 다음을 제품 사양으로 확정하지 않는다.

- '몇 시간 지속'
- '몇 km까지 보호'
- 기존 특정 브랜드보다 오래 지속
- Vaseline보다 우수
- sweat-proof / waterproof라는 절대적 표현
- 특정 ingredient가 핵심 해결책이라는 가정
- stick이 최적 format이라는 가정
- 특정 anatomy만을 대상으로 한다는 가정
- clinical/medical efficacy

이 항목들은 필요할 경우 후속 기술 검증 또는 규제 검토의 대상이다.

## 6. Format-neutral decision criteria

후보 format은 제품 컨셉 이후에 비교한다.

### A. Stick

- application/reapplication 편의성
- 휴대성
- 직접 도포 가능성
- 접촉 면적과 도포량 제어
- 용기/충전/안정성

### B. Balm / semi-solid

- film formation 가능성
- spreadability
- 손 또는 직접 도포 UX
- migration/greasiness
- 충전 및 온도 안정성

### C. Cream / emulsion

- spreadability
- skin feel
- sweat/moisture 조건에서의 거동
- packaging compatibility
- 반복 사용성

### D. Gel / other

- 빠른 spread/application
- residue
- film behavior
- sweat/moisture interaction
- 실제 endurance use suitability

**선택 원칙:** format의 장점보다 S1 scenario의 failure mode를 먼저 평가한다.

## 7. What to ask manufacturers/OEMs

초기 업체 접촉에서는 '이런 제품 만들어 주세요'가 아니라 아래 정보를 받아야 한다.

### Product development capability

- anti-chafe / friction-protection / sports or outdoor skin-care 개발 경험
- 장시간 운동용 제품 개발 경험
- sweat/moisture 및 garment interaction을 고려한 제형 개발 경험
- stick/balm/emulsion/gel 등 복수 format의 개발 가능 여부

### Formulation capability

- film-forming / protective-barrier 설계 경험
- sensory tuning 경험
- transfer/staining 저감 경험
- 반복 도포용 피부 적합성 평가 경험
- 온도 변화에 따른 제형 안정성 확보 경험

### Testing capability

- 기본 안정성 시험
- 미생물/보존력 관련 시험
- 피부 안전성 관련 시험 연계
- friction / wear / film-retention을 평가할 수 있는 외부 시험기관 연계
- 필요 시 실제 사용성/사용시험 설계 지원

### Manufacturing capability

- MOQ
- 샘플/파일럿 생산 가능 여부
- 충전 가능한 format 및 용기 범위
- 생산 lead time
- 원료 sourcing 범위
- scale-up 경험
- GMP/품질관리 체계

### Regulatory / commercialization support

- 국내 화장품 제조·책임판매 관련 지원 범위
- 표시·광고 문구 검토 지원 여부
- 기능성화장품 해당 가능성 검토를 위한 지원 범위
- 수출 대상국 대응 경험

## 8. Contact sequence

업체는 한 종류만 찾지 않는다. 다음 순서로 병렬 탐색한다.

### Track 1 — Full-service cosmetic OEM/ODM

목적: 실제 제조 가능성, MOQ, 개발기간, format 선택지, 개발비 파악.

### Track 2 — Specialized formulation / R&D partner

목적: S1의 friction/protective-film problem을 기술적으로 구현할 수 있는지 확인.

### Track 3 — Independent testing laboratory

목적: OEM이 제시하는 '가능하다'를 객관적인 시험 설계로 연결.

### Track 4 — Packaging supplier

목적: format 결정 이후 용기/도포 UX/휴대성을 최적화. 초기에는 정보 수집 수준으로 접근.

### Track 5 — Raw-material / ingredient supplier

목적: 특정 원료를 먼저 고르는 것이 아니라 후보 기능군과 기술자료를 파악. formulation partner의 요구가 구체화된 뒤 심화한다.

## 9. First contact package

업체에 처음 전달할 자료는 다음 5개로 제한한다.

1. **One-page product concept** — S1 scenario와 사용자 문제
2. **Product requirements v0.1** — 본 문서
3. **Do-not-assume list** — exact duration/ superiority/ingredient/format 미확정
4. **Development questions** — 개발 가능 format, MOQ, 샘플, 시험, lead time
5. **Evidence boundary** — public web/community evidence는 concept discovery용이며 객관적 성능 우위의 증거가 아님

## 10. Vendor comparison scorecard

업체를 단순히 '유명한가'로 평가하지 않는다.

1–5점으로 기록한다.

- S1 problem 이해도
- formulation capability
- protective-film 관련 경험
- sensory tuning capability
- testing 연계력
- sample iteration speed
- MOQ
- 개발비
- 예상 단가
- 생산 scale-up
- regulatory support
- export support
- communication / documentation quality

점수 자체가 자동 선정 기준은 아니다. 업체의 강점·약점·제약조건을 함께 기록한다.

## 11. Next technical gate

업체 접촉 후 바로 formula를 채택하지 않는다.

다음 순서로 좁힌다.

**S1 requirement → vendor capability → format candidates → formulation hypotheses → prototype → technical validation**

Prototype 단계에서 처음으로 구체적인 formula/ingredient 조합을 비교한다.

## Status

**Formulation-neutral product requirement baseline — active.**

S1 beachhead는 선택됐지만 formula, ingredient, format, exact duration, superiority claim은 아직 결정되지 않았다.
