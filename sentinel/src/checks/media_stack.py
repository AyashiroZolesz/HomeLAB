#!/usr/bin/env python3

import subprocess
import sys

SSH_KEY = "/home/zolesz/.ssh/sentinel_homelab"
REMOTE = "sentinel@192.168.31.10"

CONTAINERS = [
    "gluetun",
    "qbittorrent",
    "qbit-port-sync",
    "prowlarr",
    "radarr",
    "sonarr",
    "jellyfin",
]


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


def ok(label, value="OK"):
    print(f"[OK]   {label}: {value}")


def fail(label, value="FAILED"):
    print(f"[FAIL] {label}: {value}")


def check_ssh():
    rc, out, err = ssh("hostname")

    if rc == 0:
        ok("SSH", out)
        return True

    fail("SSH", err or f"exit {rc}")
    return False


def check_containers():
    failures = 0

    for container in CONTAINERS:
        rc, out, err = ssh(
            f"sudo /usr/bin/docker inspect "
            f"--format '{{{{.State.Status}}}}|{{{{if .State.Health}}}}{{{{.State.Health.Status}}}}{{{{else}}}}none{{{{end}}}}' "
            f"{container}"
        )

        if rc != 0:
            fail(container, err or "inspect failed")
            failures += 1
            continue

        status, _, health = out.partition("|")

        if status != "running":
            fail(container, f"status={status}, health={health}")
            failures += 1
        elif health not in ("healthy", "none"):
            fail(container, f"status={status}, health={health}")
            failures += 1
        else:
            ok(container, f"status={status}, health={health}")

    return failures


def get_media_status():
    rc, out, err = ssh(
        "sudo /usr/local/sbin/sentinel-media-status"
    )

    if rc != 0:
        fail("Media diagnostic helper", err or f"exit {rc}")
        return None, []

    forwarded_port = None
    listeners = []
    in_listeners = False

    for line in out.splitlines():
        line = line.strip()

        if line.startswith("FORWARDED_PORT="):
            forwarded_port = line.split("=", 1)[1].strip()

        elif line == "QBIT_LISTENERS_BEGIN":
            in_listeners = True

        elif line == "QBIT_LISTENERS_END":
            in_listeners = False

        elif in_listeners and line:
            listeners.append(line)

    if forwarded_port and forwarded_port.isdigit():
        ok("Proton forwarded port", forwarded_port)
    else:
        fail("Proton forwarded port", "not available")
        forwarded_port = None

    return forwarded_port, listeners


def check_qbit_port():
    rc, out, err = ssh(
        "grep '^Session\\\\Port=' "
        "/srv/homelab/appdata/qbittorrent/qBittorrent/qBittorrent.conf "
        "2>/dev/null | tail -1 | cut -d= -f2"
    )

    if rc == 0 and out.isdigit():
        ok("qBittorrent Session port", out)
        return out

    fail("qBittorrent Session port", err or out or "not available")
    return None


def check_listener(port, listeners):
    if not port:
        fail("qBittorrent VPN listener", "port unavailable")
        return False

    expected = f"10.2.0.2:{port}"

    tcp_ok = any(
        line.startswith("tcp") and expected in line
        for line in listeners
    )

    udp_ok = any(
        line.startswith("udp") and expected in line
        for line in listeners
    )

    if tcp_ok and udp_ok:
        ok("qBittorrent VPN listener", f"{expected} TCP+UDP")
        return True

    missing = []

    if not tcp_ok:
        missing.append("TCP")

    if not udp_ok:
        missing.append("UDP")

    fail(
        "qBittorrent VPN listener",
        f"{expected} missing {'+'.join(missing)}",
    )

    return False


def main():
    print("=== HomeLAB Sentinel Media Check ===")

    if not check_ssh():
        sys.exit(1)

    failures = check_containers()

    forwarded_port, listeners = get_media_status()
    qbit_port = check_qbit_port()

    if forwarded_port and qbit_port:
        if forwarded_port == qbit_port:
            ok("Port synchronization", forwarded_port)
        else:
            fail(
                "Port synchronization",
                f"Proton={forwarded_port}, qBittorrent={qbit_port}",
            )
            failures += 1
    else:
        failures += 1

    if not check_listener(qbit_port, listeners):
        failures += 1

    print()
    print(f"Failures: {failures}")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
