#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

BASE = Path("/opt/sentinel/src")

CHECKS = [
    BASE / "checks" / "basic.py",
    BASE / "checks" / "host_health.py",
    BASE / "checks" / "media_stack.py",
]


def run_check(path):
    print()
    print("=" * 72)
    print(f"RUNNING: {path.name}")
    print("=" * 72)

    result = subprocess.run(
        ["/opt/sentinel/venv/bin/python", str(path)]
    )

    return result.returncode


def main():
    print("=== HomeLAB Sentinel ===")

    failures = 0

    for check in CHECKS:
        rc = run_check(check)

        if rc != 0:
            failures += 1

    print()
    print("=" * 72)

    if failures == 0:
        print("SENTINEL STATUS: OK")
        print("All checks passed.")
    else:
        print("SENTINEL STATUS: DEGRADED")
        print(f"Failed check groups: {failures}")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
