# Radarr

## Purpose

Radarr manages movie acquisition, organization and upgrades in the HomeLAB media stack.

It works together with Prowlarr for indexers, qBittorrent for downloading, and Jellyfin for playback.

---

## Service Information

| Property | Value |
|---|---|
| Container | radarr |
| Image | lscr.io/linuxserver/radarr |
| Host Port | 7878 |
| Compose Project | media |

Web interface:

```text
http://192.168.31.10:7878
```

Persistent configuration:

```text
/srv/homelab/appdata/radarr
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
Radarr
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
/data/movies
   │
   ▼
Jellyfin
```

Prowlarr provides indexer access.

qBittorrent handles downloading and seeding.

Radarr monitors completed downloads and imports movies into the library.

Jellyfin scans the resulting movie library for playback.

---

## Storage

Movie library:

```text
/data/movies
```

Downloads:

```text
/data/downloads
```

All media-aware containers use the common `/data` filesystem layout.

This allows Radarr to create hardlinks instead of copying completed torrent data.

---

## Hardlink Imports

Hardlinks allow:

- continued torrent seeding
- organized movie files under `/data/movies`
- no duplicate storage usage
- fast imports

Hardlink operation has been verified on the deployed HomeLAB filesystem.

---

## Quality Profile

Current custom profile:

```text
HUN 1080p
```

Main policy:

- Hungarian audio preferred
- 1080p preferred
- 720p available as fallback
- 2160p excluded
- H.264 / x264 preferred through Custom Formats
- unnecessary REMUX / 3D / 4K releases avoided

The profile is intended to balance quality, compatibility and storage usage.

---

## Network Design

Radarr remains on the normal HomeLAB network.

It is not routed through Proton VPN.

qBittorrent torrent traffic is isolated behind Gluetun.

The qBittorrent WebUI is exposed through Gluetun on:

```text
192.168.31.10:8081
```

The exact download-client endpoint configured inside Radarr is application configuration and should not be assumed from the Docker service name alone.

---

## Current Status

Radarr is deployed and running as part of the media Compose stack.

Current functionality includes:

- movie management
- Prowlarr integration
- qBittorrent download handling
- hardlink imports
- custom `HUN 1080p` quality policy
- Jellyfin movie library integration
- private tracker usage
