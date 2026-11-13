# Sentinel Overview

## Purpose

Sentinel is a Raspberry Pi based monitoring and recovery node for the HomeLAB.

Its current Python implementation checks the main HomeLAB server, records state changes and attempts Telegram notifications. A separate main-host recovery helper exists, but the imported Python code does not invoke it automatically.

Survey and source review: **2026-11-13**. The owner ran the read-only runtime commands and copied the selected source files. No check program, notification or recovery helper was executed as part of this repository refresh.

---

## Platform

Current Sentinel node:

```text
Host: homelab-pi
Model: Raspberry Pi 3 Model B Rev 1.2
OS: Debian 13
Architecture: ARM64
CPU: Cortex-A53
RAM: ~1 GB
Ethernet: 192.168.31.11
Tailscale: enabled
```

The Raspberry Pi is intentionally separate from the main HomeLAB server so it can continue monitoring even when the main host is unavailable.

Ethernet and Wi-Fi are both active, with Ethernet preferred by the default-route metric. Tailscale and MagicDNS are active on the Pi. No service was listening on the DNS port in the inspected socket list; the Pi is not currently documented as a filtering DNS server. Router DNS is present in the NetworkManager configuration and Tailscale manages the system resolver. Full subnet-router, exit-node and upstream resolver behavior remain unverified.

---

## Design Philosophy

The intended recovery design is:

```text
check
  ↓
confirm
  ↓
diagnose
  ↓
recover
  ↓
verify
  ↓
notify
```

A single failed check should not immediately trigger a restart.

Failures should first be confirmed and diagnosed before recovery is attempted.

Recovery actions should be limited and bounded to avoid restart loops.

These are design requirements, not a claim that the current implementation satisfies all of them. The existing automatic path performs checks, state recording and transition notifications; the recovery helper is separate.

---

## Current Checks

The [runner](../../sentinel/src/runner.py) starts [sentinel.py](../../sentinel/src/sentinel.py), which runs three check groups:

| Group | Current source behavior | Limit |
|---|---|---|
| [Basic](../../sentinel/src/checks/basic.py) | Ping, TCP connection to the configured SSH port and HTTP GETs from the service map | Any received HTTP status passes; TCP reachability is not SSH authentication |
| [Host health](../../sentinel/src/checks/host_health.py) | Disk and memory thresholds over SSH; uptime/load output | Warnings do not fail the group; uptime/load has no severity threshold |
| [Media stack](../../sentinel/src/checks/media_stack.py) | Seven fixed container names, optional health state, saved port comparison and fixed-address TCP/UDP listener checks | Seerr is not in the fixed container list; exit IP and Internet-side port reachability are not checked |

The disk thresholds in the current source are warning at 80% and failure at 90%. Memory checks warn below 20% available and fail below 10%. The disk pipeline can accept empty output without recording a failure; it does not independently establish mount identity. These behaviors were reviewed in source, not tested by injecting live faults.

The HTTP service map is read from YAML. The live map was not copied, so current Seerr coverage through that map is unverified. The separate owner-run survey received HTTP responses from all six media application roots, including Seerr.

The current configuration is stored at:

```text
/etc/sentinel/config.yaml
```

The Sentinel project is located under:

```text
/opt/sentinel
```

Runtime state is stored under:

```text
/var/lib/sentinel
```

Logs are stored under:

```text
/var/log/sentinel
```

## Source and Runtime Layout

| Versioned source | Current runtime location |
|---|---|
| [Python source](../../sentinel/src/runner.py) and its check/notification modules | `/opt/sentinel/src` |
| [Direct Python dependencies](../../sentinel/requirements.txt) | Existing `/opt/sentinel/venv` |
| [Service](../../sentinel/systemd/sentinel.service) and [timer](../../sentinel/systemd/sentinel.timer) | `/etc/systemd/system` |
| [Configuration example](../../sentinel/config.example.yaml) | `/etc/sentinel/config.yaml`, populated separately |
| [Telegram variable names](../../sentinel/telegram.env.example) | An environment file supplied separately to the service |
| [Media diagnostic helper](../../scripts/sentinel/sentinel-media-status) and [recovery helper](../../scripts/sentinel/sentinel-recover-media) | Main host, `/usr/local/sbin` |

