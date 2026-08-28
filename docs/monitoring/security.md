# Sentinel Security

## Purpose

Sentinel requires access to the main HomeLAB server for diagnostics and later for controlled recovery actions.

The goal is to provide enough access for monitoring without giving the Raspberry Pi unrestricted root privileges.

---

## Dedicated Account

The HomeLAB server uses a dedicated user:

```text
sentinel
```

This account is used only by the Sentinel monitoring node.

It is separate from the normal administrative user account.

---

## SSH Authentication

Sentinel connects using a dedicated ED25519 SSH key.

The key belongs to the Raspberry Pi Sentinel node and is used only for HomeLAB monitoring.

Password-based automation is not used.

---

## Restricted Privileges

The `sentinel` user has restricted sudo permissions for selected diagnostic commands.

Current allowed operations include:

```text
docker ps
docker inspect
docker logs
df
free
uptime
```

The account does not currently have permission to restart containers or perform general administrative actions.

---

## Recovery Permissions

Future recovery functionality should not grant Sentinel unrestricted Docker or root access.

Recovery actions should be exposed through narrowly defined, root-owned helper scripts.

This allows Sentinel to perform specific recovery tasks without receiving broad container-management privileges.

---

## Design Principles

The Sentinel security model follows these principles:

- dedicated service account
- dedicated SSH key
- least privilege
- read-only diagnostics by default
- explicit recovery permissions
- no unrestricted root access
- no Docker group membership
- no credentials stored in Git

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
