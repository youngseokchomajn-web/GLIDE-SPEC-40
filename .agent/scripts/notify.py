#!/usr/bin/env python3
import subprocess
import sys

TOPIC = "glide40-ysys"

def send_push_notification(title, message, priority="high", tags="bell"):
    # 1. Send to ntfy.sh mobile push
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

    # 2. Send macOS native desktop banner notification
    try:
        clean_msg = message.replace('"', '\\"').replace("'", "")
        clean_title = title.replace('"', '\\"').replace("'", "")
        osa_cmd = f'display notification "{clean_msg}" with title "{clean_title}" sound name "Glass"'
        subprocess.run(["osascript", "-e", osa_cmd], timeout=3, check=False)
    except Exception:
        pass

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "GLIDE-SPEC-40"
    m = sys.argv[2] if len(sys.argv) > 2 else "Notification from GLIDE-SPEC-40"
    send_push_notification(t, m)