The Python, shell and unit files are copies of the inspected deployment sources. The configuration and environment examples are newly written schema examples, not copies of live secret values. `requirements.txt` records the directly imported third-party packages and their versions reported from the Pi; it is not a complete environment lock file.

This source collection is not an installer. Runtime paths, accounts, permissions, SSH trust/identity and populated configuration still require deliberate setup. The host-health and media checks currently keep their SSH destination and identity path in source; changing only the YAML host does not retarget them.

## Scheduling and Result Semantics

The imported timer has `OnBootSec=1min`, `OnUnitActiveSec=2min` and `AccuracySec=10s`. It activates a oneshot service running as the current administrative account on the Pi. No unit drop-ins were reported by the runtime query.

The timer was active and the inspected run had exit status zero. The runner deliberately returns zero after recording either `OK` or `DEGRADED`, so systemd success is not a summary of HomeLAB health. Exceptions before normal completion can still fail the service.

---

## HomeLAB Access

Sentinel uses a dedicated SSH key and a dedicated `sentinel` account on the HomeLAB server.

The account has diagnostic sudo permissions and an explicit VPN-stack recovery permission. The current model is therefore broader than read-only diagnostics. See the [security review](security.md).

Current diagnostic access includes:

- Docker container status
- Docker inspect
- Docker logs
- disk usage
- memory information
- system uptime

The allowed helper paths already exist on the main host. Their effective ownership, permissions and SSH-key restrictions need a separate access-control review; source availability alone does not establish least privilege.

---

## Planned Monitoring

Further verification and extensions include:

- stricter HTTP status interpretation and complete response parsing
- mount identity and missing-disk detection
- reviewed coverage of newly added services such as Seerr
- load thresholds if an operational need is established
- Jellyfin health
- Radarr health
- Sonarr health
- Prowlarr health
- qBittorrent health
- Gluetun health
- Proton VPN connectivity
- forwarded port synchronization
- qBittorrent VPN interface binding
- Tailscale connectivity
- storage health
- backup status

---

## Recovery

Sentinel recovery should only run after a failure has been confirmed.

A future automatic recovery path should:

- collect diagnostics before making changes
- perform only predefined actions
- limit restart attempts
- verify the result after recovery
- stop automated recovery if the problem persists
- notify the user when intervention is required

One important recovery group is:

```text
Gluetun
   ↓
qBittorrent
   ↓
qbit-port-sync
```

These services have a shared network dependency and may need coordinated recovery.

The current helper accepts `vpn-stack`, restarts Gluetun, polls its health up to twelve times with five-second sleeps, then restarts the two dependents. It reports completion after a further wait, without a functional check of the dependents, VPN exit or port synchronization. It has no overall timeout. No recovery action was executed during the survey.

---

## Notifications

The [Telegram module](../../sentinel/src/notifications/telegram.py) is implemented and reads `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` from the environment. The unit references a separate environment file; its contents were not copied.

The runner sends on `OK -> DEGRADED` and `DEGRADED -> OK` transitions. An initial degraded state, or a change of failures while the status remains degraded, does not trigger these transitions. A send failure is printed and is not retried; the new status is still saved. Delivery was not tested. Exception text can contain a credential-bearing request URL; see [security.md](security.md).

Notifications should eventually include:

- failed service
- failure time
- diagnostics summary
- recovery action performed
- recovery result
- whether manual intervention is required

---

## Persistent History

The runner writes `/var/lib/sentinel/status.json` and appends state transitions to `/var/log/sentinel/incidents.log`. Both files existed during the survey and the status file had a current modification time. Their contents were not read.

Longer-term reports, incidents and archived logs are planned to be stored on the main HomeLAB server under:

```text
/srv/homelab/sentinel/
```

The design should avoid unnecessary write load on the Raspberry Pi SD card.

---

## Future Direction

Planned extensions include:

- automated safe recovery
- Telegram commands
- incident history
- centralized status reporting
- monitoring dashboard
- metrics collection
- UPS monitoring
- SMART storage monitoring
- backup monitoring

Backup infrastructure, DNS filtering and automated hardware migration are deferred. No application restore, Telegram-delivery, fault-injection or automatic recovery test was established by this repository refresh.
