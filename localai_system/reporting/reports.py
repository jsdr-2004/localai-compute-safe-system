from __future__ import annotations

import csv
import os
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import mean
from typing import Any

from localai_system.common.io import ensure_parent, load_json


def number(value: Any) -> float | None:
    try:
        return float(value) if value not in ("", None) else None
    except (ValueError, TypeError):
        return None


def read_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def averages(rows: list[dict[str, str]], group_key: str, metric: str) -> dict[str, float]:
    values: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        value = number(row.get(metric))
        if value is not None:
            values[row.get(group_key, "unknown")].append(value)
    return {key: mean(items) for key, items in values.items() if items}


def _bar(plt: Any, values: dict[str, float], title: str, ylabel: str, path: Path) -> None:
    plt.figure(figsize=(8, 4.5))
    plt.bar(list(values), list(values.values()))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def generate_graphs(results: str | Path, output_dir: str | Path) -> list[Path]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = read_rows(results)
    success = [row for row in rows if row.get("status") == "success"]
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    charts = [
        ("model_name", "tokens_per_sec_estimate", "Average Tokens/sec by Model", "Tokens/sec", "average_tokens_per_sec_by_model.png"),
        ("model_name", "first_token_latency_sec", "Average First-token Latency by Model", "Seconds", "average_first_token_latency_by_model.png"),
        ("model_name", "total_response_time_sec", "Average Total Response Time by Model", "Seconds", "average_total_response_time_by_model.png"),
        ("model_name", "peak_ram_gb", "Average Peak RAM by Model", "RAM (GB)", "average_peak_ram_by_model.png"),
        ("context_length", "tokens_per_sec_estimate", "Tokens/sec by Context Length", "Tokens/sec", "tokens_per_sec_by_context_length.png"),
        ("context_length", "total_response_time_sec", "Response Time by Context Length", "Seconds", "total_response_time_by_context_length.png"),
    ]
    paths = []
    for group, metric, title, ylabel, filename in charts:
        values = averages(success, group, metric)
        if values:
            path = output / filename
            _bar(plt, values, title, ylabel, path)
            paths.append(path)
    models = sorted({row.get("model_name", "unknown") for row in rows})
    failures = {model: 100 * sum(row.get("status") != "success" for row in rows if row.get("model_name") == model) /
                max(1, sum(row.get("model_name") == model for row in rows)) for model in models}
    path = output / "failure_rate_by_model.png"
    _bar(plt, failures, "Failure Rate by Model", "Failure rate (%)", path)
    paths.append(path)
    speed, latency, ram = (averages(success, "model_name", metric) for metric in
                           ("tokens_per_sec_estimate", "first_token_latency_sec", "peak_ram_gb"))
    if models:
        x = range(len(models))
        plt.figure(figsize=(10, 5))
        plt.plot(x, [speed.get(model, 0) for model in models], marker="o", label="Tokens/sec")
        plt.plot(x, [latency.get(model, 0) for model in models], marker="o", label="First-token latency")
        plt.plot(x, [ram.get(model, 0) for model in models], marker="o", label="Peak RAM GB")
        plt.xticks(list(x), models, rotation=25, ha="right")
        plt.title("Model Performance Summary")
        plt.legend()
        plt.tight_layout()
        path = output / "model_performance_summary.png"
        plt.savefig(path)
        plt.close()
        paths.append(path)
    return paths


