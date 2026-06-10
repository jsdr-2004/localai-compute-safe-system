from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from localai_system.common.io import ensure_parent, load_json

WEIGHTS = {"quality_score": 0.35, "speed_score": 0.25, "memory_efficiency_score": 0.20, "feasibility_score": 0.20}


def _number(value: Any) -> float | None:
    try:
        return float(value) if value not in ("", None) else None
    except (TypeError, ValueError):
        return None


def feasibility(status: str, total_seconds: float | None, smooth_threshold: float = 30.0) -> tuple[str, float]:
    if status != "success":
        return "failed", 0.0
    if total_seconds is not None and total_seconds <= smooth_threshold:
        return "smooth", 1.0
    return "slow", 0.5


def final_score(quality: float | None, speed: float, memory: float, feasible: float) -> float:
    values = {"quality_score": quality, "speed_score": speed, "memory_efficiency_score": memory,
              "feasibility_score": feasible}
    available = [(WEIGHTS[key], value) for key, value in values.items() if value is not None]
    return sum(weight * value for weight, value in available) / sum(weight for weight, _ in available)


def rank(results_path: str | Path, hardware_path: str | Path) -> list[dict[str, Any]]:
    hardware = load_json(hardware_path)
    total_ram = float(hardware["ram_gb"])
    with Path(results_path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    max_speed = max((_number(row.get("tokens_per_sec_estimate")) or 0 for row in rows), default=1) or 1
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = (row.get("hardware_profile_id", hardware["hardware_profile_id"]), row.get("prompt_category", "unknown"),
               row.get("model_name", ""), row.get("model_size", ""), row.get("quantization", ""),
               row.get("context_length", ""), row.get("temperature", ""), row.get("top_p", ""))
        groups[key].append(row)
    ranked = []
    for key, group in groups.items():
        speed = mean((_number(row.get("tokens_per_sec_estimate")) or 0) / max_speed for row in group)
        ram = mean(_number(row.get("peak_ram_gb")) or total_ram for row in group)
        memory = max(0.0, min(1.0, 1 - ram / total_ram))
        qualities = [_number(row.get("quality_score")) for row in group]
        quality_values = [value / 5 for value in qualities if value is not None]
        quality = mean(quality_values) if quality_values else None
        feasibility_values = [feasibility(row.get("status", ""), _number(row.get("total_response_time_sec"))) for row in group]
        feasible_score = mean(item[1] for item in feasibility_values)
        label = "failed" if feasible_score == 0 else ("smooth" if feasible_score >= 0.75 else "slow")
        ranked.append({
            "hardware_profile_id": key[0], "task_category": key[1], "model_name": key[2], "model_size": key[3],
            "quantization": key[4], "context_length": key[5], "temperature": key[6], "top_p": key[7],
            "quality_score_normalized": "" if quality is None else round(quality, 4), "speed_score": round(speed, 4),
            "memory_efficiency_score": round(memory, 4), "feasibility_status": label,
            "feasibility_score": round(feasible_score, 4), "final_score": round(final_score(quality, speed, memory, feasible_score), 4),
        })
    ranked.sort(key=lambda row: (row["task_category"], -float(row["final_score"])))
    counts: dict[str, int] = defaultdict(int)
    for row in ranked:
        counts[row["task_category"]] += 1
        row["rank"] = counts[row["task_category"]]
    return ranked


def export(rows: list[dict[str, Any]], output: str | Path) -> None:
    target = ensure_parent(output)
    csv_target = target.with_suffix(".csv")
    with csv_target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    lines = ["# Model Recommendations", "", "Scores are normalized per hardware profile. Blank quality scores are omitted and remaining weights are normalized.", ""]
    current = None
    for row in rows:
        if row["task_category"] != current:
            current = row["task_category"]
            lines.extend([f"## {current}", "", "| Rank | Model | Configuration | Feasibility | Score |", "|---:|---|---|---|---:|"])
        lines.append(f"| {row['rank']} | {row['model_name']} | ctx={row['context_length']}, temp={row['temperature']}, top_p={row['top_p']} | {row['feasibility_status']} | {row['final_score']} |")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cli(args: Any) -> int:
    rows = rank(args.results, args.hardware)
    export(rows, args.output)
    print(f"Recommendation report saved to {args.output}")
    return 0
