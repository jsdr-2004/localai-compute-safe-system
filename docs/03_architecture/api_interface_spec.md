# API and Interface Specification

## Hardware Profiler Output

```json
{
  "hardware_profile_id": "HP-001",
  "cpu_model": "",
  "cpu_cores": 0,
  "cpu_threads": 0,
  "ram_gb": 0,
  "gpu_model": "",
  "vram_gb": 0,
  "storage_type": "",
  "os": "",
  "kernel": "",
  "runtime": "",
  "created_at": ""
}
```

## Benchmark Run Input

```json
{
  "model_name": "llama3.2:3b",
  "model_size": "3B",
  "quantization": "default",
  "context_length": 2048,
  "temperature": 0.7,
  "top_p": 0.95,
  "prompt_id": "P001"
}
```

## Benchmark Result Output

```json
{
  "run_id": "HP001-TOP8-30PROMPTS",
  "test_id": "T00001",
  "status": "success",
  "first_token_latency_sec": 0.8,
  "total_response_time_sec": 5.2,
  "tokens_per_sec_estimate": 22.4,
  "peak_ram_gb": 8.1,
  "peak_cpu_usage_percent": 91.2,
  "quality_score": 4,
  "feasibility_status": "smooth"
}
```

## Command Proposal

```json
{
  "request_id": "REQ-001",
  "user_request": "Install Docker and verify it works",
  "proposed_commands": [
    "sudo apt update",
    "sudo apt install docker.io",
    "docker --version"
  ],
  "explanation": "Updates package lists, installs Docker, and verifies installation."
}
```

## Risk Classification Output

```json
{
  "command": "sudo apt install docker.io",
  "risk_level": "medium",
  "requires_approval": true,
  "requires_backup": false,
  "decision": "approval_required",
  "reason": "Package installation modifies the system."
}
```

## Audit Log Record

```json
{
  "event_id": "EVT-001",
  "timestamp": "",
  "run_id": "",
  "session_id": "",
  "user_request": "",
  "command": "",
  "risk_level": "",
  "approval_status": "",
  "execution_status": "",
  "stdout_path": "",
  "stderr_path": "",
  "rollback_id": "",
  "reason": "",
  "broker_policy_version": "v0.2"
}
```
