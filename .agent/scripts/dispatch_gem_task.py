#!/usr/bin/env python3
"""
GLIDE-SPEC-40 ORC Decision -> GEM Task Dispatcher
Parses formal ORC Decision documents, preserves scientific findings without reinterpretation,
enforces idempotency, limits actionable scope, and writes GEM-TASK-XXX.yaml queue entries.
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

ACTIONABLE_DECISIONS = {"EXPERIMENT", "FIX_REQUIRED", "INVESTIGATE"}
STOP_DECISIONS = {"APPROVE", "REJECT", "DATA_REQUIRED", "BLOCKED", "HOLD", "CONVERGED"}

def run_git(args):
    res = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
    return res.stdout.strip()

def get_commit_details(commit_ref="HEAD"):
    sha = run_git(["rev-parse", commit_ref])
    subject = run_git(["log", "-1", "--format=%s", commit_ref])
    body = run_git(["log", "-1", "--format=%b", commit_ref])
    files = run_git(["diff-tree", "--no-commit-id", "--name-only", "-r", commit_ref]).splitlines()
    return sha, subject, body, files

def is_duplicate_orc_commit(commit_sha):
    """Checks if a task with the given source_orc_commit already exists."""
    if not os.path.exists(GEM_TASKS_DIR):
        return False
    for task_path in glob.glob(os.path.join(GEM_TASKS_DIR, "*.yaml")):
        try:
            with open(task_path, "r", encoding="utf-8") as f:
                content = f.read()
                if f"source_orc_commit: \"{commit_sha}\"" in content or f"source_orc_commit: {commit_sha}" in content:
                    return True
        except Exception:
            continue
    return False

def extract_yaml_from_markdown(file_path):
    """Extracts and parses yaml block enclosed by ```yaml ... ``` in markdown."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    match = re.search(r"```ya?ml\s*\n(.*?)\n```", text, re.DOTALL)
    if match:
        yaml_text = match.group(1)
    else:
        # Fallback: extract top key:value lines or header block
        lines = []
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("#") and len(lines) == 0:
                continue
            if s.startswith("## "):
                break
            if ":" in s or s.startswith("- "):
                lines.append(line)
            elif not s and len(lines) > 0:
                break
        yaml_text = "\n".join(lines)
        if not yaml_text.strip():
            return None
    
    parsed = {}
    current_list_key = None
    
    for line in yaml_text.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#"):
            continue
            
        if trimmed.startswith("- ") and current_list_key:
            item_val = trimmed[2:].strip().strip('"').strip("'")
            parsed[current_list_key].append(item_val)
            continue
            
        if ":" in line:
            current_list_key = None
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if not val:
                # Potential list header
                parsed[key] = []
                current_list_key = key
            else:
                # Scalar value
                clean_val = val.strip('"').strip("'")
                parsed[key] = clean_val
                
    # Normalize STATUS to DECISION if DECISION is missing
    if "STATUS" in parsed and "DECISION" not in parsed:
        parsed["DECISION"] = parsed["STATUS"]
    if "ID" in parsed and "ORC_ID" not in parsed:
        parsed["ORC_ID"] = parsed["ID"]

    # If RATIONALE or REQUIRED_ACTIONS missing, extract from markdown sections
    if "RATIONALE" not in parsed:
        m_dec = re.search(r"##\s+Decision\s*\n+(.*?)(?=\n##|\Z)", text, re.DOTALL)
        if m_dec:
            parsed["RATIONALE"] = m_dec.group(1).strip().replace("\n", " ")
    if "REQUIRED_ACTIONS" not in parsed:
        m_act = re.search(r"##\s+Required\s+(?:Next\s+)?Action[s]?\s*\n+(.*?)(?=\n##|\Z)", text, re.DOTALL)
        if m_act:
            actions = []
            for line in m_act.group(1).splitlines():
                line_s = line.strip()
                if re.match(r"^(\d+\.|\-|\*)\s+", line_s):
                    clean_act = re.sub(r"^(\d+\.|\-|\*)\s+", "", line_s).strip().rstrip(";")
                    actions.append(clean_act)
            if actions:
                parsed["REQUIRED_ACTIONS"] = actions
        
    return parsed

def locate_orc_decision_file(files):
    """Finds the primary ORC decision markdown among modified files."""
    for f in files:
        if f.startswith("analysis/commits/") and "Decision" in f and f.endswith(".md"):
            return f
        if f.startswith("analysis/commits/ORC-") and f.endswith(".md"):
            return f
    return None

