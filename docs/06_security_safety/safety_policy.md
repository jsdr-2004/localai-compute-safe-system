# Safety Policy

## Core Principle

The AI assistant must never receive uncontrolled root access.

## Risk Levels

### Low Risk

Read-only operations.

Examples:

- `ls`
- `pwd`
- `df -h`
- `free -h`
- `uptime`
- `systemctl status`

Allowed with logging.

### Medium Risk

Operations that modify user-level or package state but are commonly reversible.

Examples:

- Package installation
- Creating folders
- Updating package lists
- Starting user services

Requires approval.

### High Risk

Operations that modify system configuration or important files.

Examples:

- Editing `/etc` files
- Changing service files
- Modifying firewall rules
- Changing permissions

Requires approval and backup.

### Critical Risk

Operations with destructive or security-sensitive impact.

Examples:

- Deleting files
- Changing users
- Modifying sudoers
- Stopping security services
- Disk formatting

Requires explicit confirmation and rollback plan when possible.

### Forbidden

Blocked completely.

Examples:

- Credential theft
- Exfiltration of secrets
- Disabling security protections
- Wiping disks
- Malware persistence
- Hidden surveillance
- Destructive commands without user control
- Bypassing authentication
- Tampering with logs

## Approval Requirements

The assistant must show:

1. The command
2. The reason
3. The risk level
4. The expected effect
5. The rollback option if available

## Logging Requirements

Every action must record:

- Timestamp
- User request
- Proposed command
- Risk level
- Approval decision
- Execution result
- Output location
- Rollback metadata

## Emergency Stop

The user must be able to disable the assistant and broker at any time.
