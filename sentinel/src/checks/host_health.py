#!/usr/bin/env python3

import subprocess
import sys

SSH_KEY = "/home/zolesz/.ssh/sentinel_homelab"
REMOTE = "sentinel@192.168.31.10"


def ssh(command):
    result = subprocess.run(
        [
            "ssh",
            "-i",
            SSH_KEY,
            "-o",
            "BatchMode=yes",
            "-o",
            "ConnectTimeout=5",
            REMOTE,
            command,
        ],
        text=True,
        capture_output=True,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def ok(label, value):
    print(f"[OK]   {label}: {value}")


def warn(label, value):
    print(f"[WARN] {label}: {value}")


def fail(label, value):
    print(f"[FAIL] {label}: {value}")


def check_disk():
    rc, out, err = ssh(
        "sudo /usr/bin/df -P / /srv/media 2>/dev/null | tail -n +2"
    )

    if rc != 0:
        fail("Disk usage", err or f"exit {rc}")
        return 1

    failures = 0

    for line in out.splitlines():
        parts = line.split()

        if len(parts) < 6:
            continue

        filesystem = parts[0]
        used_pct = int(parts[4].rstrip("%"))
        mount = parts[5]

        if used_pct >= 90:
            fail(f"Disk {mount}", f"{used_pct}% used ({filesystem})")
            failures += 1
        elif used_pct >= 80:
            warn(f"Disk {mount}", f"{used_pct}% used ({filesystem})")
        else:
            ok(f"Disk {mount}", f"{used_pct}% used ({filesystem})")

    return failures


def check_memory():
    rc, out, err = ssh("sudo /usr/bin/free -m")

    if rc != 0:
        fail("Memory", err or f"exit {rc}")
        return 1

    lines = out.splitlines()

    mem_line = next(
        (line for line in lines if line.startswith("Mem:")),
        None
    )

    if not mem_line:
        fail("Memory", "unable to parse free output")
        return 1

    parts = mem_line.split()

    total = int(parts[1])
    available = int(parts[6])

    available_pct = (available / total) * 100

    if available_pct < 10:
        fail("Memory", f"{available} MB available ({available_pct:.1f}%)")
        return 1
    elif available_pct < 20:
        warn("Memory", f"{available} MB available ({available_pct:.1f}%)")
    else:
        ok("Memory", f"{available} MB available ({available_pct:.1f}%)")

    return 0


def check_uptime_load():
    rc, out, err = ssh("sudo /usr/bin/uptime")

    if rc != 0:
        fail("Uptime/load", err or f"exit {rc}")
        return 1

    ok("Uptime/load", out)
    return 0


def main():
    print("=== HomeLAB Sentinel Host Health ===")

    failures = 0

    failures += check_disk()
    failures += check_memory()
    failures += check_uptime_load()

    print()
    print(f"Failures: {failures}")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
