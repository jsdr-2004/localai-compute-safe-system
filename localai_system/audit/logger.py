from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from localai_system.common.io import ensure_parent, utc_now


class AuditLogger:
    def __init__(self, path: str | Path = "data/audit/audit.jsonl") -> None:
        self.path = Path(path)

    def write(self, **event: Any) -> dict[str, Any]:
        record = {
            "event_id": event.pop("event_id", f"EVT-{uuid.uuid4().hex[:12].upper()}"),
            "timestamp": event.pop("timestamp", utc_now()),
            "user_request": "", "proposed_command": "", "risk_level": "", "decision": "",
            "approval_status": "", "execution_status": "", "stdout_path": "", "stderr_path": "",
            "rollback_id": "", "reason": "",
        }
        record.update(event)
        ensure_parent(self.path)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")
        return record

    def list(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open(encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]

    def show(self, event_id: str) -> dict[str, Any] | None:
        return next((event for event in self.list() if event["event_id"] == event_id), None)


def cli(args: Any) -> int:
    logger = AuditLogger(args.log)
    if args.action == "list":
        for event in logger.list():
            print(f"{event['event_id']} {event['timestamp']} {event['risk_level']} {event['execution_status']} {event['proposed_command']}")
        return 0
    event = logger.show(args.event_id)
    if not event:
        print(f"Audit event not found: {args.event_id}")
        return 1
    print(json.dumps(event, indent=2))
    return 0
