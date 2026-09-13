#!/usr/bin/env python3
"""
GLIDE-SPEC-40 Autonomous Repository Watcher (Daemon)
Monitors origin/main every 10 seconds for up to 10 hours (36,000s).
Detects new ORC commits and logs events for GEM consumption.
"""

import subprocess
import time
import os
import sys
from datetime import datetime

INTERVAL_SECONDS = 180
TOTAL_DURATION_HOURS = 10
MAX_ITERATIONS = (TOTAL_DURATION_HOURS * 3600) // INTERVAL_SECONDS

LOG_FILE = "analysis/watcher.log"
STATE_FILE = ".agent/STATE.yaml"

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def get_latest_remote_commit():
    try:
        # Fetch without modifying working tree
        subprocess.run(["git", "fetch", "origin", "main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        res = subprocess.run(["git", "log", "-n", "1", "--format=%h %s", "origin/main"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"

def get_latest_local_commit():
    try:
        res = subprocess.run(["git", "log", "-n", "1", "--format=%h %s", "HEAD"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"

def main():
    os.makedirs("analysis", exist_ok=True)
    log_event(f"=== GLIDE-SPEC-40 Watcher Daemon Started ===")
    log_event(f"Interval: {INTERVAL_SECONDS}s | Duration: {TOTAL_DURATION_HOURS}h (Max {MAX_ITERATIONS} iterations)")
    
    last_known_remote = get_latest_remote_commit()
    log_event(f"Initial Remote HEAD: {last_known_remote}")
    
    iteration = 0
    while iteration < MAX_ITERATIONS:
        iteration += 1
        time.sleep(INTERVAL_SECONDS)
        
        current_remote = get_latest_remote_commit()
        if "ERROR" in current_remote:
            log_event(f"Fetch failed: {current_remote}")
            continue
            
        if current_remote != last_known_remote:
            log_event(f"🔔 NEW COMMIT DETECTED on origin/main: {current_remote}")
            if "ORC-" in current_remote:
                try:
                    py_bin = ".venv/bin/python" if os.path.exists(".venv/bin/python") else sys.executable
                    env = dict(os.environ)
                    env["PYTHONPATH"] = "."
                    subprocess.run(["git", "pull", "origin", "main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.run([py_bin, ".agent/scripts/dispatch_gem_task.py", "HEAD"], check=True, env=env)
                    log_event("✅ GEM Task Dispatch completed successfully.")
                    # Automatically trigger executor for actionable tasks
                    subprocess.run([py_bin, ".agent/scripts/execute_gem_task.py"], check=False, env=env)
                except Exception as e:
                    log_event(f"⚠️ GEM Task Dispatch/Execution failed: {e}")
            last_known_remote = current_remote
        else:
            log_event(f"Heartbeat #{iteration}/{MAX_ITERATIONS} (3m): Remote unchanged ({last_known_remote[:7]}). Monitoring...")

    log_event("=== Watcher Daemon Finished 10-Hour Window ===")

if __name__ == "__main__":
    main()
