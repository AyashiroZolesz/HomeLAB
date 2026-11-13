# Troubleshooting

This document collects real issues encountered during the HomeLAB media stack deployment and the solutions that resolved them.

The resolution examples below are historical deployment notes. The **2026-11-13** survey was read-only and did not repeat their stop, edit, remove or restart steps. Current network caveats are recorded below; application and recovery checks still need separate execution.

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

inside a container when the intended destination is in a different network namespace. Containers sharing a network namespace are an exception: their loopback interface is shared.

---

## Resolution

Check both the source container's network and the destination's network namespace before choosing an endpoint.

- Radarr, Sonarr and Prowlarr normally communicate through their shared media Docker network.
- qBittorrent and qbit-port-sync share Gluetun's network namespace. Do not assume that qBittorrent has an independent Docker DNS endpoint.
- The port-sync script deliberately calls `127.0.0.1:8081` within that shared namespace.
- A client using the published LAN WebUI reaches `192.168.31.10:8081` through Gluetun.

The saved download-client URL is application configuration; changing a Compose service name alone does not establish that URL. See [qBittorrent](qbittorrent.md) and [VPN](vpn.md).

## Docker and UFW

The survey found published Docker ports listening on all host addresses while UFW used an incoming-deny default. That default does not establish that the published ports are filtered: Docker's forwarding rules can divert traffic before UFW's rules apply. Router forwarding and Internet-facing reachability were not checked.

Review allowed and denied access paths explicitly, including IPv6, before changing firewall rules. See the [Docker firewall documentation](https://docs.docker.com/engine/network/packet-filtering-firewalls/).

## Sentinel Success and Application Health

The imported runner returns zero after recording an application state, including `DEGRADED`. A successful systemd result therefore establishes that the runner finished, not that every check passed.

The basic HTTP check accepts any received HTTP status. A `500` response can pass that reachability check. The container check also accepts running containers without a healthcheck. Neither result proves a complete media workflow.

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
- [ ] Seerr can submit a request through the intended Radarr/Sonarr integration
- [ ] VPN exit routing and forwarded-port synchronization are checked separately
- [ ] Any approved recovery action is followed by functional checks

The 2026-11-13 survey established six responding media HTTP roots, container/mount metadata and an active Sentinel timer. It did not complete this deployment checklist.

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
