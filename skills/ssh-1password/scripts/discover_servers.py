#!/usr/bin/env python3
"""Discover SSH hosts from ~/.ssh/config."""

import re
from pathlib import Path

def parse_ssh_config():
    """Parse ~/.ssh/config for Host entries with connection details."""
    config_path = Path.home() / ".ssh" / "config"
    if not config_path.exists():
        return []

    hosts = []
    current = {}
    comment = None

    for line in config_path.read_text().splitlines():
        line = line.strip()

        # Capture comments as descriptions
        if line.startswith("#"):
            comment = line.lstrip("# ")
            continue

        # New Host block (skip wildcards)
        if match := re.match(r"^Host\s+(\S+)$", line, re.I):
            if current.get("alias") and current["alias"] != "*":
                hosts.append(current)
            alias = match.group(1)
            if alias != "*" and not alias.startswith("*"):
                current = {"alias": alias, "desc": comment}
            else:
                current = {}
            comment = None
            continue

        # Host properties
        if current.get("alias"):
            if match := re.match(r"^HostName\s+(.+)$", line, re.I):
                current["hostname"] = match.group(1)
            elif match := re.match(r"^User\s+(.+)$", line, re.I):
                current["user"] = match.group(1)
            elif match := re.match(r"^Port\s+(\d+)$", line, re.I):
                current["port"] = match.group(1)

    # Don't forget last entry
    if current.get("alias") and current["alias"] != "*":
        hosts.append(current)

    return hosts

def main():
    hosts = parse_ssh_config()

    if not hosts:
        print("No SSH hosts found in ~/.ssh/config")
        return

    print("Available SSH Hosts:\n")
    print(f"{'Alias':<25} {'User':<15} {'Host':<35} {'Port':<8} {'Description'}")
    print("-" * 100)

    for h in hosts:
        alias = h.get("alias", "")
        user = h.get("user", "-")
        hostname = h.get("hostname", "-")
        port = h.get("port", "22")
        desc = h.get("desc", "")[:30] if h.get("desc") else ""
        print(f"{alias:<25} {user:<15} {hostname:<35} {port:<8} {desc}")

    print(f"\nUsage: ssh <alias> \"command\"")

if __name__ == "__main__":
    main()
