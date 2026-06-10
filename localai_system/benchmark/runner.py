from __future__ import annotations

import csv
import hashlib
import itertools
import json
import os
import shutil
import subprocess
import threading
import time
from pathlib import Path
from typing import Any, Iterator

import psutil
import requests

from localai_system.benchmark.config import load_config, validate_config
from localai_system.common.io import ensure_parent, load_json, utc_now

FIELDS = [
    "test_id", "date", "hardware_profile_id", "runtime", "model_name", "model_size",
    "quantization", "context_length", "temperature", "top_p", "threads", "prompt_id",
    "prompt_category", "repeat_id", "status", "first_token_latency_sec",
    "tokens_per_sec_estimate", "total_response_time_sec", "peak_ram_gb", "peak_vram_gb",
    "peak_cpu_usage_percent", "peak_gpu_usage_percent", "quality_score", "safety_score",
    "feasibility_status", "final_score", "raw_output_path", "error",
]


def build_matrix(config: dict[str, Any]) -> Iterator[dict[str, Any]]:
    prompts = load_json(config["_prompts_path"])
    settings = config["settings"]
    threads = settings.get("threads", [None])
    for model, context, temperature, top_p, thread_count, prompt, repeat in itertools.product(
        config["models"], settings["context_lengths"], settings["temperatures"], settings["top_p"],
        threads, prompts, range(1, int(config["repeat_each_test"]) + 1),
    ):
        identity = json.dumps([model["name"], context, temperature, top_p, thread_count, prompt["prompt_id"], repeat])
        yield {
            "test_id": "T-" + hashlib.sha256(identity.encode()).hexdigest()[:12].upper(),
            "model": model, "context_length": context, "temperature": temperature, "top_p": top_p,
            "threads": thread_count, "prompt": prompt, "repeat_id": repeat,
        }


class UsageSampler:
    def __init__(self) -> None:
        self.stop = threading.Event()
        self.peak_ram_gb = 0.0
        self.peak_cpu = 0.0
        self.peak_vram_gb = 0.0
        self.peak_gpu = 0.0
        self.thread = threading.Thread(target=self._sample, daemon=True)

    def _sample(self) -> None:
        while not self.stop.wait(0.1):
            self.peak_ram_gb = max(self.peak_ram_gb, psutil.virtual_memory().used / 1024**3)
            self.peak_cpu = max(self.peak_cpu, psutil.cpu_percent(interval=None))
            if shutil.which("nvidia-smi"):
                try:
                    output = subprocess.run(
                        ["nvidia-smi", "--query-gpu=memory.used,utilization.gpu", "--format=csv,noheader,nounits"],
                        capture_output=True, text=True, timeout=2, check=False,
                    ).stdout
                    for line in output.splitlines():
                        memory, gpu = (float(item.strip()) for item in line.split(",")[:2])
                        self.peak_vram_gb = max(self.peak_vram_gb, memory / 1024)
                        self.peak_gpu = max(self.peak_gpu, gpu)
                except (OSError, ValueError, subprocess.SubprocessError):
                    pass

    def __enter__(self) -> "UsageSampler":
        self.thread.start()
        return self

    def __exit__(self, *_: Any) -> None:
        self.stop.set()
        self.thread.join(timeout=1)


def run_ollama(test: dict[str, Any], url: str, timeout: float) -> dict[str, Any]:
    options = {"num_ctx": test["context_length"], "temperature": test["temperature"], "top_p": test["top_p"]}
    if test["threads"]:
        options["num_thread"] = test["threads"]
    payload = {"model": test["model"]["name"], "prompt": test["prompt"]["prompt"], "stream": True, "options": options}
    start = time.perf_counter()
    first = None
    output = []
    eval_count = 0
    with UsageSampler() as usage:
        try:
            with requests.post(url, json=payload, stream=True, timeout=(10, timeout)) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    data = json.loads(line)
                    chunk = data.get("response", "")
                    if chunk and first is None:
                        first = time.perf_counter()
                    output.append(chunk)
                    eval_count = data.get("eval_count", eval_count)
                    if data.get("done"):
                        break
            end = time.perf_counter()
            duration = end - start
            estimate = eval_count or max(1, len("".join(output).split()))
            return {"status": "success", "first": None if first is None else first - start, "total": duration,
                    "tokens_per_sec": estimate / duration if duration else 0, "output": "".join(output), "error": "",
                    "peak_ram_gb": usage.peak_ram_gb, "peak_cpu": usage.peak_cpu,
                    "peak_vram_gb": usage.peak_vram_gb, "peak_gpu": usage.peak_gpu}
        except Exception as exc:
            return {"status": "failed", "first": None, "total": time.perf_counter() - start, "tokens_per_sec": None,
                    "output": "".join(output), "error": str(exc), "peak_ram_gb": usage.peak_ram_gb,
                    "peak_cpu": usage.peak_cpu, "peak_vram_gb": usage.peak_vram_gb, "peak_gpu": usage.peak_gpu}


