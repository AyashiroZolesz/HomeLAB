# HomeLAB Learning Log

This document records what was built, why decisions were made, what was learned, and which commands are worth remembering.

---

## 2026-07-29 – qBittorrent and Jellyfin Media Workflow

### What Was Built

- qBittorrent deployed with Docker Compose
- Persistent qBittorrent configuration
- Complete and incomplete download directories
- qBittorrent WebUI on TCP port 8081
- Torrent traffic ports exposed on TCP and UDP 6881
- Shared download storage using a Docker bind mount
- Manual media import into the Jellyfin movie library

### Why It Was Built This Way

The qBittorrent application configuration is stored separately from downloaded files.

```text
/srv/homelab/appdata/qbittorrent
```

---

## 2026-08-28 – Proton VPN Integration and Sentinel Bootstrap

### What Was Built

- Gluetun added to the media Docker Compose stack
- qBittorrent moved behind the Gluetun network namespace
- Proton VPN WireGuard connection configured
- Proton dynamic port forwarding enabled
- `qbit-port-sync` sidecar added
- qBittorrent listening port synchronized automatically with Proton
- qBittorrent bound to the VPN interface
- Torrent traffic externally verified through the Proton exit IP
- Raspberry Pi Sentinel monitoring node initialized
- Dedicated Sentinel SSH key created
- Dedicated `sentinel` account created on the HomeLAB server
- Restricted read-only diagnostic sudo permissions added
- Initial network and HTTP service checks implemented

### Why It Was Built This Way

Only qBittorrent needs torrent traffic isolation, so the complete media stack is not routed through the VPN.

Gluetun provides a dedicated VPN network namespace for qBittorrent while Radarr, Sonarr, Prowlarr and Jellyfin remain normally reachable on the HomeLAB network.

The Raspberry Pi Sentinel is kept independent from the main HomeLAB server so it can detect and diagnose failures even when the main server has problems.

### Problems Encountered

- Proton WireGuard IPv6 configuration was incompatible with the current Gluetun setup
- Proton forwarded ports are dynamic and cannot be configured as a permanent qBittorrent port
- automatic Gluetun-to-qBittorrent port synchronization required a separate sidecar
- qBittorrent required explicit VPN interface binding
- restarting Gluetun can require dependent containers to reconnect to its recreated network namespace

### What Was Learned

- a working VPN tunnel does not automatically prove that application traffic is using it correctly
- VPN routing, forwarded ports and application interface binding are separate concerns
- runtime verification is more reliable than configuration files alone
- Docker containers sharing another container's network namespace have a lifecycle dependency on that container
- monitoring and recovery automation should use least privilege instead of unrestricted Docker or root access

### Next Steps

- continue Sentinel monitoring implementation
- add safe bounded recovery actions
- add Telegram notifications
- add persistent incident history
- integrate VPN and qBittorrent health checks into Sentinel
