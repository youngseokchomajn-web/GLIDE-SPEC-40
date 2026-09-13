#!/usr/bin/env python3
import subprocess
import sys

TOPIC = "glide40-ysys"

def send_push_notification(title, message, priority="high", tags="bell"):
    try:
        cmd = [
            "curl", "-s",
            "-H", f"Title: {title}",
            "-H", f"Priority: {priority}",
            "-H", f"Tags: {tags}",
            "-d", message,
            f"https://ntfy.sh/{TOPIC}"
        ]
        subprocess.run(cmd, timeout=5, check=False)
    except Exception:
        pass

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "GLIDE-SPEC-40"
    m = sys.argv[2] if len(sys.argv) > 2 else "Notification from GLIDE-SPEC-40"
    send_push_notification(t, m)
