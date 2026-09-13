#!/usr/bin/env python3
"""
GLIDE-SPEC-40 ORC Queue Dispatcher
Detects GEM evidence commits, performs duplicate & loop prevention,
and generates formal ORC review tasks in .agent/queue/tasks/.
"""

import os
import sys
import subprocess
import glob
from datetime import datetime

QUEUE_DIR = ".agent/queue"
TASKS_DIR = os.path.join(QUEUE_DIR, "tasks")
QUEUE_INDEX = os.path.join(QUEUE_DIR, "ORC_QUEUE.md")
STATE_FILE = ".agent/STATE.yaml"

def run_git(args):
    res = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
    return res.stdout.strip()

def get_commit_details(commit_ref="HEAD"):
    sha = run_git(["rev-parse", commit_ref])
    subject = run_git(["log", "-1", "--format=%s", commit_ref])
    body = run_git(["log", "-1", "--format=%b", commit_ref])
    files = run_git(["diff-tree", "--no-commit-id", "--name-only", "-r", commit_ref]).splitlines()
    return sha, subject, body, files

def is_duplicate_commit(commit_sha):
    """Checks if a task with the given source_commit already exists in tasks directory."""
    if not os.path.exists(TASKS_DIR):
        return False
    for task_path in glob.glob(os.path.join(TASKS_DIR, "*.yaml")):
        try:
            with open(task_path, "r", encoding="utf-8") as f:
                content = f.read()
                if f"source_commit: \"{commit_sha}\"" in content or f"source_commit: {commit_sha}" in content:
                    return True
        except Exception:
            continue
    return False

def check_trigger_eligibility(subject, files):
    """
    Returns (eligible: bool, reason: str, gem_id: str)
    Loop Prevention: ORC-, SYSTEM-, BASE-, [skip ci] commits are excluded.
    """
    sub_upper = subject.upper()
    
    # 1. Loop Prevention check
    if sub_upper.startswith("ORC-"):
        return False, "Excluded by loop prevention (ORC commit)", None
    if sub_upper.startswith("SYSTEM-") or "[SKIP CI]" in sub_upper:
        return False, "Excluded by loop prevention (SYSTEM/skip-ci commit)", None
    if sub_upper.startswith("BASE-"):
        return False, "Excluded by loop prevention (BASE commit)", None

    # 2. Trigger Candidate check
    is_gem_subject = subject.startswith("GEM-")
    has_gem_file = any(
        f.startswith("analysis/commits/GEM-") or f.startswith("analysis/commits/dummy/GEM-")
        for f in files
    )

    if not (is_gem_subject or has_gem_file):
        return False, "Commit does not match GEM evidence patterns", None

    # Extract GEM ID
    gem_id = "GEM-UNKNOWN"
    if is_gem_subject:
        gem_id = subject.split(":")[0].strip()
    else:
        for f in files:
            if "GEM-" in f:
                basename = os.path.basename(f)
                gem_id = basename.split("_")[0]
                break

    return True, "Valid GEM evidence commit detected", gem_id

def determine_source_file(files):
    for f in files:
        if f.startswith("analysis/commits/") and f.endswith(".md"):
            return f
    return files[0] if files else "UNKNOWN"

def update_queue_index():
    """Regenerates .agent/queue/ORC_QUEUE.md table from task files."""
    os.makedirs(TASKS_DIR, exist_ok=True)
    task_files = sorted(glob.glob(os.path.join(TASKS_DIR, "*.yaml")))
    
    lines = [
        "# ORC Review Task Queue",
        "",
        "**Governing Protocol:** [`.agent/PROTOCOL.md`](../PROTOCOL.md) | [`.agent/CONTRACTS.md`](../CONTRACTS.md)",
        f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "| Task ID | Source | Source Commit | Status | Created At | Evidence File |",
        "| :--- | :---: | :---: | :---: | :---: | :--- |"
    ]

    for tf in task_files:
        tid = os.path.basename(tf).replace(".yaml", "")
        data = {}
        with open(tf, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    k, v = line.split(":", 1)
                    data[k.strip()] = v.strip().strip('"')
        
        status = data.get("status", "PENDING")
        src_id = data.get("source_id", "GEM")
        sha = data.get("source_commit", "")[:7]
        created = data.get("created_at", "")
        sfile = data.get("source_file", "")
        lines.append(f"| [`{tid}`](tasks/{os.path.basename(tf)}) | {src_id} | `{sha}` | **{status}** | {created} | `{sfile}` |")

    if not task_files:
        lines.append("| *(No pending tasks)* | - | - | - | - | - |")

    with open(QUEUE_INDEX, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def dispatch(commit_ref="HEAD"):
    sha, subject, body, files = get_commit_details(commit_ref)
    print(f"Inspecting commit {sha[:7]}: {subject}")
    
    eligible, reason, gem_id = check_trigger_eligibility(subject, files)
    if not eligible:
        print(f"[-] Dispatch Skipped: {reason}")
        return False, reason

    if is_duplicate_commit(sha):
        print(f"[-] Dispatch Skipped: Commit {sha[:7]} is already queued (Duplicate Prevention).")
        return False, "DUPLICATE_PREVENTED"

    os.makedirs(TASKS_DIR, exist_ok=True)
    
    # Task ID format: ORC-TASK-<num>
    task_num = gem_id.replace("GEM-", "") if gem_id.startswith("GEM-") else f"{len(glob.glob(os.path.join(TASKS_DIR, '*.yaml'))) + 1:03d}"
    task_id = f"ORC-TASK-{task_num}"
    task_file = os.path.join(TASKS_DIR, f"{task_id}.yaml")

    source_file = determine_source_file(files)
    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")

    task_content = f"""task_id: "{task_id}"
source_agent: "GEM"
source_id: "{gem_id}"
source_commit: "{sha}"
source_file: "{source_file}"
task_type: "EVIDENCE_REVIEW"
status: "PENDING"
created_at: "{now_iso}"
requires_orc: true
inspection_checklist:
  dataset_identity: false
  baseline_integrity: false
  split_and_holdout: false
  information_leakage: false
  benchmark_overfit: false
  cross_domain_stability: false
  regression_check: false
  complexity_vs_utility: false
  manufacturing_relevance: false
  physical_validation_need: false
"""
    with open(task_file, "w", encoding="utf-8") as f:
        f.write(task_content)

    print(f"[+] Successfully registered task: {task_id} at {task_file}")
    update_queue_index()
    return True, task_id

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    success, msg = dispatch(target)
    # Return 0 on normal dispatch or valid skip conditions
    is_normal = success or any(k in msg for k in ["Excluded", "Skipped", "DUPLICATE", "does not match"])
    sys.exit(0 if is_normal else 1)
