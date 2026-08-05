# Troubleshooting

This document collects real issues encountered during the HomeLAB media stack deployment and the solutions that resolved them.

---

# Radarr Health Warning

## Symptom

```text
You are using docker; download client qBittorrent places downloads in
/downloads/complete but this directory does not appear to exist inside the container.
```

## Cause

The Docker volume configuration had already been migrated to:

```text
/data
```

However, qBittorrent still contained the old persistent paths:

```text
/downloads/complete
/downloads/incomplete
```

---

## Resolution

1. Stop qBittorrent.
2. Update the stored paths.
3. Start qBittorrent.
4. Refresh monitored downloads.
5. Remove stale torrent entries.
6. Run Health Check again.

Result:

```text
Health warning disappeared.
```

---

# Duplicate Movie Files

## Symptom

The imported movie existed twice.

Example:

```text
downloads/
movies/
```

Both contained a complete copy.

---

## Verification

Before deleting anything:

```bash
cmp -s <movie> <download>
```

Result:

```text
IDENTICAL
```

---

## Resolution

1. Remove the duplicate copy.
2. Create a hardlink.
3. Verify inode numbers.

Expected:

```text
Links: 2
```

---

# Torrent Starts Downloading Again

## Symptom

Re-adding the torrent starts a new download instead of checking existing data.

---

## Cause

The torrent cannot find the expected file structure.

---

## Resolution

- Verify the download path.
- Verify the torrent root directory.
- Place the file exactly where the torrent expects it.
- Re-add the torrent.
- Allow qBittorrent to hash-check the data.

Expected result:

```text
Checking
↓

100%

↓

Seeding
```

---

# Missing Files

## Symptom

Torrent status:

```text
Missing Files
```

---

## Possible Causes

- Manual file movement
- Incorrect Docker paths
- Wrong save path
- Different folder structure

---

## Resolution

- Restore the expected file path.
- Run Force Recheck.
- Re-add the torrent if necessary.

---

# Hardlinks Not Working

## Symptoms

- Duplicate storage usage.
- Slow imports.
- Seeding stops after import.

---

## Cause

Containers do not share the same filesystem.

Incorrect:

```text
/downloads
/media
```

Correct:

```text
/data
```

---

# Docker Networking

## Symptom

Applications cannot communicate.

---

## Cause

Using:

```text
localhost
```

inside a container.

---

## Resolution

Always use Docker service names.

Example:

```text
qbittorrent
radarr
prowlarr
```

---

# Deployment Checklist

After every deployment verify:

- [ ] Containers running
- [ ] Docker networking works
- [ ] Prowlarr sync successful
- [ ] Radarr download client connected
- [ ] Health page clean
- [ ] Hardlinks verified
- [ ] Jellyfin imports movies
- [ ] Torrent returns to Seeding

---

# Lessons Learned

The majority of deployment issues were caused by configuration mismatches rather than software defects.

The most important checks are:

1. Docker mount paths
2. Container paths
3. Persistent application configuration
4. Hardlink verification
5. Health page
6. Torrent hash check
