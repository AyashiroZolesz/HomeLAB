# HomeLAB

Personal self-hosted infrastructure project.

---

## Goals

- Learn Linux
- Learn Docker
- Learn Networking
- Learn DevOps
- Build a reproducible infrastructure
- Document every decision and lesson learned

---

## Current stack

- Debian 13
- Docker Engine
- Docker Compose
- UFW
- Portainer
- Nginx (learning project)
- Jellyfin

---

## Services

| Service | Status | Port |
|----------|--------|------|
| Portainer | ✅ Running | 9443 |
| Nginx | ✅ Running | 8080 |
| Jellyfin | ✅ Running | 8096 |

---

## Hardware

- Toshiba Satellite L750D
- AMD A6-3400M
- 8 GB RAM
- 120 GB SSD
- 500 GB HDD

---

## Project structure

```text
/srv/homelab
├── appdata/
├── backups/
├── compose/
│   ├── jellyfin/
│   ├── nginx/
│   └── portainer/
├── docs/
├── scripts/
└── web/
```

---

## Git rules

Git stores only:

- Infrastructure
- Configuration
- Documentation
- Scripts

Git does **not** store:

- Runtime application data (`appdata/`)
- Logs
- Cache
- Temporary files
---

## Current Services

| Service | Status | Purpose |
|---|---|---|
| Portainer | Running | Docker container management |
| Jellyfin | Running | Media server |
| qBittorrent | Running | Download client |

## Media Directory Structure

```text
/srv/media/
├── downloads/
│   ├── complete/
│   └── incomplete/
├── movies/
└── series/
