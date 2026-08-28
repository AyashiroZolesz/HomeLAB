# qBittorrent VPN

## Purpose

qBittorrent torrent traffic is routed through Proton VPN while the rest of the HomeLAB media stack remains on the normal network.

This keeps torrent traffic isolated without routing Jellyfin, Radarr, Sonarr or Prowlarr through the VPN.

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

The WireGuard configuration is stored at:

```text
/srv/homelab/appdata/gluetun/wireguard/wg0.conf
```

VPN credentials and private keys are runtime data and are not stored in Git.

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

The synchronization script is stored at:

```text
/srv/homelab/appdata/gluetun/update-qbit-port.sh
```

The script also ensures that qBittorrent uses the VPN interface.

---

## Network Binding

qBittorrent is bound to the VPN interface inside the shared Gluetun network namespace.

Expected interface:

```text
tun0
```

This prevents torrent traffic from using the normal HomeLAB network interface.

---

## Deployment Notes

The Proton WireGuard configuration originally included IPv6 settings that were not accepted by the current Gluetun setup, so the VPN configuration was changed to IPv4-only addressing.

Direct automatic synchronization of the Proton forwarded port from Gluetun to qBittorrent was not reliable in the chosen setup.

A dedicated `qbit-port-sync` sidecar was introduced instead.

qBittorrent also required explicit VPN interface binding in addition to synchronizing the forwarded port.

---

## Restart Behaviour

qBittorrent and qbit-port-sync share Gluetun's network namespace.

If Gluetun is restarted, the dependent containers may also need to reconnect to the recreated network namespace.

This dependency is planned to be handled later by Sentinel recovery automation.

---

## Security

The following must never be committed to Git:

- WireGuard private keys
- Proton VPN credentials
- qBittorrent credentials
- application runtime data

Sensitive files remain under ignored `appdata` directories.
