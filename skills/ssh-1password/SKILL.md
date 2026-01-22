---
name: ssh-1password
description: Use when SSHing to servers, running remote commands, checking logs, or needing to discover available SSH hosts.
---

# SSH with 1Password Agent

## Overview

SSH using Host aliases from `~/.ssh/config`. Authentication via 1Password SSH agent with ControlMaster connection reuse.

## Quick Start

1. **Discover hosts:** `python3 ~/.claude/skills/ssh-1password/scripts/discover_servers.py`
2. **First connection:** Warn user about 1Password biometric prompt
3. **Run command:** `ssh <host-alias> "command"`

## ControlMaster

First SSH triggers 1Password biometric → creates socket at `~/.ssh/sockets/`. Subsequent connections reuse socket (no prompt). Persists 30 min.

## Common Patterns

| Task | Command |
|------|---------|
| Logs | `ssh host "tail -100 /var/log/app.log"` |
| Docker logs | `ssh host "docker logs --tail 100 container"` |
| Disk | `ssh host "df -h"` |
| Processes | `ssh host "ps aux \| grep pattern"` |
| Copy out | `scp host:/path/file ./local` |
| Copy in | `scp ./local host:/path/file` |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Hangs | User seeing 1Password prompt—wait |
| Permission denied | Check 1Password has key, `ssh-add -l` |
| Stale socket | `rm ~/.ssh/sockets/*` |