def _resolve(config: dict[str, Any], value: str, default: str) -> Path:
    path = Path(value or default)
    return path if path.is_absolute() else Path.cwd() / path


def _completed(csv_path: Path) -> set[str]:
    if not csv_path.exists():
        return set()
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return {row["test_id"] for row in csv.DictReader(handle) if row.get("test_id")}


def run(config: dict[str, Any]) -> int:
    csv_path = _resolve(config, config["output_csv"], "data/results/benchmark_results.csv")
    jsonl_path = _resolve(config, config.get("output_jsonl", ""), "data/results/benchmark_results.jsonl")
    raw_dir = _resolve(config, config.get("raw_output_dir", ""), "data/raw_outputs")
    raw_dir.mkdir(parents=True, exist_ok=True)
    ensure_parent(csv_path)
    ensure_parent(jsonl_path)
    completed = _completed(csv_path)
    write_header = not csv_path.exists() or csv_path.stat().st_size == 0
    with csv_path.open("a", newline="", encoding="utf-8") as csv_handle, jsonl_path.open("a", encoding="utf-8") as jsonl:
        writer = csv.DictWriter(csv_handle, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        for test in build_matrix(config):
            if test["test_id"] in completed:
                print(f"Skipping completed {test['test_id']}")
                continue
            print(f"Running {test['test_id']} {test['model']['name']} {test['prompt']['prompt_id']}")
            result = run_ollama(test, config.get("ollama_url", os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")),
                                float(config.get("timeout_seconds", 300)))
            raw_path = raw_dir / f"{test['test_id']}.txt"
            raw_path.write_text(result["output"], encoding="utf-8")
            row = {
                "test_id": test["test_id"], "date": utc_now(), "hardware_profile_id": config["hardware_profile_id"],
                "runtime": "ollama", "model_name": test["model"]["name"], "model_size": test["model"]["size"],
                "quantization": test["model"]["quantization"], "context_length": test["context_length"],
                "temperature": test["temperature"], "top_p": test["top_p"], "threads": test["threads"] or "",
                "prompt_id": test["prompt"]["prompt_id"], "prompt_category": test["prompt"]["category"],
                "repeat_id": test["repeat_id"], "status": result["status"],
                "first_token_latency_sec": _round(result["first"]), "tokens_per_sec_estimate": _round(result["tokens_per_sec"]),
                "total_response_time_sec": _round(result["total"]), "peak_ram_gb": _round(result["peak_ram_gb"]),
                "peak_vram_gb": _round(result["peak_vram_gb"]) if result["peak_vram_gb"] else "",
                "peak_cpu_usage_percent": _round(result["peak_cpu"]),
                "peak_gpu_usage_percent": _round(result["peak_gpu"]) if result["peak_gpu"] else "",
                "quality_score": "", "safety_score": "", "feasibility_status": "",
                "final_score": "", "raw_output_path": str(raw_path), "error": result["error"],
            }
            writer.writerow(row)
            csv_handle.flush()
            jsonl.write(json.dumps(row) + "\n")
            jsonl.flush()
    print(f"Benchmark results saved to {csv_path}")
    return 0


def _round(value: float | None) -> float | str:
    return "" if value is None else round(value, 4)


def cli(args: Any) -> int:
    config = load_config(args.config)
    errors = validate_config(config)
    if errors:
        print("Invalid benchmark configuration:")
        for error in errors:
            print(f"- {error}")
        return 2
    matrix = list(build_matrix(config))
    if args.action == "validate":
        print(f"Valid configuration with {len(matrix)} tests")
        return 0
    if args.action == "dry-run":
        for test in matrix:
            print(f"{test['test_id']} model={test['model']['name']} ctx={test['context_length']} "
                  f"temp={test['temperature']} top_p={test['top_p']} prompt={test['prompt']['prompt_id']} "
                  f"repeat={test['repeat_id']}")
        print(f"Total tests: {len(matrix)}")
        return 0
    return run(config)
