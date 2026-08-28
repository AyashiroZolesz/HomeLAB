# HomeLAB

Personal self-hosted infrastructure and learning project.

The goal is to build a reproducible, documented and maintainable home infrastructure while learning Linux, Docker, networking, storage, automation and operations.

---

## Current Platform

### Main HomeLAB

- Debian 13
- Docker Engine
- Docker Compose
- UFW
- Tailscale
- Toshiba Satellite L750D
- AMD A6-3400M
- 8 GB RAM
- 120 GB SSD
- 500 GB HDD

### Sentinel Node

- Raspberry Pi 3 class hardware
- Debian 13
- ARM64 / Cortex-A53
- ~1 GB RAM
- Ethernet: `192.168.31.11`
- Tailscale enabled
- Sentinel monitoring project under development

---

## Current Services

| Service | Purpose | Port |
|---|---|---:|
| Jellyfin | Media playback | 8096 |
| qBittorrent | Download client | 8081 |
| Gluetun | Proton VPN gateway for qBittorrent | internal |
| qbit-port-sync | Proton forwarded-port synchronization | internal |
| Radarr | Movie automation | 7878 |
| Sonarr | Series automation | 8989 |
| Prowlarr | Indexer management | 9696 |
| Portainer | Docker management | 9443 |
| Nginx | Web / learning service | 8080 |

Planned:

- Seerr request management
- Sentinel automated diagnostics and recovery
- Telegram notifications

---

## Media Architecture

```text
Trackers
   │
   ▼
Prowlarr
   │
   ├──────────► Radarr ─────► Movies
   │
   └──────────► Sonarr ─────► Series
                        │
                        ▼
                  qBittorrent
                        │
                        ▼
                     Gluetun
                        │
                        ▼
                  Proton VPN
```

Only qBittorrent torrent traffic is routed through Proton VPN.

Radarr, Sonarr, Prowlarr and Jellyfin remain on the normal HomeLAB network.

---

## Media Storage

```text
/srv/media/
├── downloads/
│   ├── complete/
│   └── incomplete/
├── movies/
└── series/
```

Radarr and Sonarr use hardlinks where possible so downloaded media can remain available for seeding without consuming duplicate disk space.

---

## Sentinel

The Raspberry Pi is being developed as an independent monitoring, diagnostics and recovery node.

Target flow:

```text
check
  ↓
confirm
  ↓
diagnose
  ↓
safe recovery
  ↓
verify
  ↓
notify
```

Current implementation:

- HomeLAB ping check
- SSH connectivity check
- HTTP service checks
- Dedicated Sentinel SSH key
- Dedicated `sentinel` account on HomeLAB
- Restricted read-only sudo permissions

Planned Sentinel features:

- Docker container state monitoring
- disk / RAM / load monitoring
- Gluetun and Proton VPN validation
- qBittorrent forwarded-port validation
- automated recovery with bounded retries
- Telegram notifications
- incident history
- log rotation

---

## Repository Structure

```text
/srv/homelab
├── appdata/
├── backups/
├── compose/
│   ├── jellyfin/
│   ├── media/
│   ├── nginx/
│   └── portainer/
├── docs/
│   ├── media/
│   └── monitoring/
├── scripts/
└── web/
```

---

## Git Policy

Git stores:

- infrastructure configuration
- Docker Compose definitions
- scripts
- documentation

Git does not store:

- runtime application data
- logs
- credentials
- API keys
- VPN private keys
- generated caches
- local rollback copies

---

## Documentation

Detailed technical documentation is maintained under:

```text
docs/
```

The documentation is part of the implementation process and should follow the real deployed system closely enough that the environment can be understood and rebuilt without relying on memory.
