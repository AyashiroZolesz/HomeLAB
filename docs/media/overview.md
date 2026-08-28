# Media Stack Overview

## Purpose

The HomeLAB media stack automates movie and TV series discovery, downloading, organization, seeding, and playback.

---

## Architecture

```text
                 Trackers
                    │
                    ▼
                Prowlarr
                /      \
               ▼        ▼
           Radarr      Sonarr
               \        /
                \      /
                 ▼    ▼
              qBittorrent
                    │
                    ▼
                 Gluetun
                    │
                    ▼
                Proton VPN

Downloads:
    /data/downloads
        │
        ├── hardlink ──► /data/movies
        │
        └── hardlink ──► /data/series
                            │
                            ▼
                         Jellyfin
```

---

## Components

| Component | Responsibility |
|---|---|
| Prowlarr | Central indexer management |
| Radarr | Movie automation |
| Sonarr | TV series automation |
| qBittorrent | Downloading and seeding |
| Gluetun | Proton VPN network gateway |
| qbit-port-sync | Dynamic Proton port synchronization |
| Jellyfin | Media library and playback |

---

## Storage

All media-aware containers use the same filesystem mapping:

```text
/srv/media -> /data
```

Relevant directories:

```text
/data/downloads
/data/movies
/data/series
```

The shared `/data` filesystem layout allows Radarr and Sonarr to import completed downloads using hardlinks where possible.

---

## VPN Design

Only qBittorrent torrent traffic is routed through Proton VPN.

Radarr, Sonarr, Prowlarr and Jellyfin remain on the normal HomeLAB network.

qBittorrent shares the Gluetun network namespace.

Proton port forwarding is synchronized to qBittorrent automatically by the `qbit-port-sync` sidecar.

---

## Current Status

Working:

- Jellyfin
- qBittorrent
- Gluetun
- Proton VPN
- Proton port forwarding
- qbit-port-sync
- Radarr
- Sonarr
- Prowlarr
- hardlink imports
- private tracker integration
- Tailscale remote access

Planned:

- Seerr
- Sentinel integration
- automated backups
- expanded monitoring

---

## Design Principles

- One responsibility per service
- Persistent configuration is separated from media
- Shared filesystem layout enables hardlinks
- Secrets are excluded from Git
- Torrent traffic is isolated behind VPN
- The rest of the media stack stays on the normal network
- Documentation follows the deployed system
