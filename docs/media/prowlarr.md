# Prowlarr

## Purpose

Prowlarr provides centralized indexer management for the HomeLAB media stack.

It manages tracker connections and synchronizes indexer configuration to Radarr and Sonarr.

---

## Service Information

| Property | Value |
|---|---|
| Container | prowlarr |
| Image | lscr.io/linuxserver/prowlarr |
| Host Port | 9696 |
| Compose Project | media |

Web interface:

```text
http://192.168.31.10:9696
```

Persistent configuration:

```text
/srv/homelab/appdata/prowlarr
```

---

## Integration

```text
Trackers
   │
   ▼
Prowlarr
   │
   ├──► Radarr
   │
   └──► Sonarr
```

Prowlarr acts as the central point for indexer configuration instead of configuring trackers independently in each application.

Radarr uses synchronized indexers for movie searches.

Sonarr uses synchronized indexers for TV series searches.

---

## Trackers

The HomeLAB currently uses private tracker integrations through Prowlarr.

Tracker credentials and authentication data are stored in application runtime configuration and are not committed to Git.

---

## Docker Configuration

Relevant container configuration:

```yaml
environment:
  - PUID=1000
  - PGID=1000
  - TZ=Europe/Budapest

volumes:
  - /srv/homelab/appdata/prowlarr:/config

ports:
  - "9696:9696"
```

---

## Network Design

Prowlarr remains on the normal HomeLAB network.

It is not routed through Proton VPN.

Only qBittorrent torrent traffic is isolated behind Gluetun.

Prowlarr communicates with Radarr and Sonarr as part of the normal media Docker stack.

---

## Current Status

Prowlarr is deployed and running.

Current functionality includes:

- centralized indexer management
- Radarr integration
- Sonarr integration
- private tracker support
