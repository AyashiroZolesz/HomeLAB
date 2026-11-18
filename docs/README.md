# HomeLAB Documentation

Detailed technical documentation for the HomeLAB project.

The [root README](../README.md) provides the platform, network and service inventory. This directory contains implementation details, troubleshooting notes and learning documentation.

The current read-only deployment survey is dated **2026-11-13**. Survey observations and earlier deployment tests are identified separately. Older examples do not establish the current outcome of an application workflow.

---

## Media

| Document | Description | Status |
|---|---|---|
| [Overview](media/overview.md) | Seerr, media architecture, runtime mounts and verification limits | Survey updated |
| [qBittorrent](media/qbittorrent.md) | WebUI access through Gluetun, storage and seeding | Survey updated |
| [VPN](media/vpn.md) | Proton VPN, Gluetun and port synchronization | Survey updated |
| [Prowlarr](media/prowlarr.md) | Indexer management | Deployment notes |
| [Radarr](media/radarr.md) | Movie automation | Deployment notes |
| [Sonarr](media/sonarr.md) | Series automation | Deployment notes |
| [Hardlinks](media/hardlinks.md) | Hardlink design and earlier verification | Historical test evidence |
| [Troubleshooting](media/troubleshooting.md) | Earlier issues and current network caveats | Survey updated |

---

## Monitoring

| Document | Description | Status |
|---|---|---|
| [Sentinel overview](monitoring/sentinel-overview.md) | Pi runtime, source layout and remaining verification | Source and runtime reviewed |
| [Sentinel security](monitoring/security.md) | Observed diagnostic and recovery permissions | Survey updated |

## Dashboard

| Document | Description | Status |
|---|---|---|
| [Homarr](dashboard/homarr.md) | Private HTTPS, eight HomeLAB tiles, six integrations, deployment and restore | Deployed and reviewed; manual checks listed |

---

## Networking

The [root inventory](../README.md#network) records the owner-confirmed router/switch models and the observed node roles. The Pi's advertised subnet route was observed on November 18; the owner confirmed Homarr and Jellyfin access on mobile data with Tailscale enabled. Other remote application links, router settings and exit-node operation remain unverified. Homarr's dedicated private HTTPS endpoint is documented in the [dashboard runbook](dashboard/homarr.md).

---

## Docker

Further documentation and verification:

- Docker Compose workflow
- bind mounts and persistent application data
- Docker networking
- deployment and rollback practices

The November 13 source refresh did not change running services. The November 18 Homarr deployment adds a separate Compose project; its current verification state is recorded in the dashboard runbook. Backup infrastructure, DNS filtering and automated hardware migration are deferred. A tested application restore procedure is still needed.

---

## Documentation Philosophy

Each document should answer:

- What was built?
- Why was it built this way?
- How is it configured?
- How was it verified?
- What problems were encountered?
- What was learned?
- Which commands are useful later?

The repository documentation should follow the real deployed system closely enough that the HomeLAB can be understood, maintained, and rebuilt without relying on memory.
