# HomeLAB Documentation

Detailed technical documentation for the HomeLAB project.

The root `README.md` provides a high-level overview. This directory contains implementation details, architecture, operational procedures, troubleshooting notes, and learning documentation.

---

## Media

| Document | Description | Status |
|---|---|---|
| `media/overview.md` | Complete media stack architecture and workflow | ✅ |
| `media/qbittorrent.md` | qBittorrent configuration and seeding | ✅ |
| `media/vpn.md` | Proton VPN, Gluetun and port forwarding | ✅ |
| `media/prowlarr.md` | Indexer management | ✅ |
| `media/radarr.md` | Movie automation | ✅ |
| `media/sonarr.md` | Series automation | ✅ |
| `media/hardlinks.md` | Hardlink design and verification | ✅ |
| `media/troubleshooting.md` | Real deployment issues and fixes | ✅ |

---

## Monitoring

| Document | Description | Status |
|---|---|---|
| `monitoring/sentinel-overview.md` | Raspberry Pi Sentinel architecture and roadmap | 🚧 Active |
| `monitoring/security.md` | Sentinel SSH and privilege model | 🚧 Active |

---

## Networking

Planned documentation:

- Home network architecture
- Tailscale remote access
- router and switching layout

---

## Docker

Planned documentation:

- Docker Compose workflow
- bind mounts and persistent application data
- Docker networking
- deployment and rollback practices

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
