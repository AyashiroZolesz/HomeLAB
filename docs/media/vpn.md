# qBittorrent VPN

## Purpose

The deployed design routes qBittorrent torrent traffic through Proton VPN while the rest of the HomeLAB media stack remains on the normal network.

This keeps torrent traffic isolated without routing Jellyfin, Radarr, Sonarr or Prowlarr through the VPN.

Survey and source review: **2026-11-13**. The existing deployment sources were copied for review without changing the running services. Container metadata and HTTP reachability were inspected; the VPN exit path and recovery behavior were not exercised.

---

## Architecture

```text
Internet
   │
   ▼
Proton VPN
   │
WireGuard
   │
   ▼
Gluetun
   │
   ├── qBittorrent
   └── qbit-port-sync
```

qBittorrent shares the Gluetun network namespace:

```yaml
network_mode: "service:gluetun"
```

This means qBittorrent does not use an independent Docker network path for Internet access.

---

## Gluetun

Gluetun provides the WireGuard connection to Proton VPN.

Runtime configuration is stored under:

```text
/srv/homelab/appdata/gluetun/
```

The Compose file references runtime WireGuard configuration outside the versioned sources. VPN credentials and private keys were not copied into the repository.

---

## Port Forwarding

Proton dynamically assigns an incoming torrent port.

Gluetun stores the current forwarded port in:

```text
/tmp/gluetun/forwarded_port
```

The host-mounted copy is available at:

```text
/srv/homelab/appdata/gluetun/tmp/forwarded_port
```

The assigned port is dynamic and can change after VPN reconnects.

---

## qbit-port-sync

`qbit-port-sync` is a small Alpine sidecar used to synchronize Proton's forwarded port with qBittorrent.

It reads the forwarded port from Gluetun and updates qBittorrent through its Web API.

The versioned source is [scripts/media/update-qbit-port.sh](../../scripts/media/update-qbit-port.sh). The current deployed script is stored at:

```text
/srv/homelab/appdata/gluetun/update-qbit-port.sh
```

Compose still mounts that existing runtime path. Adding the versioned source does not install it there or change the active mount.

The script reads the forwarded-port file and POSTs preferences to `http://127.0.0.1:8081/api/v2/app/setPreferences` in the shared network namespace. It requests the listening port, `tun0` binding, disabled random-port selection and disabled UPnP. It does not perform a login, so successful requests depend on the configured qBittorrent API access policy.

Its retry loop has no attempt limit and it does not read the preferences back after a successful HTTP request. The source records the existing implementation; this import does not claim that synchronization was functionally tested.

---

## Network Binding

The deployed design binds qBittorrent to the VPN interface inside the shared Gluetun network namespace. The imported script attempts to set that binding; the saved application preference was not read during this survey.

Expected interface:

```text
tun0
```

Binding is intended to restrict torrent traffic to that interface. Verify the actual interface, exit address and failure behavior before treating it as evidence of traffic isolation.

---

## Deployment Notes

The earlier deployment notes report that the Proton WireGuard configuration originally included IPv6 settings that were not accepted by that Gluetun setup, so the VPN configuration was changed to IPv4-only addressing. This was not reconfigured during the survey.

Direct automatic synchronization of the Proton forwarded port from Gluetun to qBittorrent was not reliable in the chosen setup.

A dedicated `qbit-port-sync` sidecar was introduced instead.

qBittorrent also required explicit VPN interface binding in addition to synchronizing the forwarded port.

---

## Restart Behaviour

qBittorrent and qbit-port-sync share Gluetun's network namespace.

If Gluetun is restarted, the dependent containers may also need to reconnect to the recreated network namespace.

The main host already permits a separate [sentinel-recover-media](../../scripts/sentinel/sentinel-recover-media) helper with the `vpn-stack` argument. It restarts Gluetun, performs up to twelve health-status polls with five-second sleeps, then restarts qBittorrent and qbit-port-sync. It does not perform a functional VPN or port check after restarting the dependents, and it has no overall execution timeout.

The imported Sentinel Python checks do not invoke this helper automatically. No recovery action was run during the survey. Review the [Sentinel security notes](../monitoring/security.md) before introducing automated recovery.

## Diagnostic Limits

The imported [media-status helper](../../scripts/sentinel/sentinel-media-status) reads the forwarded-port file and filters qBittorrent listeners for a fixed VPN address. The Sentinel media check compares that value with a saved qBittorrent port and looks for TCP/UDP listeners at that address.

These checks do not establish the current external Proton port allocation, Internet-side port reachability, the VPN exit IP or absence of traffic leaks. The fixed VPN address is deployment-specific and must be reviewed if the VPN setup changes.

---

## Security

The following must never be committed to Git:

- WireGuard private keys
- Proton VPN credentials
- qBittorrent credentials
- application runtime data

Sensitive files remain under ignored `appdata` directories.
