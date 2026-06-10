"""
Starter pseudocode for AI Privilege Broker.
Do not use this as production security code.
"""

FORBIDDEN_PATTERNS = [
    "rm -rf /",
    "mkfs",
    "dd if=",
    "cat ~/.ssh/id_rsa",
    "cat ~/.aws/credentials",
    "systemctl disable ufw",
    "iptables -F",
    "history -c"
]

HIGH_RISK_PATTERNS = [
    "/etc/",
    "chmod",
    "chown",
    "systemctl restart"
]

MEDIUM_RISK_PATTERNS = [
    "sudo apt install",
    "sudo apt update",
    "mkdir",
    "touch"
]

LOW_RISK_PATTERNS = [
    "df -h",
    "free -h",
    "uptime",
    "pwd",
    "ls"
]

def classify_command(command: str):
    command_lower = command.lower()

    for pattern in FORBIDDEN_PATTERNS:
        if pattern.lower() in command_lower:
            return {
                "risk_level": "forbidden",
                "decision": "block",
                "reason": f"Command matched forbidden pattern: {pattern}"
            }

    for pattern in HIGH_RISK_PATTERNS:
        if pattern.lower() in command_lower:
            return {
                "risk_level": "high",
                "decision": "backup_required",
                "reason": f"Command matched high-risk pattern: {pattern}"
            }

    for pattern in MEDIUM_RISK_PATTERNS:
        if pattern.lower() in command_lower:
            return {
                "risk_level": "medium",
                "decision": "approval_required",
                "reason": f"Command matched medium-risk pattern: {pattern}"
            }

    for pattern in LOW_RISK_PATTERNS:
        if command_lower.strip().startswith(pattern.lower()):
            return {
                "risk_level": "low",
                "decision": "allow",
                "reason": f"Command matched low-risk pattern: {pattern}"
            }

    return {
        "risk_level": "unknown",
        "decision": "approval_required",
        "reason": "Command did not match known policy rules."
    }

if __name__ == "__main__":
    examples = [
        "df -h",
        "sudo apt install docker.io",
        "sudo nano /etc/hosts",
        "rm -rf /",
        "cat ~/.ssh/id_rsa"
    ]

    for command in examples:
        print(command, "=>", classify_command(command))
