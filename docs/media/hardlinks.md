# Hardlinks

## Purpose

The HomeLAB media stack uses hardlinks to avoid storing duplicate copies of the same movie.

A completed download remains available for torrent seeding while the organized movie library becomes immediately available to Jellyfin.

Only one physical copy of the movie exists on disk.

---

## Why Hardlinks?

Without hardlinks:

```text
Downloads
└── Movie.mkv (8 GB)

Movies
└── Movie.mkv (another 8 GB)
```

Total storage:

```text
16 GB
```

With hardlinks:

```text
Downloads
└── Movie.mkv
        │
        │
        └───────────────┐
                        │
Movies                  │
└── Movie.mkv ◄─────────┘
```

Both directory entries reference the same physical data.

Total storage:

```text
8 GB
```

---

## Requirements

Hardlinks only work when:

- Source and destination are on the same filesystem.
- Both applications see the same filesystem.
- Docker mounts are identical.

Current configuration:

```yaml
volumes:
  - /srv/media:/data
```

Container paths:

```text
Downloads:
/data/downloads

Movies:
/data/movies
```

---

## Verification

The following movie was used:

```text
We Live in Time (2024)
```

Verification command:

```bash
stat \
"/srv/media/movies/We Live in Time (2024)/We.Live.in.Time.2024.1080p.WEB.H264-AccomplishedYak.mkv" \
"/srv/media/downloads/complete/We.Live.in.Time.2024.1080p.WEB.H264-AccomplishedYak/we.live.in.time.2024.1080p.web.h264-accomplishedyak.mkv"
```

Expected result:

```text
Inode: identical
Links: 2
```

Both files must have:

- identical inode
- identical device
- identical size
- link count of two

---

## Byte Verification

Before replacing the duplicate copy with a hardlink, both files were compared.

Command:

```bash
cmp -s <movie> <download> \
&& echo "IDENTICAL" || echo "DIFFERENT"
```

Result:

```text
IDENTICAL
```

Only after confirming identical contents was the duplicate removed.

---

## Migration Procedure

The duplicate copy was replaced safely using the following sequence:

1. Verify both files are identical.
2. Remove the duplicate movie copy.
3. Create a hardlink.
4. Verify inode numbers.
5. Re-add the torrent.
6. Allow qBittorrent to hash-check the data.
7. Confirm **100%** and **Seeding**.

---

## Lessons Learned

### Never assume files are identical

Always verify with:

```bash
cmp
```

before deleting a large file.

---

### Verify using inode numbers

The inode number proves whether two directory entries reference the same file.

Checking file size alone is not sufficient.

---

### Hardlinks preserve seeding

Radarr can organize the movie library while qBittorrent continues seeding the original torrent.

No additional storage is consumed.

---

## Related Documentation

- overview.md
- qbittorrent.md
- radarr.md
- troubleshooting.md
