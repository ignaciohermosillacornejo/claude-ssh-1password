# SSH 1Password Plugin for Claude Code

A Claude Code skill for SSH access using 1Password SSH agent with ControlMaster connection multiplexing.

## What It Does

- **Discovers** available SSH hosts from your `~/.ssh/config`
- **Handles** 1Password biometric authentication transparently
- **Reuses** connections via ControlMaster (no repeated auth prompts)

## Prerequisites

1. **1Password** with SSH agent enabled
2. **SSH config** with ControlMaster setup:

```ssh-config
# ~/.ssh/config
Host *
  IdentityAgent "~/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock"
  ControlMaster auto
  ControlPath ~/.ssh/sockets/%C
  ControlPersist 30m
```

3. Create the sockets directory:
```bash
mkdir -p ~/.ssh/sockets && chmod 700 ~/.ssh/sockets
```

## Installation

```bash
# Clone the repo
git clone https://github.com/ignaciohermosillacornejo/claude-ssh-1password.git

# Use with Claude Code
claude --plugin-dir /path/to/claude-ssh-1password
```

Or add to your Claude Code settings for permanent use.

## Usage

Once installed, Claude will automatically use this skill when you ask to:
- SSH into servers
- Check remote logs
- Run commands on remote machines
- Discover available SSH hosts

Example prompts:
- "What servers do I have available?"
- "SSH into my-server and check disk usage"
- "Check the nginx logs on production"

## How It Works

1. **Discovery**: Parses `~/.ssh/config` for Host aliases with their connection details
2. **First connection**: Triggers 1Password biometric → creates ControlMaster socket
3. **Subsequent connections**: Reuse existing socket (instant, no prompt)
4. **Socket persistence**: 30 minutes after last use

## License

MIT
