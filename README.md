# LocalAI Compute-Aware Safe System

Python 3.11+ research tooling for compute-aware local LLM benchmarking and a safety-gated Linux assistant. The model can propose commands, but only the deterministic privilege broker can approve, block, back up, log, or execute them.

## Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

Install Ollama separately. On macOS, use the official Ollama app distribution; the Homebrew formula used during HP-001 lacked its required `llama-server` binary.

```bash
ollama pull llama3.2:1b
ollama pull llama3.2:3b
ollama pull qwen2.5:3b
ollama pull mistral:7b
```

## HP-001 Research Dataset

The first controlled experiment is HP-001: MacBook Air M4 with 16GB unified memory. Its corrected dataset contains 480 successful tests across four models. The earlier all-HTTP-500 runtime attempt was discarded.

```bash
python -m localai_system hardware print
python -m localai_system benchmark validate --config configs/benchmark_ollama.yaml
python -m localai_system benchmark dry-run --config configs/benchmark_ollama.yaml
```

Do not rerun the initial 480-case sweep merely to generate reports. Use the preserved dataset:

```bash
python -m localai_system report graphs --results data/results/benchmark_results.csv --output-dir reports/graphs/hp001_macbook_air_m4
python -m localai_system recommend --results data/results/benchmark_results.csv --hardware data/hardware_profiles/HP-001.json --output reports/recommendations.md
python -m localai_system report markdown --results data/results/benchmark_results.csv --hardware data/hardware_profiles/HP-001.json --recommendations reports/recommendations.csv --graphs-dir reports/graphs/hp001_macbook_air_m4 --output reports/benchmark_report.md
```

Future benchmark runs create self-contained `data/runs/<run_id>/` directories containing results, hardware/config/prompt snapshots, environment metadata, and optional raw outputs. Legacy output paths remain supported.

## Safe Broker And Assistant

```bash
python -m localai_system broker classify "df -h"
python -m localai_system broker classify "sudo apt install docker.io"
python -m localai_system broker classify "rm -rf /"
python -m localai_system assistant
python -m localai_system audit list
python -m localai_system rollback list
```

The assistant defaults to no-execute mode. `--execute` is explicit and does not bypass broker classification, approvals, backups, forbidden blocks, or audit logging. Never run the assistant as root.

## Safety Limitations

- This is a research prototype, not a production privilege boundary.
- Unknown approved commands can still be unsafe.
- Execution uses `shell=False`, but no complete OS sandbox is provided.
- Rollback supports existing individual files only.
- Full-system rollback and automatic system-file editing are intentionally out of scope.

## Research Guides

- [HP-001 benchmark report](reports/hp001_macbook_air_m4_benchmark_report.md)
- [Dataset validation](reports/macbook_hp001_dataset_validation.md)
- [Reproducibility checklist](docs/09_usage/reproducibility_checklist.md)
- [Next-phase plan](docs/09_usage/next_phase_top8_30prompt_plan.md)
- [v0.2 audit](docs/09_usage/v0_2_audit_report.md)
- [Release notes](RELEASE_NOTES_v0.2.md)
