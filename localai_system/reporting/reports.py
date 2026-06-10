from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Callable

from localai_system.common.io import ensure_parent


def _number(value: Any) -> float | None:
    try:
        return float(value) if value not in ("", None) else None
    except (ValueError, TypeError):
        return None


def read_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _averages(rows: list[dict[str, str]], group_key: str, metric: str) -> dict[str, float]:
    values: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        value = _number(row.get(metric))
        if value is not None:
            values[row.get(group_key, "unknown")].append(value)
    return {key: mean(items) for key, items in values.items() if items}


def generate_graphs(results: str | Path, output_dir: str | Path) -> list[Path]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = read_rows(results)
    success = [row for row in rows if row.get("status") == "success"]
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    charts = [
        ("model_name", "tokens_per_sec_estimate", "Average Tokens/sec by Model", "Tokens/sec", "avg_tokens_per_sec_by_model.png"),
        ("model_name", "peak_ram_gb", "Peak RAM by Model", "RAM (GB)", "peak_ram_by_model.png"),
        ("model_name", "first_token_latency_sec", "First-token Latency by Model", "Seconds", "first_token_latency_by_model.png"),
        ("context_length", "total_response_time_sec", "Response Time by Context Length", "Seconds", "response_time_by_context_length.png"),
        ("model_name", "final_score", "Score by Model/Configuration", "Score", "score_by_model.png"),
    ]
    paths = []
    for group, metric, title, ylabel, filename in charts:
        values = _averages(success, group, metric)
        if not values:
            continue
        plt.figure(figsize=(8, 4.5))
        plt.bar(list(values), list(values.values()))
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        path = output / filename
        plt.savefig(path)
        plt.close()
        paths.append(path)
    models = sorted({row.get("model_name", "unknown") for row in rows})
    failure_rates = {model: 100 * sum(row.get("status") != "success" for row in rows if row.get("model_name") == model) /
                     max(1, sum(row.get("model_name") == model for row in rows)) for model in models}
    if failure_rates:
        plt.figure(figsize=(8, 4.5))
        plt.bar(list(failure_rates), list(failure_rates.values()))
        plt.title("Failure Rate by Model")
        plt.ylabel("Failure rate (%)")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        path = output / "failure_rate_by_model.png"
        plt.savefig(path)
        plt.close()
        paths.append(path)
    return paths


def markdown_report(results: str | Path, output: str | Path) -> Path:
    rows = read_rows(results)
    success = [row for row in rows if row.get("status") == "success"]
    models = sorted({row.get("model_name", "unknown") for row in rows})
    lines = ["# Benchmark Report", "", f"- Total runs: {len(rows)}", f"- Successful runs: {len(success)}",
             f"- Failed runs: {len(rows) - len(success)}", "", "## Model Summary", "",
             "| Model | Runs | Success Rate | Avg Tokens/sec | Avg Peak RAM GB | Avg First-token Latency sec |",
             "|---|---:|---:|---:|---:|---:|"]
    for model in models:
        model_rows = [row for row in rows if row.get("model_name") == model]
        good = [row for row in model_rows if row.get("status") == "success"]
        avg = lambda metric: mean(values) if (values := [_number(row.get(metric)) for row in good if _number(row.get(metric)) is not None]) else 0
        lines.append(f"| {model} | {len(model_rows)} | {100 * len(good) / max(1, len(model_rows)):.1f}% | "
                     f"{avg('tokens_per_sec_estimate'):.2f} | {avg('peak_ram_gb'):.2f} | {avg('first_token_latency_sec'):.2f} |")
    lines.extend(["", "## Reproducibility Notes", "", "- Preserve the hardware profile used for these runs.",
                  "- Record runtime and model versions.", "- Keep prompts and benchmark configuration with the results.",
                  "- Treat estimated tokens/sec as an approximation unless runtime token counts are present.", ""])
    target = ensure_parent(output)
    target.write_text("\n".join(lines), encoding="utf-8")
    return target


def cli(args: Any) -> int:
    if args.action == "graphs":
        paths = generate_graphs(args.results, args.output_dir)
        print(f"Generated {len(paths)} graphs in {args.output_dir}")
    else:
        path = markdown_report(args.results, args.output)
        print(f"Benchmark report saved to {path}")
    return 0
