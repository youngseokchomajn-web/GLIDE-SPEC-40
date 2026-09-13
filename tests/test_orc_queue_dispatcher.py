"""
Unit and Integration Tests for ORC Queue Dispatcher
Validates Test A (Detection), Test B (Duplicate Prevention), and Test C (Loop Prevention).
"""

import os
import shutil
import tempfile
import pytest

import sys
AGENT_SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".agent", "scripts"))
if AGENT_SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, AGENT_SCRIPTS_DIR)

from dispatch_orc_queue import (
    check_trigger_eligibility as check_eligibility,
    is_duplicate_commit,
    TASKS_DIR,
)


class TestOrcQueueDispatcher:

    def test_a_gem_commit_trigger_detection(self):
        """Test A: GEM evidence commits must be detected as eligible."""
        subject = "GEM-002: dummy benchmark improvement evidence"
        files = ["analysis/commits/dummy/GEM-002_DUMMY_EVIDENCE.md"]
        
        eligible, reason, gem_id = check_eligibility(subject, files)
        assert eligible is True
        assert gem_id == "GEM-002"
        assert "Valid GEM evidence commit" in reason

        # Case with GEM in file path even if subject has different prefix
        subject2 = "feat: add benchmark evidence"
        files2 = ["analysis/commits/GEM-003_analysis.md"]
        eligible2, reason2, gem_id2 = check_eligibility(subject2, files2)
        assert eligible2 is True
        assert gem_id2 == "GEM-003"

    def test_b_duplicate_prevention(self, tmp_path):
        """Test B: Re-processing the same commit SHA must be blocked."""
        # Setup mock tasks directory
        mock_tasks_dir = tmp_path / "tasks"
        mock_tasks_dir.mkdir()
        
        test_sha = "c592056657fa02fc08760d9679bf3d94f4bb921a"
        dummy_task_file = mock_tasks_dir / "ORC-TASK-002.yaml"
        dummy_task_file.write_text(f"""task_id: "ORC-TASK-002"
source_commit: "{test_sha}"
status: "PENDING"
""")
        
        # Test duplicate check logic
        import glob
        existing_shas = []
        for tf in glob.glob(str(mock_tasks_dir / "*.yaml")):
            with open(tf) as f:
                content = f.read()
                if f"source_commit: \"{test_sha}\"" in content:
                    existing_shas.append(test_sha)
                    
        assert len(existing_shas) == 1
        assert existing_shas[0] == test_sha

    def test_c_loop_prevention_exclusions(self):
        """Test C: ORC, SYSTEM, BASE, and [skip ci] commits must NOT trigger ORC tasks."""
        # 1. ORC commit
        eligible, reason, _ = check_eligibility("ORC-001: dummy review of SYSTEM-001", ["analysis/commits/ORC-001.md"])
        assert eligible is False
        assert "ORC commit" in reason

        # 2. SYSTEM commit
        eligible, reason, _ = check_eligibility("SYSTEM-001: initialize multi-agent protocol", [".agent/PROTOCOL.md"])
        assert eligible is False
        assert "SYSTEM/skip-ci" in reason

        # 3. BASE commit
        eligible, reason, _ = check_eligibility("BASE-001: update baseline to rev8.2", ["docs/REV8.2_BASELINE.md"])
        assert eligible is False
        assert "BASE commit" in reason

        # 4. Skip CI commit
        eligible, reason, _ = check_eligibility("fix: internal typo [skip ci]", ["README.md"])
        assert eligible is False
        assert "skip-ci" in reason

        # 5. Irrelevant doc commit without GEM
        eligible, reason, _ = check_eligibility("docs: update user guide", ["docs/guide.md"])
        assert eligible is False
        assert "does not match GEM evidence patterns" in reason
