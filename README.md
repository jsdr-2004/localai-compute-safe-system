# LocalAI Compute-Aware Safe System

A Python 3.11+ research prototype for compute-aware local LLM benchmarking and a safety-gated Linux assistant. The assistant never receives uncontrolled root access: it proposes commands, while a deterministic privilege broker classifies, approves, logs, backs up, or blocks them.

## Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

Install [Ollama](https://ollama.com/) separately, then pull models used by `configs/benchmark_ollama.yaml`:

```bash
ollama pull llama3.2:1b
ollama pull llama3.2:3b
```

## Hardware And Benchmarks

```bash
python -m localai_system hardware print
python -m localai_system hardware profile --output data/hardware_profiles/HP-001.json
python -m localai_system benchmark validate --config configs/benchmark_ollama.yaml
python -m localai_system benchmark dry-run --config configs/benchmark_ollama.yaml
python -m localai_system benchmark run --config configs/benchmark_ollama.yaml
```

The runner streams Ollama output, samples system RAM/CPU, records failures, writes CSV and JSONL, stores raw outputs separately, skips completed stable test IDs, and continues after individual failures.

## Recommendations And Reports

The included sample data works without Ollama:

```bash
python -m localai_system recommend --results data/results/sample_benchmark_results.csv --hardware data/hardware_profiles/HP-SAMPLE.json --output reports/recommendations.md
python -m localai_system report graphs --results data/results/sample_benchmark_results.csv
python -m localai_system report markdown --results data/results/sample_benchmark_results.csv --output reports/benchmark_report.md
```

Scores use `0.35 quality + 0.25 speed + 0.20 memory efficiency + 0.20 feasibility`. When quality is blank, the available weights are normalized.

## Safe Broker And Assistant

```bash
python -m localai_system broker classify "df -h"
python -m localai_system broker classify "sudo apt install docker.io"
python -m localai_system broker classify "rm -rf /"
python -m localai_system assistant
python -m localai_system audit list
python -m localai_system rollback list
```

The assistant starts with execution disabled. `--execute` enables execution of broker-approved argument vectors using `shell=False`; it does not weaken policy, approval, backup, or audit requirements. Use it only on a suitable Linux test machine.

## Safety Limitations

- This is research prototype code, not a production privilege boundary.
- The deterministic policy is intentionally conservative and incomplete.
- Unknown commands require approval, but approval does not make an unknown command intrinsically safe.
- File backup supports existing individual files only; there is no full-system rollback.
- The broker blocks shell operators and redirection, but it is not a complete shell parser or sandbox.
- Never run the assistant itself as root.

## Reproducibility

Follow [the reproducibility checklist](docs/09_usage/reproducibility_checklist.md). Preserve hardware profiles, configs, prompts, runtime/model versions, raw outputs, all failures, and quality-scoring records with each experiment.

Additional guides:

- [Quickstart](docs/09_usage/quickstart.md)
- [Demo script](docs/09_usage/demo_script.md)
- [Architecture](docs/03_architecture/system_architecture.md)
- [Safety policy](docs/06_security_safety/safety_policy.md)