def markdown_report(results: str | Path, output: str | Path, hardware: str | Path | None = None,
                    recommendations: str | Path | None = None, graphs_dir: str | Path = "reports/graphs") -> Path:
    target = ensure_parent(output)
    rows = read_rows(results)
    success = [row for row in rows if row.get("status") == "success"]
    profile = load_json(hardware) if hardware else {}
    models = sorted({row.get("model_name", "unknown") for row in rows})
    run_id = rows[0].get("run_id", "") if rows else ""
    lines = ["# Benchmark Report", "", f"- Date generated: {date.today().isoformat()}", f"- Run ID: {run_id or 'legacy dataset'}",
             f"- Results: `{results}`", "", "## Hardware Profile", ""]
    if profile:
        lines.extend([f"- Profile: {profile.get('hardware_profile_id')}", f"- CPU: {profile.get('cpu_model')}",
                      f"- Cores/threads: {profile.get('cpu_cores')}/{profile.get('cpu_threads')}",
                      f"- RAM: {profile.get('ram_gb')} GB", f"- GPU: {profile.get('gpu_model') or 'none reported'}",
                      f"- OS/kernel: {profile.get('os')} / {profile.get('kernel')}", f"- Ollama: {profile.get('ollama_version')}", ""])
    lines.extend(["## Experiment Summary", "", f"- Total tests: {len(rows)}", f"- Successful: {len(success)}",
                  f"- Failed: {len(rows) - len(success)}", f"- Models: {', '.join(models)}",
                  f"- Prompt categories: {', '.join(sorted({r.get('prompt_category', '') for r in rows}))}", "",
                  "## Model Metrics", "",
                  "| Model | Runs | Success Rate | Avg Tokens/sec | Avg First-token Latency | Avg Total Time | Avg Peak RAM |",
                  "|---|---:|---:|---:|---:|---:|---:|"])
    for model in models:
        group = [row for row in rows if row.get("model_name") == model]
        good = [row for row in group if row.get("status") == "success"]
        avg = lambda metric: mean(values) if (values := [number(row.get(metric)) for row in good if number(row.get(metric)) is not None]) else 0
        lines.append(f"| {model} | {len(group)} | {100 * len(good) / max(1, len(group)):.1f}% | {avg('tokens_per_sec_estimate'):.2f} | "
                     f"{avg('first_token_latency_sec'):.3f} | {avg('total_response_time_sec'):.2f} | {avg('peak_ram_gb'):.2f} |")
    categories = sorted({row.get("prompt_category", "unknown") for row in rows})
    lines.extend(["", "## Prompt Category Metrics", "",
                  "| Category | Runs | Success Rate | Avg Tokens/sec | Avg First-token Latency | Avg Total Time | Avg Peak RAM |",
                  "|---|---:|---:|---:|---:|---:|---:|"])
    for category in categories:
        group = [row for row in rows if row.get("prompt_category") == category]
        good = [row for row in group if row.get("status") == "success"]
        avg = lambda metric: mean(values) if (values := [number(row.get(metric)) for row in good if number(row.get(metric)) is not None]) else 0
        lines.append(f"| {category} | {len(group)} | {100 * len(good) / max(1, len(group)):.1f}% | "
                     f"{avg('tokens_per_sec_estimate'):.2f} | {avg('first_token_latency_sec'):.3f} | "
                     f"{avg('total_response_time_sec'):.2f} | {avg('peak_ram_gb'):.2f} |")
    failures = [row for row in rows if row.get("status") != "success"]
    lines.extend(["", "## Failure Table", ""])
    lines.append("No failures recorded." if not failures else "| Test ID | Model | Error |\n|---|---|---|\n" +
                 "\n".join(f"| {r['test_id']} | {r['model_name']} | {r.get('error', '')} |" for r in failures[:25]))
    if recommendations and Path(recommendations).exists():
        recs = read_rows(recommendations)
        lines.extend(["", "## Top 5 Recommended Configurations", "", "| Rank | Model | Context | Temperature | Top-p | Score |",
                      "|---:|---|---:|---:|---:|---:|"])
        for row in recs[:5]:
            lines.append(f"| {row['final_rank']} | {row['model_name']} | {row['context_length']} | {row['temperature']} | {row['top_p']} | {row['final_score']} |")
    lines.extend(["", "## Graphs", ""])
    for path in sorted(Path(graphs_dir).glob("*.png")):
        relative_path = os.path.relpath(path, start=target.parent)
        lines.append(f"- [{path.name}]({Path(relative_path).as_posix()})")
    lines.extend(["", "## Limitations", "", "- Quality scores may be blank; recommendation scores are partial when so marked.",
                  "- Results are specific to one hardware profile and the Ollama backend.",
                  f"- This dataset contains {len({row.get('prompt_id', '') for row in rows})} distinct prompts.",
                  "", "## Reproducibility Checklist", "", "- [x] Hardware profile preserved", "- [x] Config and prompt files preserved",
                  "- [x] CSV, JSONL, failures, and raw outputs preserved", "- [x] Runtime/model versions recorded where available",
                  "- [ ] Human quality scoring complete", ""])
    target.write_text("\n".join(lines), encoding="utf-8")
    return target


def cli(args: Any) -> int:
    if args.action == "graphs":
        paths = generate_graphs(args.results, args.output_dir)
        print(f"Generated {len(paths)} graphs in {args.output_dir}")
    else:
        path = markdown_report(args.results, args.output, args.hardware, args.recommendations, args.graphs_dir)
        print(f"Benchmark report saved to {path}")
    return 0
