from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path
from typing import Any

from localai_system.common.io import utc_now, write_json


class RollbackManager:
    def __init__(self, backup_dir: str | Path = "data/backups") -> None:
        self.backup_dir = Path(backup_dir)

    def backup_file(self, source: str | Path) -> dict[str, Any]:
        source_path = Path(source).expanduser().resolve()
        if not source_path.is_file():
            raise FileNotFoundError(f"Only existing files can be backed up: {source_path}")
        rollback_id = f"RB-{uuid.uuid4().hex[:12].upper()}"
        folder = self.backup_dir / rollback_id
        folder.mkdir(parents=True, exist_ok=False)
        backup_path = folder / source_path.name
        shutil.copy2(source_path, backup_path)
        metadata = {"rollback_id": rollback_id, "created_at": utc_now(), "original_path": str(source_path),
                    "backup_path": str(backup_path), "status": "available"}
        write_json(folder / "metadata.json", metadata)
        return metadata

    def list(self) -> list[dict[str, Any]]:
        if not self.backup_dir.exists():
            return []
        records = []
        for path in sorted(self.backup_dir.glob("RB-*/metadata.json")):
            records.append(json.loads(path.read_text(encoding="utf-8")))
        return records

    def restore(self, rollback_id: str) -> dict[str, Any]:
        metadata_path = self.backup_dir / rollback_id / "metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Rollback not found: {rollback_id}")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        shutil.copy2(metadata["backup_path"], metadata["original_path"])
        metadata["status"] = "restored"
        metadata["restored_at"] = utc_now()
        write_json(metadata_path, metadata)
        return metadata


def cli(args: Any) -> int:
    manager = RollbackManager(args.backup_dir)
    if args.action == "list":
        for item in manager.list():
            print(f"{item['rollback_id']} {item['status']} {item['original_path']}")
        return 0
    try:
        restored = manager.restore(args.rollback_id)
    except FileNotFoundError as exc:
        print(exc)
        return 1
    print(f"Restored {restored['original_path']} from {restored['rollback_id']}")
    return 0
