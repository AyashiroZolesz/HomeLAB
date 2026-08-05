# Media Stack Overview

## Purpose

The HomeLAB media stack automates movie discovery, downloading, organization, and playback while keeping the system modular, reproducible, and easy to maintain.

Each service has a single responsibility and communicates with the others through Docker networking.

---

## Architecture

```text
                nCore
                  │
                  ▼
             Prowlarr
                  │
                  ▼
              Radarr
                  │
                  ▼
          qBittorrent
                  │
                  ▼
     /data/downloads/complete
                  │
          Hardlink Import
                  │
                  ▼
          /data/movies
                  │
                  ▼
             Jellyfin
                  │
                  ▼
               End User
```

---

## Components

| Component | Responsibility |
|-----------|----------------|
| Prowlarr | Central indexer management |
| Radarr | Movie automation |
| qBittorrent | Torrent downloading and seeding |
| Jellyfin | Media library and playback |

---

## Design Principles

The media stack follows these principles:

- One responsibility per service.
- Services communicate through Docker service names.
- Runtime data is separated from configuration.
- Configuration is version controlled.
- Media is stored only once using hardlinks whenever possible.
- Components can be replaced independently.

---

## Documentation

Detailed documentation for each component is available separately.

| Document | Purpose |
|----------|---------|
| qbittorrent.md | Download client configuration |
| prowlarr.md | Indexer management |
| radarr.md | Movie automation |
| hardlinks.md | Hardlink implementation and verification |
| troubleshooting.md | Common issues and resolutions |

---

## Current Status

### Working

- Docker Compose media stack
- Prowlarr
- Radarr
- qBittorrent
- Jellyfin
- nCore integration
- Hardlink imports
- Torrent seeding verification

### Planned

- Sonarr
- Bazarr
- Jellyseerr
- Discord notifications
- Monitoring
- Automated backups

---

## Verification

The complete movie workflow has been verified end-to-end:

1. Search request sent from Radarr.
2. Prowlarr queried the configured indexer.
3. qBittorrent downloaded the selected release.
4. Radarr imported the movie.
5. Hardlink was successfully created.
6. Jellyfin detected the movie.
7. Torrent successfully returned to the **Seeding** state.

This confirms that the complete media pipeline is functioning correctly.
