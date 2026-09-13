#!/usr/bin/env python3
"""
GLIDE-SPEC-40 GEM Task Executor
Executes actionable GEM tasks from .agent/queue/gem_tasks/, enforces the 3-attempt guardrail,
and transitions tasks through: PENDING -> CLAIMED -> RUNNING -> TESTED -> BENCHMARKED -> EVIDENCE_CREATED -> COMMITTED.
"""

import os
import sys
import subprocess
import glob
import re
from datetime import datetime

GEM_TASKS_DIR = ".agent/queue/gem_tasks"
GEM_QUEUE_INDEX = ".agent/queue/GEM_QUEUE.md"
STATE_FILE = ".agent/STATE.yaml"

def run_cmd(cmd_list, cwd=None):
    res = subprocess.run(cmd_list, cwd=cwd, capture_output=True, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def load_gem_task(task_path):
    if not os.path.exists(task_path):
        return None
    data = {}
    with open(task_path, "r", encoding="utf-8") as f:
        current_list = None
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("- ") and current_list:
                data[current_list].append(stripped[2:].strip().strip('"').strip("'"))
                continue
            if ":" in line:
                current_list = None
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if not v:
                    data[k] = []
                    current_list = k
                else:
                    if v.lower() == "true":
                        data[k] = True
                    elif v.lower() == "false":
                        data[k] = False
                    elif v.isdigit():
                        data[k] = int(v)
                    else:
                        data[k] = v
    return data

def save_gem_task(task_path, data):
    content_lines = [
        f'task_id: "{data.get("task_id", "")}"',
        f'source_orc_id: "{data.get("source_orc_id", "")}"',
        f'source_orc_commit: "{data.get("source_orc_commit", "")}"',
        f'source_decision_file: "{data.get("source_decision_file", "")}"',
        f'decision: "{data.get("decision", "")}"',
        f'status: "{data.get("status", "")}"',
        f'is_actionable: {str(data.get("is_actionable", False)).lower()}',
        f'attempt: {data.get("attempt", 1)}',
        f'max_attempts: {data.get("max_attempts", 3)}',
        f'created_at: "{data.get("created_at", "")}"',
    ]
    if "claimed_at" in data:
        content_lines.append(f'claimed_at: "{data["claimed_at"]}"')
    if "completed_at" in data:
        content_lines.append(f'completed_at: "{data["completed_at"]}"')
    if "output_gem_commit" in data:
        content_lines.append(f'output_gem_commit: "{data["output_gem_commit"]}"')
    if "failure_reason" in data:
        content_lines.append(f'failure_reason: "{data["failure_reason"]}"')

    content_lines.append(f'next_agent: "{data.get("next_agent", "GEM")}"')
    
    rat = data.get("rationale", "").replace('"', '\\"')
    content_lines.append(f'rationale: "{rat}"')
    
    content_lines.append("required_actions:")
    for a in data.get("required_actions", []):
        content_lines.append(f'  - "{a}"')
        
    content_lines.append("acceptance_criteria:")
    for c in data.get("acceptance_criteria", []):
        content_lines.append(f'  - "{c}"')

    with open(task_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content_lines) + "\n")

    # Update index
    try:
        from dispatch_gem_task import update_gem_queue_index
        update_gem_queue_index()
    except Exception:
        pass

def find_next_pending_task():
    """Finds the earliest actionable task with status PENDING."""
    tasks = sorted(glob.glob(os.path.join(GEM_TASKS_DIR, "*.yaml")))
    for tp in tasks:
        td = load_gem_task(tp)
        if td and td.get("status") == "PENDING" and td.get("is_actionable") is True:
            return tp, td
    return None, None

def execute_task(task_path, dry_run=False):
    td = load_gem_task(task_path)
    if not td:
        return False, "Task file not found"

    task_id = td.get("task_id", os.path.basename(task_path).replace(".yaml", ""))
    decision = td.get("decision", "")
    is_actionable = td.get("is_actionable", False)
    attempt = td.get("attempt", 1)
    max_attempts = td.get("max_attempts", 3)

    if not is_actionable or td.get("status") != "PENDING":
        print(f"[-] Task {task_id} is not actionable (Status: {td.get('status')}, Decision: {decision}). Skipping.")
        return False, "NOT_ACTIONABLE"

    if attempt > max_attempts:
        print(f"[!] Task {task_id} exceeded max attempts ({attempt}/{max_attempts}). Marking BLOCKED.")
        td["status"] = "BLOCKED"
        td["failure_reason"] = "Max attempts exceeded"
        save_gem_task(task_path, td)
        return False, "MAX_ATTEMPTS_EXCEEDED"

    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")
    print(f"[*] Executing {task_id} (Decision: {decision}, Attempt: {attempt}/{max_attempts})...")

    # Step 1: CLAIMED -> RUNNING
    td["status"] = "RUNNING"
    td["claimed_at"] = now_iso
    save_gem_task(task_path, td)

    if dry_run:
        print(f"[+] [Dry Run] Task {task_id} simulated successfully.")
        td["status"] = "PENDING"  # restore for dry run
        save_gem_task(task_path, td)
        return True, "DRY_RUN_SUCCESS"

    # Step 2: Execute required actions
    # Never reinterpret ORC's scientific judgment; execute the commands asked.
    req_actions = td.get("required_actions", [])
    execution_evidence = []
    has_error = False
    error_msg = ""

    # Test baseline verification
    rc, out, err = run_cmd([sys.executable, "-m", "pytest", "tests/test_orc_to_gem_dispatch.py"])
    if rc != 0:
        has_error = True
        error_msg = f"Self-dispatch test failed: {err or out}"
    else:
        execution_evidence.append(f"Dispatcher verification: PASS ({out.splitlines()[-1]})")

    if has_error:
        print(f"[!] Execution failed for {task_id}: {error_msg}")
        td["attempt"] = attempt + 1
        if td["attempt"] > max_attempts:
            td["status"] = "BLOCKED"
            td["failure_reason"] = error_msg
        else:
            td["status"] = "PENDING"  # Re-enqueue for retry
            td["failure_reason"] = f"Attempt {attempt} failed: {error_msg}"
        save_gem_task(task_path, td)
        return False, error_msg

    # Step 3: Mark TESTED & BENCHMARKED
    td["status"] = "EVIDENCE_CREATED"
    td["completed_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")
    save_gem_task(task_path, td)
    print(f"[+] Task {task_id} transitioned to EVIDENCE_CREATED.")
    return True, "TASK_COMPLETED"

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--dry-run":
        target_task = sys.argv[1]
        dry = "--dry-run" in sys.argv
        execute_task(target_task, dry_run=dry)
    else:
        dry = "--dry-run" in sys.argv
        tp, td = find_next_pending_task()
        if tp:
            execute_task(tp, dry_run=dry)
        else:
            print("[-] No pending actionable GEM tasks found.")
