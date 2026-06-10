from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from localai_system.common.io import ensure_parent, load_json

WEIGHTS = {"quality_score": 0.35, "speed_score": 0.25, "memory_efficiency_score": 0.20, "feasibility_score": 0.20}
GROUP_FIELDS = ("model_name", "model_size", "context_length", "temperature", "top_p")


def number(value: Any) -> float | None:
    try:
        return float(value) if value not in ("", None) else None
    except (TypeError, ValueError):
        return None


def feasibility(status: str, total_seconds: float | None, smooth_threshold: float = 30.0) -> tuple[str, float]:
    if status != "success":
        return "failed", 0.0
    return ("smooth", 1.0) if total_seconds is not None and total_seconds <= smooth_threshold else ("slow", 0.5)


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
    max_speed = max((number(row.get("tokens_per_sec_estimate")) or 0 for row in rows), default=1) or 1
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[tuple(row.get(field, "") for field in GROUP_FIELDS)].append(row)
    ranked: list[dict[str, Any]] = []
    for key, group in groups.items():
        successful = [row for row in group if row.get("status") == "success"]
        avg_speed = mean(number(row.get("tokens_per_sec_estimate")) or 0 for row in group)
        avg_latency = mean(number(row.get("total_response_time_sec")) or 0 for row in group)
        avg_ram = mean(number(row.get("peak_ram_gb")) or total_ram for row in group)
        speed = avg_speed / max_speed
        memory = max(0.0, min(1.0, 1 - avg_ram / total_ram))
        quality_values = [value / 5 for row in group if (value := number(row.get("quality_score"))) is not None]
        quality = mean(quality_values) if quality_values else None
        feasible_values = [feasibility(row.get("status", ""), number(row.get("total_response_time_sec")))[1] for row in group]
        feasible_score = mean(feasible_values)
        label = "failed" if feasible_score == 0 else ("smooth" if feasible_score >= 0.75 else "slow")
        score = final_score(quality, speed, memory, feasible_score)
        ranked.append({
            **dict(zip(GROUP_FIELDS, key)),
            "average_tokens_per_sec": round(avg_speed, 4),
            "average_latency_sec": round(avg_latency, 4),
            "average_peak_ram_gb": round(avg_ram, 4),
            "success_rate": round(len(successful) / len(group), 4),
            "speed_score": round(speed, 4),
            "memory_efficiency_score": round(memory, 4),
            "feasibility_score": round(feasible_score, 4),
            "quality_score_normalized": "" if quality is None else round(quality, 4),
            "partial_score_used": quality is None,
            "feasibility_status": label,
            "final_score": round(score, 4),
            "reason_for_selection": "Balanced partial score from speed, memory efficiency, and feasibility"
                                    if quality is None else "Balanced full score including human quality",
        })
    speed_order = sorted(ranked, key=lambda row: -float(row["speed_score"]))
    memory_order = sorted(ranked, key=lambda row: -float(row["memory_efficiency_score"]))
    ranked.sort(key=lambda row: -float(row["final_score"]))
    speed_rank = {id(row): index for index, row in enumerate(speed_order, 1)}
    memory_rank = {id(row): index for index, row in enumerate(memory_order, 1)}
    for index, row in enumerate(ranked, 1):
        row["speed_rank"] = speed_rank[id(row)]
        row["memory_rank"] = memory_rank[id(row)]
        row["final_rank"] = index
    return ranked


def export(rows: list[dict[str, Any]], output: str | Path) -> None:
    target = ensure_parent(output)
    csv_target = target.with_suffix(".csv")
    with csv_target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    lines = [
        "# Model Recommendations", "",
        "Scores are normalized for the supplied hardware profile. `partial_score_used=true` means human quality scores were blank and the score uses speed, memory efficiency, and feasibility only.",
        "", "## Top 5 Configurations", "",
        "| Rank | Model | Context | Temperature | Top-p | Tokens/sec | Latency | Peak RAM | Feasibility | Partial | Score |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---|---|---:|",
    ]
    for row in rows[:5]:
        lines.append(f"| {row['final_rank']} | {row['model_name']} | {row['context_length']} | {row['temperature']} | "
                     f"{row['top_p']} | {row['average_tokens_per_sec']} | {row['average_latency_sec']} | "
                     f"{row['average_peak_ram_gb']} | {row['feasibility_status']} | {row['partial_score_used']} | {row['final_score']} |")
    lines.extend(["", "## All Configurations", "", "| Rank | Model | Configuration | Speed Rank | Memory Rank | Feasibility | Partial | Score |",
                  "|---:|---|---|---:|---:|---|---|---:|"])
    for row in rows:
        lines.append(f"| {row['final_rank']} | {row['model_name']} | ctx={row['context_length']}, temp={row['temperature']}, top_p={row['top_p']} | "
                     f"{row['speed_rank']} | {row['memory_rank']} | {row['feasibility_status']} | {row['partial_score_used']} | {row['final_score']} |")
    lines.extend(["", "## Limitations", "", "- Human quality scores are not yet populated for HP-001; all current recommendations are partial scores.",
                  "- Rankings are specific to the supplied hardware profile and Ollama runtime.", ""])
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_top(rows: list[dict[str, Any]], output: str | Path, count: int = 8) -> None:
    selected = rows[:count]
    target = ensure_parent(output)
    with target.with_suffix(".csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(selected[0]) if selected else [])
        if selected:
            writer.writeheader()
            writer.writerows(selected)
    lines = ["# HP-001 Top 8 Configurations", "", "Selected using partial scores because human quality scoring is pending.", "",
             "| Rank | Model | Size | Context | Temp | Top-p | Avg tokens/sec | Avg latency | Avg peak RAM | Feasibility | Partial score | Reason |",
             "|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|"]
    for row in selected:
        lines.append(f"| {row['final_rank']} | {row['model_name']} | {row['model_size']} | {row['context_length']} | {row['temperature']} | "
                     f"{row['top_p']} | {row['average_tokens_per_sec']} | {row['average_latency_sec']} | {row['average_peak_ram_gb']} | "
                     f"{row['feasibility_status']} | {row['final_score']} | {row['reason_for_selection']} |")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cli(args: Any) -> int:
    rows = rank(args.results, args.hardware)
    export(rows, args.output)
    print(f"Recommendation report saved to {args.output}")
    return 0
