# HomeLAB Learning Log

This document records what was built, why decisions were made, what was learned, and which commands are worth remembering.

---

## 2026-07-29 – qBittorrent and Jellyfin Media Workflow

### What Was Built

- qBittorrent deployed with Docker Compose
- Persistent qBittorrent configuration
- Complete and incomplete download directories
- qBittorrent WebUI on TCP port 8081
- Torrent traffic ports exposed on TCP and UDP 6881
- Shared download storage using a Docker bind mount
- Manual media import into the Jellyfin movie library

### Why It Was Built This Way

The qBittorrent application configuration is stored separately from downloaded files.

```text
/srv/homelab/appdata/qbittorrent
