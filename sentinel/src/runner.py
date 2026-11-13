#!/usr/bin/env python3

import json
import subprocess
from datetime import datetime
from pathlib import Path

from notifications.telegram import send_message

PYTHON = "/opt/sentinel/venv/bin/python"
SENTINEL = "/opt/sentinel/src/sentinel.py"

STATE_FILE = Path("/var/lib/sentinel/status.json")
INCIDENT_LOG = Path("/var/log/sentinel/incidents.log")


def now():
    return datetime.now().astimezone()


def now_iso():
    return now().isoformat(timespec="seconds")


def load_previous_state():
    if not STATE_FILE.exists():
        return None

    try:
        return json.loads(STATE_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def save_state(status, failures, degraded_since=None):
    data = {
        "status": status,
        "checked_at": now_iso(),
        "failures": failures,
        "degraded_since": degraded_since,
    }

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(data, indent=2) + "\n")


def log_transition(old_status, new_status):
    INCIDENT_LOG.parent.mkdir(parents=True, exist_ok=True)

    with INCIDENT_LOG.open("a") as f:
        f.write(
            f"{now_iso()} "
            f"{old_status or 'UNKNOWN'} -> {new_status}\n"
        )


def extract_failures(output):
    failures = []

    for raw_line in output.splitlines():
        line = raw_line.strip()

        if line.startswith("[FAIL]"):
            failures.append(line.replace("[FAIL]", "", 1).strip())

        elif line.startswith("FAIL"):
            cleaned = line[4:].strip()

            if cleaned:
                failures.append(cleaned)

    return failures


def format_duration(start_iso):
    if not start_iso:
        return "unknown"

    try:
        start = datetime.fromisoformat(start_iso)
        seconds = int((now() - start).total_seconds())
    except (ValueError, TypeError):
        return "unknown"

    if seconds < 60:
        return f"{seconds} sec"

    minutes = seconds // 60

    if minutes < 60:
        return f"{minutes} min"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    return f"{hours}h {remaining_minutes}m"


def degraded_message(failures):
    lines = [
        "⚠️ HomeLAB Sentinel",
        "",
        "Status: OK -> DEGRADED",
        "",
        "Failed checks:",
    ]

    if failures:
        for failure in failures:
            lines.append(f"- {failure}")
    else:
        lines.append("- Unknown failure")

    lines.extend([
        "",
        f"Time: {now().strftime('%Y-%m-%d %H:%M:%S')}",
    ])

    return "\n".join(lines)


def recovery_message(previous):
    previous_failures = previous.get("failures", [])
    degraded_since = previous.get("degraded_since")

    lines = [
        "✅ HomeLAB Sentinel",
        "",
        "Status: DEGRADED -> OK",
        "",
        "Recovered:",
    ]

    if previous_failures:
        for failure in previous_failures:
            lines.append(f"- {failure}")
    else:
        lines.append("- HomeLAB health checks")

    lines.extend([
        "",
        f"Downtime: {format_duration(degraded_since)}",
        f"Time: {now().strftime('%Y-%m-%d %H:%M:%S')}",
    ])

    return "\n".join(lines)


def notify(message):
    try:
        send_message(message)
        print("Telegram notification sent.")
    except Exception as exc:
        print(f"Telegram notification failed: {exc}")


def main():
    result = subprocess.run(
        [PYTHON, SENTINEL],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    print(result.stdout, end="")

    current_status = (
        "OK"
        if result.returncode == 0
        else "DEGRADED"
    )

    failures = extract_failures(result.stdout)

    previous = load_previous_state()
    previous_status = (
        previous.get("status")
        if previous
        else None
    )

    degraded_since = None

    if current_status == "DEGRADED":
        if previous_status == "DEGRADED":
            degraded_since = previous.get("degraded_since")
        else:
            degraded_since = now_iso()

    if previous_status != current_status:
        print()
        print(
            f"STATE CHANGE: "
            f"{previous_status or 'UNKNOWN'} -> {current_status}"
        )

        log_transition(previous_status, current_status)

        if previous_status == "OK" and current_status == "DEGRADED":
            notify(degraded_message(failures))

        elif previous_status == "DEGRADED" and current_status == "OK":
            notify(recovery_message(previous))

    save_state(
        current_status,
        failures,
        degraded_since,
    )

    # DEGRADED is a HomeLAB state, not a Sentinel program failure.
    # If this code reached the end successfully, systemd should see SUCCESS.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
