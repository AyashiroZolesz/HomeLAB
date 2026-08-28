# Sentinel Overview

## Purpose

Sentinel is a Raspberry Pi based monitoring and recovery node for the HomeLAB.

Its role is to monitor the main HomeLAB server independently, detect failures, collect diagnostics, perform safe recovery actions where appropriate, and send notifications.

---

## Platform

Current Sentinel node:

```text
Host: homelab-pi
OS: Debian 13
Architecture: ARM64
CPU: Cortex-A53
RAM: ~1 GB
Ethernet: 192.168.31.11
Tailscale: enabled
```

The Raspberry Pi is intentionally separate from the main HomeLAB server so it can continue monitoring even when the main host is unavailable.

---

## Design Philosophy

Sentinel follows this flow:

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

---

## Current Checks

The current implementation can check:

- HomeLAB network reachability
- SSH availability
- Jellyfin HTTP availability
- qBittorrent HTTP availability
- Radarr HTTP availability
- Sonarr HTTP availability
- Prowlarr HTTP availability

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

---

## HomeLAB Access

Sentinel uses a dedicated SSH key and a dedicated `sentinel` account on the HomeLAB server.

The account has restricted read-only sudo permissions for selected diagnostic commands.

This allows Sentinel to inspect the system without giving it unrestricted root access.

Current diagnostic access includes:

- Docker container status
- Docker inspect
- Docker logs
- disk usage
- memory information
- system uptime

Recovery permissions will be introduced separately and kept as narrow as possible.

---

## Planned Monitoring

Planned checks include:

- Docker container health
- disk usage
- memory pressure
- system load
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

The recovery system should:

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

---

## Notifications

Telegram is the planned first notification channel.

Notifications should eventually include:

- failed service
- failure time
- diagnostics summary
- recovery action performed
- recovery result
- whether manual intervention is required

---

## Persistent History

Sentinel will keep lightweight local runtime state on the Raspberry Pi.

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
