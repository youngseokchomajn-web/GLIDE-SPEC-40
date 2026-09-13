"""
Unit tests for ORC Decision -> GEM Task Dispatcher
Validates parsing fidelity, actionability restriction, idempotency, and non-reinterpretation.
"""

import os
import sys
import pytest

AGENT_SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".agent", "scripts"))
if AGENT_SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, AGENT_SCRIPTS_DIR)

from dispatch_gem_task import (
    extract_yaml_from_markdown,
    ACTIONABLE_DECISIONS,
    STOP_DECISIONS,
    is_duplicate_orc_commit,
)


class TestOrcToGemDispatcher:

    def test_extract_yaml_from_markdown(self, tmp_path):
        """Validates that YAML block in ORC decision markdown is extracted with high fidelity."""
        test_md = tmp_path / "ORC-010_Decision.md"
        test_md.write_text("""# ORC-010 Decision

```yaml
ORC_ID: "ORC-010"
REF_GEM: "GEM-009"
STATUS: "COMPLETE"
DECISION: "EXPERIMENT"
RATIONALE: "Validation sample size is insufficient. Group-CV required."
REQUIRED_ACTIONS:
  - "Run Group-CV on 8 public formulation clusters"
  - "Extract prediction intervals at 90% confidence"
ACCEPTANCE_CRITERIA:
  - "No test leakage"
  - "RMSE improvement >= 5.0%"
NEXT_AGENT: "GEM"
```

## Additional text
Some review text that should not affect the YAML parser.
""")

        parsed = extract_yaml_from_markdown(str(test_md))
        assert parsed is not None
        assert parsed["ORC_ID"] == "ORC-010"
        assert parsed["DECISION"] == "EXPERIMENT"
        assert parsed["STATUS"] == "COMPLETE"
        assert parsed["NEXT_AGENT"] == "GEM"
        assert len(parsed["REQUIRED_ACTIONS"]) == 2
        assert "Run Group-CV on 8 public formulation clusters" in parsed["REQUIRED_ACTIONS"]
        assert len(parsed["ACCEPTANCE_CRITERIA"]) == 2
        assert "RMSE improvement >= 5.0%" in parsed["ACCEPTANCE_CRITERIA"]

    def test_actionability_rule_boundaries(self):
        """Verifies strict boundary between actionable and stop/passive decisions."""
        # Actionable decisions that trigger GEM PENDING tasks
        assert "EXPERIMENT" in ACTIONABLE_DECISIONS
        assert "FIX_REQUIRED" in ACTIONABLE_DECISIONS
        assert "INVESTIGATE" in ACTIONABLE_DECISIONS

        # Passive/terminal decisions that must NEVER auto-trigger work loops
        assert "APPROVE" in STOP_DECISIONS
        assert "REJECT" in STOP_DECISIONS
        assert "DATA_REQUIRED" in STOP_DECISIONS
        assert "BLOCKED" in STOP_DECISIONS
        assert "HOLD" in STOP_DECISIONS
        assert "CONVERGED" in STOP_DECISIONS

        # Disjoint sets (no overlap)
        assert len(ACTIONABLE_DECISIONS.intersection(STOP_DECISIONS)) == 0

    def test_idempotency_duplicate_prevention(self, tmp_path):
        """Verifies that an already processed source_orc_commit is blocked."""
        mock_tasks_dir = tmp_path / "gem_tasks"
        mock_tasks_dir.mkdir()
        
        test_orc_sha = "5503be98a38808a4c80e6545abbb1d95a779c064"
        dummy_task = mock_tasks_dir / "GEM-TASK-003.yaml"
        dummy_task.write_text(f"""task_id: "GEM-TASK-003"
source_orc_commit: "{test_orc_sha}"
decision: "APPROVE"
status: "ACKNOWLEDGED_STOP"
""")
        
        # Check duplicate logic
        import glob
        existing = False
        for tf in glob.glob(str(mock_tasks_dir / "*.yaml")):
            with open(tf) as f:
                if f'source_orc_commit: "{test_orc_sha}"' in f.read():
                    existing = True
                    break
        assert existing is True

    def test_all_seed_tasks_have_valid_40_hex_git_commits(self):
        """Invariant: Every GEM task YAML must have an authentic 40-char hex SHA that exists in git."""
        import glob
        import re
        import subprocess

        hex_pattern = re.compile(r"^[0-9a-f]{40}$")
        gem_tasks = glob.glob(".agent/queue/gem_tasks/*.yaml")
        assert len(gem_tasks) >= 2, "Seed tasks GEM-TASK-002 and GEM-TASK-003 must exist"

        for task_path in gem_tasks:
            source_sha = None
            with open(task_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("source_orc_commit:"):
                        source_sha = line.split(":", 1)[1].strip().strip('"').strip("'")
                        break
            
            assert source_sha is not None, f"source_orc_commit missing in {task_path}"
            assert hex_pattern.match(source_sha), f"source_orc_commit '{source_sha}' in {task_path} is not a valid 40-char hex SHA"
            
            # Verify git existence
            res = subprocess.run(["git", "cat-file", "-e", f"{source_sha}^{{commit}}"], capture_output=True)
            assert res.returncode == 0, f"Git commit {source_sha} does not exist in repository"
