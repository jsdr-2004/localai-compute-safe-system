from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any

import psutil

from localai_system.common.io import utc_now, write_json


def _command_output(command: list[str], timeout: int = 5) -> str | None:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        return result.stdout.strip() or result.stderr.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def _cpu_model() -> str:
    if platform.system() == "Darwin":
        return _command_output(["sysctl", "-n", "machdep.cpu.brand_string"]) or platform.processor()
    if Path("/proc/cpuinfo").exists():
        for line in Path("/proc/cpuinfo").read_text(errors="ignore").splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[-1].strip()
    return platform.processor() or "unknown"


def _gpu_info() -> list[dict[str, Any]]:
    if shutil.which("nvidia-smi"):
        output = _command_output([
            "nvidia-smi",
            "--query-gpu=name,memory.total,driver_version",
            "--format=csv,noheader,nounits",
        ])
        if output:
            return [
                {"model": parts[0].strip(), "vram_mb": float(parts[1]), "driver": parts[2].strip()}
                for line in output.splitlines()
                if len(parts := line.split(",")) >= 3
            ]
    if platform.system() == "Darwin":
        output = _command_output(["system_profiler", "SPDisplaysDataType"], timeout=15)
        models = [line.split(":", 1)[1].strip() for line in (output or "").splitlines() if "Chipset Model:" in line]
        return [{"model": model, "vram_mb": None, "driver": None} for model in models]
    return []


def collect_profile(profile_id: str = "HP-001") -> dict[str, Any]:
    disks = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (OSError, PermissionError):
            continue
        disks.append({
            "device": part.device,
            "mountpoint": part.mountpoint,
            "filesystem": part.fstype,
            "total_gb": round(usage.total / 1024**3, 3),
            "free_gb": round(usage.free / 1024**3, 3),
        })
    gpus = _gpu_info()
    return {
        "hardware_profile_id": profile_id,
        "created_at": utc_now(),
        "os": platform.platform(),
        "kernel": platform.release(),
        "python_version": platform.python_version(),
        "cpu_model": _cpu_model(),
        "cpu_cores": psutil.cpu_count(logical=False) or 0,
        "cpu_threads": psutil.cpu_count(logical=True) or 0,
        "ram_gb": round(psutil.virtual_memory().total / 1024**3, 3),
        "disks": disks,
        "gpus": gpus,
        "gpu_model": ", ".join(str(gpu["model"]) for gpu in gpus),
        "vram_gb": round(sum(float(gpu["vram_mb"] or 0) for gpu in gpus) / 1024, 3),
        "apple_silicon": platform.system() == "Darwin" and platform.machine() == "arm64",
        "machine": platform.machine(),
        "ollama_version": _command_output(["ollama", "--version"]) if shutil.which("ollama") else None,
        "llama_cpp_path": shutil.which("llama-cli") or shutil.which("llama-server") or shutil.which("main"),
        "hostname": platform.node(),
    }


def cli(args: Any) -> int:
    profile = collect_profile()
    if args.action == "profile":
        profile_id = Path(args.output).stem
        profile = collect_profile(profile_id)
        target = write_json(args.output, profile)
        print(f"Hardware profile saved to {target}")
    else:
        print(json.dumps(profile, indent=2))
    return 0
