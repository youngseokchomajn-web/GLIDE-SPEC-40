"""
Unit tests for GEM Task Executor
Validates task loading, state machine transitions, attempt limits, and actionability boundaries.
"""

import os
import sys
import pytest

AGENT_SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".agent", "scripts"))
if AGENT_SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, AGENT_SCRIPTS_DIR)

from execute_gem_task import (
    load_gem_task,
    save_gem_task,
    execute_task,
    find_next_pending_task,
)


class TestGemTaskExecutor:

    def test_non_actionable_tasks_are_skipped(self):
        """Verifies that ACKNOWLEDGED_STOP / is_actionable=False tasks are strictly not executed."""
        # Existing seed tasks GEM-TASK-002 (REJECT) and GEM-TASK-003 (APPROVE)
        task_002 = ".agent/queue/gem_tasks/GEM-TASK-002.yaml"
        task_003 = ".agent/queue/gem_tasks/GEM-TASK-003.yaml"

        if os.path.exists(task_002):
            success, reason = execute_task(task_002)
            assert success is False
            assert reason == "NOT_ACTIONABLE"

        if os.path.exists(task_003):
            success, reason = execute_task(task_003)
            assert success is False
            assert reason == "NOT_ACTIONABLE"

    def test_actionable_dummy_task_lifecycle(self, tmp_path):
        """Validates state machine transitions for an actionable EXPERIMENT task in dry_run."""
        dummy_task = tmp_path / "GEM-TASK-TEST-001.yaml"
        dummy_task.write_text("""task_id: "GEM-TASK-TEST-001"
source_orc_id: "ORC-TEST-001"
source_orc_commit: "0123456789abcdef0123456789abcdef01234567"
source_decision_file: "analysis/commits/ORC-TEST-001.md"
decision: "EXPERIMENT"
status: "PENDING"
is_actionable: true
attempt: 1
max_attempts: 3
created_at: "2026-09-13T12:00:00+09:00"
next_agent: "GEM"
rationale: "Execute dummy test"
required_actions:
  - "Run test suite"
acceptance_criteria:
  - "Test suite passes"
""")

        # Execute in dry run
        success, reason = execute_task(str(dummy_task), dry_run=True)
        assert success is True
        assert reason == "DRY_RUN_SUCCESS"

        # Now test real execution of this dummy task
        success_real, reason_real = execute_task(str(dummy_task), dry_run=False)
        assert success_real is True
        assert reason_real == "TASK_COMPLETED"

        # Verify task is now EVIDENCE_CREATED
        td = load_gem_task(str(dummy_task))
        assert td["status"] == "EVIDENCE_CREATED"
        assert "completed_at" in td
        # Ensure ORC rationale/actions were preserved exactly
        assert td["decision"] == "EXPERIMENT"
        assert td["rationale"] == "Execute dummy test"

    def test_max_attempts_guardrail_blocks_task(self, tmp_path):
        """Validates that a task exceeding max_attempts=3 transitions to BLOCKED."""
        exhausted_task = tmp_path / "GEM-TASK-EXHAUSTED.yaml"
        exhausted_task.write_text("""task_id: "GEM-TASK-EXHAUSTED"
source_orc_id: "ORC-EXHAUSTED"
source_orc_commit: "abcdefabcdefabcdefabcdefabcdefabcdefabcd"
source_decision_file: "analysis/commits/ORC-EXHAUSTED.md"
decision: "FIX_REQUIRED"
status: "PENDING"
is_actionable: true
attempt: 4
max_attempts: 3
created_at: "2026-09-13T12:00:00+09:00"
next_agent: "GEM"
rationale: "Failing bug fix"
required_actions:
  - "Fix syntax error"
acceptance_criteria:
  - "Zero errors"
""")

        success, reason = execute_task(str(exhausted_task))
        assert success is False
        assert reason == "MAX_ATTEMPTS_EXCEEDED"

        td = load_gem_task(str(exhausted_task))
        assert td["status"] == "BLOCKED"
        assert td["failure_reason"] == "Max attempts exceeded"
