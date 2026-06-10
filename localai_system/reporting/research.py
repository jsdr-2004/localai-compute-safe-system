from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from localai_system.common.io import ensure_parent, load_json
from localai_system.recommender.engine import export, export_top, number, rank
from localai_system.reporting.reports import generate_graphs, markdown_report, read_rows

SUMMARY_FIELDS = ("model_name", "model_size", "context_length", "temperature", "top_p")
METRICS = ("first_token_latency_sec", "total_response_time_sec", "tokens_per_sec_estimate",
           "peak_ram_gb", "peak_cpu_usage_percent")


def validate_dataset(results: str | Path, hardware: str | Path, config: str | Path, prompts: str | Path,
                     output: str | Path, summary_csv: str | Path) -> dict[str, Any]:
    rows = read_rows(results)
    success = [row for row in rows if row.get("status") == "success"]
    raw_missing = [row["test_id"] for row in success if not row.get("raw_output_path") or
                   not Path(row["raw_output_path"]).exists() or not Path(row["raw_output_path"]).read_text(encoding="utf-8").strip()]
    duplicate_ids = len(rows) - len({row["test_id"] for row in rows})
    coverage = {field: Counter(row.get(field, "") for row in rows) for field in
                ("model_name", "prompt_id", "context_length", "temperature", "top_p", "repeat_id")}
    invalid = [row for row in rows if not row.get("test_id") or row.get("status") not in {"success", "failed"}]
    usable = len(rows) == 480 and len(success) == 480 and not raw_missing and not invalid and duplicate_ids == 0
    lines = ["# HP-001 MacBook Air M4 Dataset Validation", "",
             f"- Dataset path: `{results}`", f"- Hardware profile path: `{hardware}`",
             f"- Benchmark config path: `{config}`", f"- Prompt file path: `{prompts}`",
             f"- Total rows: {len(rows)}", f"- Success rows: {len(success)}",
             f"- Failed rows: {len(rows) - len(success)}", f"- Duplicate test IDs: {duplicate_ids}",
             f"- Successful rows with empty/missing raw output: {len(raw_missing)}",
             f"- Invalid rows: {len(invalid)}", f"- Usable for Paper 1: **{'yes' if usable else 'no'}**", "",
             "## Model Coverage", "", "| Model | Rows |", "|---|---:|"]
    lines.extend(f"| {key} | {value} |" for key, value in sorted(coverage["model_name"].items()))
    lines.extend(["", "## Prompt Coverage", "", "| Prompt ID | Rows |", "|---|---:|"])
    lines.extend(f"| {key} | {value} |" for key, value in sorted(coverage["prompt_id"].items()))
    lines.extend(["", "## Settings Coverage", "", "| Setting | Value | Rows |", "|---|---|---:|"])
    for field in ("context_length", "temperature", "top_p", "repeat_id"):
        lines.extend(f"| {field} | {key} | {value} |" for key, value in sorted(coverage[field].items()))
    lines.extend(["", "## Invalid-row Summary", "", "No invalid rows were found." if not invalid else f"{len(invalid)} invalid rows require review.",
                  "", "## Limitations", "", "- The benchmark CSV stores raw-output paths rather than embedding output text.",
                  "- Human quality scores are blank and must be added before full weighted conclusions.",
                  "- This is one hardware profile, one runtime backend, and an initial five-prompt sweep.", ""])
    ensure_parent(output).write_text("\n".join(lines), encoding="utf-8")
    grouped: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[field] for field in SUMMARY_FIELDS)].append(row)
    summary = []
    for key, group in grouped.items():
        record: dict[str, Any] = dict(zip(SUMMARY_FIELDS, key))
        for metric in METRICS:
            values = [number(row.get(metric)) for row in group if number(row.get(metric)) is not None]
            record[f"average_{metric}"] = round(mean(values), 4) if values else ""
        record["success_rate"] = round(sum(row.get("status") == "success" for row in group) / len(group), 4)
        summary.append(record)
    with ensure_parent(summary_csv).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(sorted(summary, key=lambda row: tuple(row[field] for field in SUMMARY_FIELDS)))
    return {"rows": rows, "usable": usable, "coverage": coverage}


