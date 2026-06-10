import json
from pathlib import Path

from localai_system.assistant.planner import route_request
from localai_system.audit.logger import AuditLogger
from localai_system.benchmark.config import load_config, validate_config
from localai_system.broker.broker import PrivilegeBroker
from localai_system.broker.classifier import classify_command
from localai_system.broker.policy import Policy
from localai_system.hardware.profiler import collect_profile
from localai_system.recommender.engine import final_score
from localai_system.rollback.manager import RollbackManager


def policy() -> Policy:
    return Policy.from_yaml("configs/policy_rules.yaml")


def test_hardware_profiler_does_not_crash():
    profile = collect_profile("HP-TEST")
    assert profile["hardware_profile_id"] == "HP-TEST"
    assert profile["ram_gb"] > 0


def test_benchmark_config_validation():
    assert validate_config(load_config("configs/benchmark_ollama.yaml")) == []


def test_scoring_formula():
    assert final_score(1.0, 1.0, 1.0, 1.0) == 1.0
    assert round(final_score(0.8, 0.6, 0.5, 1.0), 3) == 0.73
    assert final_score(None, 1.0, 1.0, 1.0) == 1.0


def test_risk_classifier():
    assert classify_command("df -h", policy()).risk_level == "low"
    assert classify_command("sudo apt install docker.io", policy()).decision == "approval_required"
    assert classify_command("sudo nano /etc/hosts", policy()).decision == "backup_required"


def test_forbidden_command_is_blocked_even_when_approved(tmp_path):
    broker = PrivilegeBroker(policy(), audit=AuditLogger(tmp_path / "audit.jsonl"), execution_enabled=True)
    result = broker.handle("delete all", "rm -rf /", approved=True)
    assert result["classification"]["decision"] == "block"
    assert result["event"]["execution_status"] == "blocked"


def test_audit_log_writing(tmp_path):
    logger = AuditLogger(tmp_path / "audit.jsonl")
    record = logger.write(user_request="check disk", proposed_command="df -h")
    assert logger.show(record["event_id"])["proposed_command"] == "df -h"


def test_rollback_metadata_creation_and_restore(tmp_path):
    source = tmp_path / "config.txt"
    source.write_text("before")
    manager = RollbackManager(tmp_path / "backups")
    record = manager.backup_file(source)
    source.write_text("after")
    manager.restore(record["rollback_id"])
    assert source.read_text() == "before"


def test_assistant_demo_routing():
    assert route_request("check disk usage").commands == ["df -h"]
    assert route_request("delete all files").commands == ["rm -rf /"]
