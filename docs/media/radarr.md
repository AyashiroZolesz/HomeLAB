# Radarr

## Purpose

Radarr is responsible for automating the complete movie management workflow.

Its responsibilities include:

- Managing the movie library.
- Searching for releases.
- Communicating with Prowlarr for indexers.
- Sending downloads to qBittorrent.
- Importing completed movies.
- Organizing the media library.
- Monitoring existing movies for upgrades.

---

## Service Information

| Property | Value |
|----------|-------|
| Container | radarr |
| Image | lscr.io/linuxserver/radarr |
| Host Port | 7878 |
| Compose Project | media |

---

## Communication

Radarr communicates with multiple services.

### Prowlarr

Purpose:

- Receives configured indexers.
- Performs searches through synchronized indexers.

Docker address:

```text
http://prowlarr:9696
```

---

### qBittorrent

Purpose:

- Sends torrent downloads.
- Tracks download progress.
- Imports completed downloads.

Docker address:

```text
http://qbittorrent:8080
```

Category:

```text
radarr
```

---

## Root Folder

Current library:

```text
/data/movies
```

Movies imported by Radarr are stored here.

---

## Download Workflow

The verified workflow is:

```text
Movie Added
      │
      ▼
Search
      │
      ▼
Prowlarr
      │
      ▼
Indexer
      │
      ▼
qBittorrent
      │
      ▼
Download Completed
      │
      ▼
Hardlink Import
      │
      ▼
Movie Library
      │
      ▼
Jellyfin
```

---

## Import Method

Radarr imports completed downloads using hardlinks.

Advantages:

- No duplicate storage.
- Torrent keeps seeding.
- Instant import.
- Organized movie library.

---

## Quality Profile

Current profile:

```text
HD-1080p
```

Future improvements:

- Prefer Hungarian audio.
- Prefer 5.1 audio.
- Prefer H.264 when appropriate.
- Introduce Custom Formats.
- Automatic upgrades when a better release becomes available.

---

## Docker Configuration

The container mounts:

```text
Host:
/srv/media

Container:
/data
```

Important paths:

```text
Movies:
/data/movies

Downloads:
/data/downloads
```

Using the same filesystem is required for hardlinks.

---

## Health Checks

During implementation the following warning appeared:

```text
Downloads directory does not exist inside the container.
```

Cause:

The qBittorrent configuration still referenced the old download paths.

Resolution:

- Updated qBittorrent paths.
- Restarted qBittorrent.
- Removed stale torrent entries.
- Refreshed monitored downloads.
- Verified container mounts.

The warning disappeared after the migration.

---

## Verification

The workflow was verified with:

```text
We Live in Time (2024)
```

Successful verification included:

- Search
- Download
- Import
- Hardlink creation
- Jellyfin detection
- Torrent returned to Seeding

---

## Lessons Learned

### Docker paths matter

Applications must always use container paths.

Correct:

```text
/data/movies
```

Incorrect:

```text
/srv/media/movies
```

---

### Docker service names

Services communicate using Docker DNS.

Example:

```text
qbittorrent
```

instead of fixed IP addresses.

---

### Health warnings are useful

The health page immediately highlighted the path mismatch between Radarr and qBittorrent.

Checking Health should always be part of deployment verification.

---

## Related Documentation

- overview.md
- prowlarr.md
- qbittorrent.md
- hardlinks.md
- troubleshooting.md
