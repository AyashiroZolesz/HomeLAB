# qBittorrent

## Purpose

qBittorrent is the download client of the HomeLAB media stack.

Its responsibilities are:

- Download torrent data.
- Verify downloaded files.
- Continue seeding completed torrents.
- Expose a WebUI for automation tools.
- Communicate with Radarr through the qBittorrent Web API.

---

## Service Information

| Property | Value |
|----------|-------|
| Container | qbittorrent |
| Image | lscr.io/linuxserver/qbittorrent |
| Host WebUI Port | 8081, published by Gluetun |
| Network | Gluetun network namespace, shared with qbit-port-sync |
| Compose Project | media |

Survey date: **2026-11-13**. qBittorrent was running and its WebUI root returned HTTP `200` from the Pi. Authentication, current torrent state and application API integrations were not tested.

## WebUI Access

The active media stack owns qBittorrent; Gluetun publishes its WebUI on the host's port `8081`. qBittorrent does not have a separate published host port in the inspected runtime.

For an application on the media Docker network, the configured endpoint must reach the shared Gluetun network namespace. Do not assume that qBittorrent has an independent Docker DNS endpoint. Confirm the configured WebUI listening port and network reachability before changing a download-client URL. A client using the LAN endpoint reaches `http://192.168.31.10:8081`.

The separate `compose/qbittorrent/compose.yaml` is not the configuration source identified for the running media project.

---

## Storage Layout

The container mounts the complete media directory:

```text
Host:
/srv/media

Container:
/data
```

Relevant paths:

```text
/data/downloads/complete
/data/downloads/incomplete
```

Downloads remain inside the download directory even after Radarr imports the movie.

---

## Download Categories

The earlier deployment notes recorded this category:

```text
radarr
```

The documented intended categories are:

```text
radarr
sonarr
```

Categories allow multiple automation services to share the same download client.

The current category configuration was not read during the survey. In particular, the presence of a running Sonarr container does not establish its download category or integration result.

---

## Seeding

After Radarr imports a movie, qBittorrent continues seeding the original torrent.

This is possible because Radarr creates a hardlink instead of moving the file.

The expected final torrent state is:

```text
100%
Seeding
```

Upload speed may remain **0 B/s** if no peers currently request data.

---

## Configuration

Previously documented download paths:

```text
Default Save Path:
/data/downloads/complete

Incomplete Path:
/data/downloads/incomplete
```

The survey confirmed the `/srv/media -> /data` mount, without reading the saved application paths or credentials.

---

## Verification

The earlier deployment notes report verification by:

- Downloading a movie through Radarr.
- Importing it successfully.
- Re-adding the torrent.
- Running a hash check.
- Returning to **Seeding** without downloading the movie again.

These actions were not repeated on 2026-11-13. A new end-to-end check must also cover Sonarr/Seerr integration, the VPN exit path, forwarded-port synchronization and continued seeding after import.

---

## Lessons Learned

### Use the same filesystem

qBittorrent and Radarr must use the same mounted filesystem:

```text
/data
```

instead of separate mounts such as:

```text
/downloads
/media
```

This enables hardlinks.

### Existing configuration matters

Changing Docker mounts alone is not enough.

The saved download paths inside qBittorrent must also match the new container paths.

---

## Related Documentation

- [Overview](overview.md)
- [Radarr](radarr.md)
- [Hardlinks](hardlinks.md)
- [VPN and port synchronization](vpn.md)
- [Troubleshooting](troubleshooting.md)
