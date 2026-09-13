# Regression & Negative Result Registry

**Purpose:**  
본 문서는 모델 개선 실험 중 발생한 성능 저하(Regression), Ablation 실패, 음성 결과(Negative Results)를 영구 보존하는 레지스트리입니다.
프로토콜 원칙에 따라 성공한 결과뿐만 아니라 실패한 실험도 일체 은폐하거나 삭제하지 않고 원인과 함께 추적 기록합니다.

---

## Registry Entries

*(현재 등록된 회귀 내역 없음 - 시스템 초기화 상태)*

### Entry Format Template:
- **Date / Commit:** `YYYY-MM-DD` (`GEM-XXX` / `ORC-YYY`)
- **Hypothesis:** 검증하고자 했던 가설 또는 변경 사항
- **Observed Degradation:** 저하된 지표 (예: 특정 도메인 RMSE 증가, PI Coverage 붕괴 등)
- **Root Cause Analysis:** 물리적/통계적 원인 (예: 특정 점증제 영역에서 외삽 오류)
- **ORC Determination:** `REJECT` 또는 `DATA_REQUIRED` 사유
- **Action Taken / Retained Evidence:** 채택 폐기 및 회귀 방지 테스트 케이스 추가 여부
