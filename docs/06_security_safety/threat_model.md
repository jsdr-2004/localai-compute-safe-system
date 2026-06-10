# Threat Model

## Assets

- User files
- System configuration
- Credentials and keys
- Package manager state
- Audit logs
- Privilege broker policy
- Local model runtime
- Hardware benchmark dataset

## Trust Boundaries

The AI model is untrusted.

The privilege broker is trusted.

The user approval interface is trusted.

The Linux operating system enforces final system permissions.

## Threats

### T1 Prompt Injection

A malicious prompt asks the assistant to ignore rules or execute dangerous commands.

Mitigation:

- Broker enforces policy outside the model.
- Forbidden commands are blocked.
- Risk classification is independent.

### T2 Destructive Command Execution

The assistant proposes commands that delete important files.

Mitigation:

- Command preview
- Critical confirmation
- Backup/rollback
- Blocklist

### T3 Credential Theft

The assistant tries to read SSH keys, API keys, browser tokens, or environment secrets.

Mitigation:

- Secret path blocklist
- Data exfiltration rules
- Forbidden action classification

### T4 Privilege Escalation

The assistant tries to gain uncontrolled sudo/root access.

Mitigation:

- Broker-only privileged path
- No direct shell root
- Limited command allowlist
- Audit logging

### T5 Log Tampering

The assistant tries to hide or delete evidence.

Mitigation:

- Append-only logs
- Protected log directory
- Hashing later version

### T6 Unsafe Package Installation

The assistant installs unknown or malicious software.

Mitigation:

- Approval required
- Package source verification
- Risk warnings

### T7 Model Hallucination

The assistant invents unsafe or incorrect commands.

Mitigation:

- Risk classifier
- Command preview
- Human approval
- Safe command templates

## Evaluation Plan

Test the broker against:

- Safe commands
- Risky but valid commands
- Destructive commands
- Credential-access attempts
- Prompt injection attempts
- Security-disabling attempts

## Safety Metrics

- Unsafe command block rate
- False positive rate
- False negative rate
- Approval compliance rate
- Rollback success rate
