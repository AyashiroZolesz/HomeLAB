#!/usr/bin/env python3

import socket
import subprocess
import sys
from pathlib import Path

import requests
import yaml


CONFIG = Path("/etc/sentinel/config.yaml")


def load_config():
    with CONFIG.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ping(host):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def tcp_check(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def http_check(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        return True, response.status_code
    except requests.RequestException:
        return False, None


def main():
    cfg = load_config()
    host = cfg["homelab"]["host"]
    ssh_port = cfg["homelab"]["ssh_port"]

    failures = 0

    print("=== Sentinel basic check ===")
    print()

    ok = ping(host)
    print(f"{'OK' if ok else 'FAIL':4}  HomeLAB ping        {host}")
    failures += not ok

    ok = tcp_check(host, ssh_port)
    print(f"{'OK' if ok else 'FAIL':4}  HomeLAB SSH         {host}:{ssh_port}")
    failures += not ok

    for name, service in cfg["services"].items():
        ok, status = http_check(service["url"])

        if ok:
            print(f"OK    {name:<18} HTTP {status}")
        else:
            print(f"FAIL  {name:<18} no response")
            failures += 1

    print()
    print(f"Result: {failures} failure(s)")

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
