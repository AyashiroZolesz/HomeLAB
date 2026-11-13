# Sentinel Security

## Purpose

Sentinel has access to the main HomeLAB server for diagnostics and an explicitly permitted VPN-stack recovery helper.

The goal is to provide enough access for monitoring without giving the Raspberry Pi unrestricted root privileges.

Survey and source review: **2026-11-13**. The statements below describe observed configuration and imported source behavior. This repository refresh does not change privileges or deploy the copied code.

---

## Dedicated Account

The HomeLAB server uses a dedicated user:

```text
sentinel
```

This account is used only by the Sentinel monitoring node.

It is separate from the normal administrative user account.

The inspected group membership contained only its own group; no Docker group membership was reported. On the Pi, however, `sentinel.service` runs as the administrative account rather than a separate Sentinel runtime user.

---

## SSH Authentication

The imported host-health and media-check sources select a dedicated SSH identity and the main host's `sentinel` account, with batch mode and a connection timeout. The key's algorithm and server-side restrictions were not re-inspected; no private key was copied.

The current source hardcodes the SSH destination and identity path. The operator's password-authenticated survey sessions are separate from this service-to-service access.

---

## Restricted Privileges

The owner-run `sudo -l -U sentinel` query reported the following passwordless root command permissions:

Current allowed operations include:

```text
/usr/bin/docker ps *
/usr/bin/docker inspect *
/usr/bin/docker logs *
/usr/bin/df *
/usr/bin/free *
/usr/bin/uptime
/usr/local/sbin/sentinel-media-status
/usr/local/sbin/sentinel-recover-media vpn-stack
```

The recovery permission authorizes a helper that restarts containers. The account is not limited to read-only operations.

Diagnostic access also requires care: unrestricted inspect output can include environment secrets, and container logs can contain credentials. A future tightening should expose only the required fields through reviewed helpers. The survey used selected metadata and did not dump complete container configurations or runtime logs.

---

## Recovery Permissions

The imported [recovery helper](../../scripts/sentinel/sentinel-recover-media) checks for the `vpn-stack` action, restarts Gluetun, waits for its reported health and restarts qBittorrent plus qbit-port-sync. The imported Python programs do not call this helper automatically.

Effective helper ownership, permissions and SSH-key restrictions were not established by copying the source. Root-owned, non-service-writable helpers and a narrow action boundary remain requirements for an access-control review.

The helper does not have an overall execution timeout, a lock or a functional post-restart check. Source review is not a successful recovery test; no recovery action was run during the survey.

## Pi Runtime and Source Integrity

The observed Python source directory and two entry-point files are owned by the same administrative account that runs the service. Their reported modes were `775`; the YAML configuration was `664`. The inspected service properties had `NoNewPrivileges=no` and `ProtectSystem=no`.

These facts do not by themselves prove an exploit. They mean the service has no separation from that account's source/configuration ownership, and the inspected systemd protections are absent. A separate runtime account, restricted writable paths and compatible service protections should be planned together rather than enabled without checking SSH and state-write requirements.

## Telegram Error Handling

The Telegram source reads its token and destination from environment variables. The repository contains only an empty [environment example](../../sentinel/telegram.env.example), not the populated file.

The request URL contains the bot token at runtime. `runner.py` prints notification exception text, and a requests HTTP exception can include that URL. Service logs may therefore disclose the token on a delivery failure. Avoid publishing logs without a secret review. Error redaction is a separate functional change; the imported implementation was not modified in this refresh.

---

## Design Principles

The intended security model is:

- dedicated service account
- dedicated SSH key
- least privilege
- selected diagnostics by default
- explicit recovery permissions
- no unrestricted root access
- no Docker group membership
- no credentials stored in Git

The observed deployment does not yet establish every intended property. Dedicated runtime-user separation, helper ownership, SSH-key restrictions and the actual application-level recovery result remain review items.

---

## Future Hardening

Possible additional hardening includes:

- disabling SSH agent forwarding
- disabling SSH port forwarding
- disabling X11 forwarding
- disabling PTY allocation for automation
- restricting the SSH key to predefined commands
- separating diagnostic and recovery permissions
- logging Sentinel recovery actions
