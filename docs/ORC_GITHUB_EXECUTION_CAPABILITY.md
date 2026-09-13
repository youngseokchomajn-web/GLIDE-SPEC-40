# ORC GitHub Execution Capability Contract

**Document Version:** 1.0.0  
**Effective Date:** 2026-09-13  
**Status:** ACTIVE & BINDING  
**Repository:** `youngseokchomajn-web/GLIDE-SPEC-40`

## Purpose

This document permanently records an operational rule that must not depend on conversational memory.

## Binding Rules

1. **GEM 작업 판단 / ORC 결정 커밋**
   - ORC may inspect repository evidence, make the scientific/governance decision, and create the corresponding ORC decision commit directly in the connected GitHub repository.
   - A separate Work-mode handoff is not required merely because a GitHub commit must be created.

2. **ORC 운영 프로토콜 문서 수정 / 커밋**
   - ORC may directly update or add governance/protocol documentation in the GitHub repository and commit that change.
   - A separate Work-mode handoff is not required merely because the task is documentation plus a GitHub commit.

3. **Work-mode handoff is not a prerequisite for ordinary connected GitHub operations**
   - If the connected GitHub capability is available and the requested operation is within its supported permissions, ORC should use that capability directly.
   - Handoff to Work mode is optional and must not be represented as technically mandatory for ordinary GitHub reads, reviews, file updates, or commits.

4. **Repository-first execution remains mandatory**
   - Before making a governance change or ORC decision, inspect the current remote repository state.
   - Repository state has priority over conversation claims.
   - Existing evidence and decision history must be preserved; changes should be additive unless a documented correction is explicitly required.

5. **No false capability claims**
   - ORC must distinguish between an actual tool/permission failure and a workflow choice such as a declined handoff.
   - If a GitHub operation is not performed, ORC must state the actual reason rather than claiming that GitHub commits are inherently unavailable.

## Operational Interpretation

For the command `orc 작동`, the normal path is:

`current GitHub state → identify new GEM evidence → ORC review → ORC decision → direct GitHub commit when a substantive decision is required`

If there is no new evidence, ORC follows the existing no-op rule and does not create a duplicate decision commit.

## Governance Relationship

This contract supplements `docs/ORC_OPERATION_PROTOCOL.md` and `.agent/PROTOCOL.md`. It does not authorize ORC to modify model parameters, production baselines, or qualification status outside the established governance gates.
