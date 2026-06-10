# Quickstart

Requires Python 3.11+.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m localai_system hardware profile --output data/hardware_profiles/HP-001.json
python -m localai_system benchmark dry-run --config configs/benchmark_ollama.yaml
python -m localai_system recommend --results data/results/sample_benchmark_results.csv --hardware data/hardware_profiles/HP-SAMPLE.json --output reports/recommendations.md
python -m localai_system report graphs --results data/results/sample_benchmark_results.csv
python -m localai_system broker classify "rm -rf /"
python -m localai_system assistant
```

The assistant defaults to preview/classify/log mode. Use `--execute` only when intentionally testing approved commands on a suitable Linux test machine.
