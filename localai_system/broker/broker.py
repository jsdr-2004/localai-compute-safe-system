from __future__ import annotations

import json
import shlex
import subprocess
import uuid
from pathlib import Path
from typing import Any, Callable

from localai_system.audit.logger import AuditLogger
from localai_system.broker.classifier import classify_command
from localai_system.broker.policy import Classification, Policy
from localai_system.rollback.manager import RollbackManager


class PrivilegeBroker:
    def __init__(self, policy: Policy, audit: AuditLogger | None = None, rollback: RollbackManager | None = None,
                 execution_enabled: bool = False) -> None:
        self.policy = policy
        self.audit = audit or AuditLogger()
        self.rollback = rollback or RollbackManager()
        self.execution_enabled = execution_enabled

    def classify(self, command: str) -> Classification:
        return classify_command(command, self.policy)

    def handle(self, user_request: str, command: str, approved: bool = False, backup_path: str | None = None,
               timeout: int = 60) -> dict[str, Any]:
        result = self.classify(command)
        rollback_id = ""
        approval_status = "not_required" if not result.requires_approval else ("approved" if approved else "not_approved")
        execution_status = "blocked" if result.decision == "block" else "not_executed"
        stdout = ""
        stderr = ""
        event_id = f"EVT-{uuid.uuid4().hex[:12].upper()}"
        if result.decision != "block" and (not result.requires_approval or approved):
            if result.requires_backup:
                if not backup_path:
                    execution_status = "blocked_backup_required"
                else:
                    try:
                        rollback_id = self.rollback.backup_file(backup_path)["rollback_id"]
                    except (OSError, ValueError) as exc:
                        execution_status = "blocked_backup_failed"
                        stderr = str(exc)
            if execution_status not in {"blocked_backup_required", "blocked_backup_failed"}:
                if not self.execution_enabled:
                    execution_status = "execution_disabled"
                else:
                    try:
                        completed = subprocess.run(shlex.split(command), capture_output=True, text=True, timeout=timeout,
                                                   shell=False, check=False)
                        stdout, stderr = completed.stdout, completed.stderr
                        execution_status = "success" if completed.returncode == 0 else "failed"
                    except (OSError, subprocess.SubprocessError, ValueError) as exc:
                        execution_status = "failed"
                        stderr = str(exc)
        stdout_path = ""
        stderr_path = ""
        if stdout or stderr:
            output_dir = self.audit.path.parent / "outputs"
            output_dir.mkdir(parents=True, exist_ok=True)
            if stdout:
                stdout_file = output_dir / f"{event_id}.stdout.txt"
                stdout_file.write_text(stdout, encoding="utf-8")
                stdout_path = str(stdout_file)
            if stderr:
                stderr_file = output_dir / f"{event_id}.stderr.txt"
                stderr_file.write_text(stderr, encoding="utf-8")
                stderr_path = str(stderr_file)
        event = self.audit.write(event_id=event_id, user_request=user_request, proposed_command=command, risk_level=result.risk_level,
                                 decision=result.decision, approval_status=approval_status,
                                 execution_status=execution_status, stdout_path=stdout_path, stderr_path=stderr_path,
                                 rollback_id=rollback_id, reason=result.reason)
        return {"classification": result.as_dict(), "event": event, "stdout": stdout, "stderr": stderr}


def cli(args: Any) -> int:
    policy = Policy.from_yaml(args.policy)
    result = classify_command(args.command, policy)
    print(json.dumps(result.as_dict(), indent=2))
    return 0
