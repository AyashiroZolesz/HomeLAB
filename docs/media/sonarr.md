# Sonarr

## Purpose

Sonarr manages TV series acquisition and organization in the HomeLAB media stack.

It works together with Prowlarr for indexer access, qBittorrent for downloading, and Jellyfin for playback.

---

## Service Information

| Property | Value |
|---|---|
| Container | sonarr |
| Image | lscr.io/linuxserver/sonarr |
| Host Port | 8989 |
| Compose Project | media |

Web interface:

```text
http://192.168.31.10:8989
```

Persistent configuration:

```text
/srv/homelab/appdata/sonarr
```

Media mount:

```text
/srv/media -> /data
```

---

## Integration

```text
Prowlarr
   │
   ▼
Sonarr
   │
   ▼
qBittorrent
   │
   ▼
/data/downloads
   │
Hardlink Import
   │
   ▼
/data/series
   │
   ▼
Jellyfin
```

Prowlarr provides indexer access.

qBittorrent handles downloading and seeding.

Sonarr monitors completed downloads and imports episodes into the series library.

Jellyfin scans the resulting series library for playback.

---

## Storage

Series library:

```text
/data/series
```

Downloads:

```text
/data/downloads
```

Sonarr uses the common `/data` filesystem layout shared by the media stack.

This allows completed downloads to be imported using hardlinks where possible.

---

## Network Design

Sonarr remains on the normal HomeLAB network.

It is not routed through Proton VPN.

Only qBittorrent torrent traffic is isolated behind Gluetun.

---

## Current Status

Sonarr is deployed and running as part of the media Compose stack.

Current functionality includes:

- TV series management
- Prowlarr integration
- qBittorrent download handling
- shared `/data` filesystem
- hardlink-compatible imports
- Jellyfin series library integration