def hp001_report(results: str | Path, hardware: str | Path, config: str | Path, recommendations_csv: str | Path,
                 top8_csv: str | Path, graphs_dir: str | Path, output: str | Path) -> None:
    rows = read_rows(results)
    profile = load_json(hardware)
    top8 = read_rows(top8_csv)
    models = sorted({row["model_name"] for row in rows})
    success = [row for row in rows if row["status"] == "success"]
    avg = lambda group, metric: mean(number(row[metric]) or 0 for row in group)
    fastest = max(models, key=lambda model: avg([r for r in success if r["model_name"] == model], "tokens_per_sec_estimate"))
    lowest_ram = min(models, key=lambda model: avg([r for r in success if r["model_name"] == model], "peak_ram_gb"))
    lowest_latency = min(models, key=lambda model: avg([r for r in success if r["model_name"] == model], "first_token_latency_sec"))
    lines = ["# HP-001 MacBook Air M4 Local LLM Benchmark Report", "", "## Purpose", "",
             "This is the first controlled fixed-hardware configuration sweep for compute-aware local LLM selection. It establishes an HP-001 baseline without claiming cross-hardware generality.",
             "", "## Hardware Summary", "", f"- CPU/GPU: {profile['cpu_model']} / {profile.get('gpu_model')}",
             f"- CPU cores/threads: {profile['cpu_cores']}/{profile['cpu_threads']}", f"- Unified memory: {profile['ram_gb']} GB",
             f"- OS/kernel: {profile['os']} / {profile['kernel']}", f"- Ollama: {profile.get('ollama_version')}", "",
             "## Model Matrix", "", f"- Models: {', '.join(models)}", "- Context lengths: 1024, 2048",
             "- Temperatures: 0.2, 0.7", "- Top-p: 0.8, 0.95", "- Prompts: 5", "- Repeats: 3", "",
             "## Experimental Design", "", "4 models × 2 context lengths × 2 temperatures × 2 top-p values × 5 prompts × 3 repeats = **480 tests**.",
             "", "## Metrics", "", "- First-token latency", "- Total response time", "- Estimated tokens/sec",
             "- Peak system RAM", "- Peak CPU usage", "- Success/failure status", "- Derived feasibility", "",
             "## Results Summary", "", f"- Successful runs: {len(success)}/{len(rows)}", f"- Fastest average model: **{fastest}**",
             f"- Lowest average peak RAM model: **{lowest_ram}**", f"- Lowest average first-token latency model: **{lowest_latency}**",
             f"- Highest partial-score configuration: **{top8[0]['model_name']}**, context {top8[0]['context_length']}, temperature {top8[0]['temperature']}, top-p {top8[0]['top_p']}.",
             "", "## Top 8 Configurations", "", "| Rank | Model | Size | Context | Temp | Top-p | Avg tokens/sec | Avg latency | Avg peak RAM | Feasibility | Partial score |",
             "|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|"]
    for row in top8:
        lines.append(f"| {row['final_rank']} | {row['model_name']} | {row['model_size']} | {row['context_length']} | {row['temperature']} | {row['top_p']} | "
                     f"{row['average_tokens_per_sec']} | {row['average_latency_sec']} | {row['average_peak_ram_gb']} | {row['feasibility_status']} | {row['final_score']} |")
    lines.extend(["", "## Failure Analysis", "", "No corrected-run failures were recorded. The earlier all-HTTP-500 run was invalid runtime output and was discarded before this dataset.",
                  "", "## Graphs", ""])
    lines.extend(f"- [{path.name}]({path.as_posix()})" for path in sorted(Path(graphs_dir).glob("*.png")))
    lines.extend(["", "## Research Interpretation", "",
                  "On this 16 GB Apple Silicon laptop, the 1B model provides the strongest throughput and memory-efficient interactive baseline. The 3B models trade speed for potentially greater capability, while Mistral 7B remains feasible but has materially lower throughput and longer responses. Human quality review is required before treating the partial-score ranking as a final recommendation.",
                  "", "## Limitations", "", "- One hardware profile only so far.", "- Human quality scoring is not yet completed.",
                  "- Ollama is the only tested backend.", "- The initial sweep uses five prompts.", "- Cross-hardware validation is pending.",
                  "", "## Next Step", "", "Use the selected top eight configurations for a 30-prompt expanded test on HP-001 MacBook Air M4 16GB, HP-002 Ryzen 5 5500U 8GB, and HP-003 RTX 3090-class GPU PC 32GB.", ""])
    ensure_parent(output).write_text("\n".join(lines), encoding="utf-8")


def generate_hp001_artifacts() -> None:
    results = "data/results/benchmark_results.csv"
    hardware = "data/hardware_profiles/HP-001.json"
    config = "configs/benchmark_ollama.yaml"
    prompts = "configs/prompts.json"
    validate_dataset(results, hardware, config, prompts, "reports/macbook_hp001_dataset_validation.md",
                     "reports/macbook_hp001_dataset_summary.csv")
    graph_dir = "reports/graphs/hp001_macbook_air_m4"
    generate_graphs(results, graph_dir)
    rows = rank(results, hardware)
    export(rows, "reports/recommendations.md")
    export_top(rows, "reports/hp001_top_8_configurations.md")
    hp001_report(results, hardware, config, "reports/recommendations.csv", "reports/hp001_top_8_configurations.csv",
                 graph_dir, "reports/hp001_macbook_air_m4_benchmark_report.md")
    markdown_report(results, "reports/benchmark_report.md", hardware, "reports/recommendations.csv", graph_dir)
