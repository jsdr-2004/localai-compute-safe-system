from __future__ import annotations

from localai_system.broker.policy import Classification, Policy

SHELL_CONTROL_OPERATORS = ("&&", "||", ";", "|", ">", "<", "`", "$(")


def normalize(command: str) -> str:
    return " ".join(command.strip().lower().split())


def classify_command(command: str, policy: Policy) -> Classification:
    normalized = normalize(command)
    if not normalized:
        return Classification(command, "unknown", "approval_required", "Empty commands are not executable.")
    if any(operator in normalized for operator in SHELL_CONTROL_OPERATORS):
        return Classification(command, "forbidden", "block", "Shell control operators and redirection are blocked.")
    for risk in ("forbidden", "critical", "high", "medium"):
        rule = policy.rules.get(risk, {})
        for pattern in rule.get("patterns", []):
            if normalize(pattern) in normalized:
                return Classification(command, risk, rule["decision"], f"Matched {risk} policy pattern: {pattern}")
    low = policy.rules.get("low", {})
    for prefix in low.get("prefixes", []):
        clean = normalize(prefix)
        if normalized == clean or normalized.startswith(clean + " "):
            return Classification(command, "low", low["decision"], f"Matched low-risk command prefix: {prefix}")
    return Classification(command, "unknown", "approval_required", "Command did not match a deterministic policy rule.")
