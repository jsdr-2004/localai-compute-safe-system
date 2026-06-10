from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from localai_system.common.io import load_yaml


@dataclass(frozen=True)
class Classification:
    command: str
    risk_level: str
    decision: str
    reason: str

    @property
    def requires_approval(self) -> bool:
        return self.decision in {"approval_required", "backup_required", "explicit_confirmation_required"}

    @property
    def requires_backup(self) -> bool:
        return self.decision == "backup_required"

    def as_dict(self) -> dict[str, Any]:
        return {
            "command": self.command, "risk_level": self.risk_level, "decision": self.decision,
            "requires_approval": self.requires_approval, "requires_backup": self.requires_backup, "reason": self.reason,
        }


class Policy:
    def __init__(self, rules: dict[str, Any]) -> None:
        self.rules = rules
        self.version = str(rules.get("version", "v0.2"))

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Policy":
        return cls(load_yaml(path))
