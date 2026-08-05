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
| Host Port | 8081 |
| Internal Port | 8080 |
| Compose Project | media |

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

Current category:

```text
radarr
```

Planned categories:

```text
radarr
sonarr
```

Categories allow multiple automation services to share the same download client.

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

Verified download paths:

```text
Default Save Path:
/data/downloads/complete

Incomplete Path:
/data/downloads/incomplete
```

---

## Verification

The configuration was verified by:

- Downloading a movie through Radarr.
- Importing it successfully.
- Re-adding the torrent.
- Running a hash check.
- Returning to **Seeding** without downloading the movie again.

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

- overview.md
- radarr.md
- hardlinks.md
- troubleshooting.md
