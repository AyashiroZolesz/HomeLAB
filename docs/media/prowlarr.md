# Prowlarr

## Purpose

Prowlarr is the centralized indexer manager of the HomeLAB media stack.

Instead of configuring every indexer separately in Radarr, Sonarr, or future applications, Prowlarr manages them from a single location and synchronizes them automatically.

---

## Responsibilities

Prowlarr is responsible for:

- Managing torrent indexers
- Testing indexer connectivity
- Synchronizing indexers with media applications
- Managing API communication with supported ARR applications
- Reducing duplicated configuration

---

## Service Information

| Property | Value |
|----------|-------|
| Container | prowlarr |
| Image | lscr.io/linuxserver/prowlarr |
| Host Port | 9696 |
| Compose Project | media |

---

## Communication

Prowlarr communicates with:

### Indexers

Current:

```text
nCore
```

Future:

- Additional private trackers
- Public indexers (if required)

---

### Applications

Current:

```text
Radarr
```

Future:

```text
Sonarr
```

Docker communication:

```text
http://radarr:7878
```

Future:

```text
http://sonarr:8989
```

---

## Synchronization

Prowlarr pushes indexer configuration directly into supported ARR applications.

Current synchronization:

```text
Prowlarr
        │
        ▼
     Radarr
```

Future:

```text
          Prowlarr
          /      \
         ▼        ▼
    Radarr     Sonarr
```

This ensures that indexers only need to be configured once.

---

## Current Configuration

Verified components:

- nCore indexer
- Radarr application
- API communication
- Full synchronization
- Interactive search
- Automatic search
- RSS synchronization

---

## Security

Private tracker credentials are stored only inside Prowlarr.

Git must never contain:

- Username
- Password
- Cookies
- API Keys

Runtime configuration is stored under:

```text
/srv/homelab/appdata/prowlarr
```

---

## Verification

The following workflow was verified:

1. Radarr requested a movie search.
2. Prowlarr received the request.
3. nCore returned matching releases.
4. Prowlarr passed the results back to Radarr.
5. Radarr successfully selected and downloaded the release.

---

## Lessons Learned

### Configure indexers only once

Without Prowlarr every ARR application would require its own indexer configuration.

With Prowlarr:

- One configuration
- Multiple applications
- Easier maintenance

---

### Docker networking

Applications communicate using Docker service names.

Example:

```text
http://radarr:7878
```

instead of fixed IP addresses.

---

### Keep credentials centralized

All tracker credentials remain inside Prowlarr.

Other applications receive only synchronized indexer definitions.

This simplifies management and reduces duplicated configuration.

---

## Related Documentation

- overview.md
- radarr.md
- qbittorrent.md
- troubleshooting.md
