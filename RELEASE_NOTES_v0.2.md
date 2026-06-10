# LocalAI Compute-Aware Safe System v0.2

## Summary

v0.2 turns the prototype into a reproducible, paper-ready research release built around the completed HP-001 MacBook Air M4 benchmark.

## New Features

- Self-contained `data/runs/<run_id>/` benchmark directories.
- Config, prompt, hardware, and environment snapshots.
- Warmups, cooldowns, output limits, per-test timeouts, raw-output controls, and resume controls.
- Global configuration recommendations with component scores and ranks.
- HP-001 dataset validation, top-eight selection, complete graphs, and benchmark report.

## HP-001 Outputs

- 480 corrected benchmark rows, all successful.
- Four models, five prompts, eight setting combinations, three repeats.
- CSV, JSONL, 480 raw outputs, validation report, grouped summary, recommendations, and graphs.

## Reproducibility Improvements

- Run IDs and environment metadata.
- Git hash/dirty status, Ollama version/model list, config/prompt snapshots.
- Expanded reproducibility checklist and experiment protocol.

## Safety Improvements

- Expanded deterministic blocks for destructive disks/files, credential extraction, security disabling, log hiding, and untrusted pipe-to-shell commands.
- Assistant remains no-execute by default.
- Audit records include session/run fields and broker policy version.

## Reporting Improvements

- Hardware-aware Markdown benchmark reports.
- Eight HP-001 graphs plus global top-five/top-eight tables.
- Partial-score labeling when human quality is missing.

## Tests

Tests cover profiling, config validation, matrix counts, run directories, metadata, recommendations, reports, safety policy, assistant/broker execution boundaries, audit logs, and rollback.

## Known Limitations

- HP-001 quality scores are pending.
- Multi-hardware and non-Ollama validation are pending.
- The broker is a research prototype, not a production sandbox.

## HP-001 Validation Commands

```bash
python -m localai_system benchmark validate --config configs/benchmark_ollama.yaml
python -m localai_system report markdown --results data/results/benchmark_results.csv --hardware data/hardware_profiles/HP-001.json --recommendations reports/recommendations.csv --graphs-dir reports/graphs/hp001_macbook_air_m4 --output reports/benchmark_report.md
```

## Graph And Recommendation Commands

```bash
python -m localai_system report graphs --results data/results/benchmark_results.csv --output-dir reports/graphs/hp001_macbook_air_m4
python -m localai_system recommend --results data/results/benchmark_results.csv --hardware data/hardware_profiles/HP-001.json --output reports/recommendations.md
```

## Next Top-8 / 30-Prompt Phase

```bash
python -m localai_system benchmark validate --config configs/benchmark_hp001_top8_30prompts.yaml
python -m localai_system benchmark dry-run --config configs/benchmark_hp001_top8_30prompts.yaml
python -m localai_system benchmark run --config configs/benchmark_hp001_top8_30prompts.yaml
```