def update_gem_queue_index():
    """Regenerates .agent/queue/GEM_QUEUE.md index table."""
    os.makedirs(GEM_TASKS_DIR, exist_ok=True)
    task_files = sorted(glob.glob(os.path.join(GEM_TASKS_DIR, "*.yaml")))
    
    lines = [
        "# GEM Execution Task Queue",
        "",
        "**Governing Protocol:** [`.agent/PROTOCOL.md`](../PROTOCOL.md) | [`.agent/CONTRACTS.md`](../CONTRACTS.md)",
        f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "| Task ID | Source ORC | Decision | Status | Actionable | Created At |",
        "| :--- | :---: | :---: | :---: | :---: | :--- |"
    ]

    for tf in task_files:
        tid = os.path.basename(tf).replace(".yaml", "")
        data = {}
        with open(tf, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line and not line.strip().startswith("-"):
                    k, v = line.split(":", 1)
                    data[k.strip()] = v.strip().strip('"')
        
        status = data.get("status", "PENDING")
        src_orc = data.get("source_orc_id", "ORC")
        decision = data.get("decision", "UNKNOWN")
        actionable = data.get("is_actionable", "false")
        created = data.get("created_at", "")
        lines.append(f"| [`{tid}`](gem_tasks/{os.path.basename(tf)}) | {src_orc} | `{decision}` | **{status}** | `{actionable}` | {created} |")

    if not task_files:
        lines.append("| *(No GEM tasks)* | - | - | - | - | - |")

    with open(GEM_QUEUE_INDEX, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def dispatch_gem_task(commit_ref="HEAD"):
    sha, subject, body, files = get_commit_details(commit_ref)
    print(f"Inspecting commit for ORC Decision {sha[:7]}: {subject}")

    is_orc_subject = subject.startswith("ORC-")
    has_orc_file = any(
        f.startswith("analysis/commits/ORC-") or f.startswith(".agent/queue/tasks/ORC-")
        for f in files
    )

    if not (is_orc_subject or has_orc_file):
        print("[-] Skip: Not an ORC decision commit.")
        return False, "NOT_AN_ORC_COMMIT"

    if is_duplicate_orc_commit(sha):
        print(f"[-] Skip: ORC commit {sha[:7]} is already processed (Idempotency).")
        return False, "DUPLICATE_PREVENTED"

    decision_file = locate_orc_decision_file(files)
    if not decision_file:
        print("[-] Skip: No ORC decision markdown file found in commit.")
        return False, "NO_DECISION_FILE"

    decision_data = extract_yaml_from_markdown(decision_file)
    if not decision_data:
        print(f"[-] Skip: Failed to parse YAML block in {decision_file}.")
        return False, "INVALID_YAML_BLOCK"

    orc_id = decision_data.get("ORC_ID", subject.split(":")[0].strip())
    decision = decision_data.get("DECISION", "UNKNOWN").upper()
    rationale = decision_data.get("RATIONALE", "")
    req_actions = decision_data.get("REQUIRED_ACTIONS", [])
    acc_criteria = decision_data.get("ACCEPTANCE_CRITERIA", [])
    next_agent = decision_data.get("NEXT_AGENT", "GEM")

    # Determine actionability strictly according to governance rules
    is_actionable = decision in ACTIONABLE_DECISIONS
    task_status = "PENDING" if is_actionable else "ACKNOWLEDGED_STOP"

    os.makedirs(GEM_TASKS_DIR, exist_ok=True)
    task_num = orc_id.replace("ORC-", "") if orc_id.startswith("ORC-") else "001"
    task_id = f"GEM-TASK-{task_num}"
    task_file = os.path.join(GEM_TASKS_DIR, f"{task_id}.yaml")
    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")

    req_actions_yaml = "\n".join([f'  - "{a}"' for a in req_actions]) if req_actions else "  []"
    acc_criteria_yaml = "\n".join([f'  - "{c}"' for c in acc_criteria]) if acc_criteria else "  []"

    # Sanitize multiline string for YAML scalar
    escaped_rationale = rationale.replace('"', '\\"')

    content = f"""task_id: "{task_id}"
source_orc_id: "{orc_id}"
source_orc_commit: "{sha}"
source_decision_file: "{decision_file}"
decision: "{decision}"
status: "{task_status}"
is_actionable: {str(is_actionable).lower()}
attempt: 1
max_attempts: 3
created_at: "{now_iso}"
next_agent: "{next_agent}"
rationale: "{escaped_rationale}"
required_actions:
{req_actions_yaml}
acceptance_criteria:
{acc_criteria_yaml}
"""
    with open(task_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[+] Successfully generated GEM task: {task_id} (Decision: {decision}, Status: {task_status}) at {task_file}")
    update_gem_queue_index()
    return True, task_id

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    success, msg = dispatch_gem_task(target)
    is_normal = success or any(k in msg for k in ["Skip", "DUPLICATE", "NOT_AN_ORC"])
    sys.exit(0 if is_normal else 1)
